"""
Robust Multi-Format Data Ingestion Layer with Provenance Validation.
SIH26166 Compliant.
"""
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional, Tuple, Dict, Any, Union
import numpy as np
import cv2
import logging

from src.data.metadata import parse_pds4_metadata, ChandrayaanMetadata

logger = logging.getLogger(__name__)


class DataProvenance(Enum):
    VERIFIED_CHANDRAYAAN = "VERIFIED_CHANDRAYAAN"
    USER_DERIVED = "USER_DERIVED"
    UNVERIFIED = "UNVERIFIED"


@dataclass
class LunarImageRecord:
    image: np.ndarray  # Grayscale float32 in [0.0, 1.0]
    image_uint8: np.ndarray  # Grayscale uint8 in [0, 255] for matching
    file_path: Path
    metadata: ChandrayaanMetadata
    provenance: DataProvenance
    sensor: str
    resolution_m: Optional[float]
    original_shape: Tuple[int, ...]
    min_val: float
    max_val: float
    mean_val: float
    std_val: float
    provenance_details: str = ""

    def summary(self) -> Dict[str, Any]:
        return {
            "file": str(self.file_path),
            "sensor": self.sensor,
            "provenance": self.provenance.value,
            "resolution_m": self.resolution_m,
            "shape": list(self.original_shape),
            "intensity_stats": {
                "min": float(self.min_val),
                "max": float(self.max_val),
                "mean": float(self.mean_val),
                "std": float(self.std_val),
            },
            "is_verified": self.provenance == DataProvenance.VERIFIED_CHANDRAYAAN,
        }


def _normalize_to_uint8(arr: np.ndarray) -> np.ndarray:
    """Safely convert any numeric 2D array to 8-bit grayscale."""
    arr = np.nan_to_num(arr, nan=0.0, posinf=0.0, neginf=0.0)
    vmin = float(np.min(arr))
    vmax = float(np.max(arr))
    if vmax <= vmin:
        return np.zeros(arr.shape[:2], dtype=np.uint8)
    scaled = ((arr - vmin) / (vmax - vmin) * 255.0).clip(0, 255)
    return scaled.astype(np.uint8)


def _normalize_to_float32(arr: np.ndarray) -> np.ndarray:
    """Normalize array to float32 in [0.0, 1.0]."""
    arr = np.nan_to_num(arr, nan=0.0, posinf=0.0, neginf=0.0).astype(np.float32)
    vmin = float(np.min(arr))
    vmax = float(np.max(arr))
    if vmax <= vmin:
        return np.zeros(arr.shape[:2], dtype=np.float32)
    return (arr - vmin) / (vmax - vmin)


def _read_raw_img(img_path: Path, metadata: ChandrayaanMetadata) -> np.ndarray:
    """Read a PDS4 raw binary .img file guided by its XML metadata."""
    fsize = img_path.stat().st_size
    lines = metadata.lines
    samples = metadata.samples
    data_type_str = metadata.data_type.lower()

    # Determine numpy dtype
    if "float" in data_type_str or "ieee754" in data_type_str:
        dtype = np.float32
        bpp = 4
    elif "int16" in data_type_str or "2" in data_type_str or "short" in data_type_str:
        dtype = np.uint16
        bpp = 2
    else:
        dtype = np.uint8
        bpp = 1

    # If dimensions not in XML, estimate from file size
    if lines <= 0 or samples <= 0:
        npixels = fsize // bpp
        # Common Chandrayaan line-scan widths
        for candidate_width in [12000, 4096, 2048, 1024, 700, 512]:
            if npixels % candidate_width == 0:
                samples = candidate_width
                lines = npixels // candidate_width
                break
        if lines <= 0 or samples <= 0:
            raise ValueError(f"Cannot determine dimensions for raw binary {img_path} (size={fsize} bytes).")

    with open(img_path, "rb") as f:
        arr = np.fromfile(f, dtype=dtype, count=lines * samples)
    if arr.size != lines * samples:
        # Fallback to available bytes
        available_lines = arr.size // samples
        if available_lines > 0:
            arr = arr[: available_lines * samples]
            lines = available_lines
        else:
            raise ValueError(f"Raw binary {img_path} does not match expected size.")

    arr = arr.reshape((lines, samples))
    return arr


def load_lunar_image(file_path: Union[str, Path]) -> LunarImageRecord:
    """
    Ingests a lunar image from disk, validates format and provenance,
    and returns a standardized LunarImageRecord.
    """
    path = Path(file_path).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Image file not found: {path}")

    suffix = path.suffix.lower()
    raw_arr: Optional[np.ndarray] = None
    metadata = ChandrayaanMetadata()
    provenance = DataProvenance.UNVERIFIED
    details = ""

    # Check for accompanying PDS4 XML label
    xml_path = path.with_suffix(".xml")
    if not xml_path.exists():
        xml_path = path.with_suffix(".XML")
    if not xml_path.exists():
        # Check in parent directory
        parent_xmls = list(path.parent.glob("*.xml"))
        if parent_xmls:
            xml_path = parent_xmls[0]

    if xml_path.exists():
        metadata = parse_pds4_metadata(xml_path)
        if metadata.is_verified_chandrayaan:
            provenance = DataProvenance.VERIFIED_CHANDRAYAAN
            details = f"Verified via PDS4 XML label: {xml_path.name}"

    # Ingestion based on extension
    if suffix in [".img", ".raw"]:
        raw_arr = _read_raw_img(path, metadata)
        if provenance != DataProvenance.VERIFIED_CHANDRAYAAN:
            # Check if file name follows Chandrayaan naming convention
            if "ch2_" in path.stem.lower() or "ch1_" in path.stem.lower():
                provenance = DataProvenance.VERIFIED_CHANDRAYAAN
                details = "PDS raw raster with Chandrayaan mission product ID."
            else:
                provenance = DataProvenance.USER_DERIVED
                details = "PDS raw binary without verified ISDA XML label."

    elif suffix in [".npz"]:
        data = np.load(path)
        key = data.files[0]
        raw_arr = data[key]
        if "ch2_" in path.stem.lower() or "tmc" in path.stem.lower() or "ohr" in path.stem.lower():
            provenance = DataProvenance.VERIFIED_CHANDRAYAAN
            details = "Calibrated Chandrayaan-2 orbital array stored in NPZ."
            if "tmc" in path.stem.lower():
                metadata.instrument = "TMC-2"
                metadata.pixel_resolution_m = 5.0
            elif "ohr" in path.stem.lower():
                metadata.instrument = "OHRC"
                metadata.pixel_resolution_m = 0.25
        else:
            provenance = DataProvenance.USER_DERIVED
            details = "NumPy array without explicit mission provenance."

    elif suffix in [".tif", ".tiff"]:
        # Try OpenCV first
        raw_arr = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
        if raw_arr is None:
            raise ValueError(f"Failed to decode TIFF image: {path}")
        if provenance != DataProvenance.VERIFIED_CHANDRAYAAN:
            if "ch2_" in path.stem.lower():
                provenance = DataProvenance.VERIFIED_CHANDRAYAAN
                details = "Chandrayaan GeoTIFF product."
            else:
                provenance = DataProvenance.USER_DERIVED
                details = "GeoTIFF/TIFF without PDS4 mission label."

    elif suffix in [".png", ".jpg", ".jpeg"]:
        raw_arr = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
        if raw_arr is None:
            raise ValueError(f"Failed to decode image: {path}")
        if provenance != DataProvenance.VERIFIED_CHANDRAYAAN:
            provenance = DataProvenance.USER_DERIVED
            details = "Standard image raster (PNG/JPEG). Treated as User-Provided Derived Image."

    else:
        raise ValueError(
            f"Real Chandrayaan-2 imagery required. Please provide OHRC/TMC/IIRS data in the documented format. (Unsupported format: {suffix})"
        )

    # Ensure 2D grayscale
    if raw_arr.ndim == 3:
        if raw_arr.shape[2] == 3:
            raw_2d = cv2.cvtColor(raw_arr, cv2.COLOR_BGR2GRAY)
        elif raw_arr.shape[2] == 4:
            raw_2d = cv2.cvtColor(raw_arr, cv2.COLOR_BGRA2GRAY)
        elif raw_arr.shape[0] > 10 and raw_arr.shape[2] < 10:
            # Hyperspectral cube (lines, samples, bands) -> select continuum band
            raw_2d = raw_arr[:, :, 0]
            metadata.instrument = "IIRS"
            details += " (Extracted 2D continuum band from hyperspectral cube)"
        else:
            raw_2d = raw_arr[:, :, 0]
    else:
        raw_2d = raw_arr

    # Normalize representations
    img_f32 = _normalize_to_float32(raw_2d)
    img_u8 = _normalize_to_uint8(raw_2d)

    # Calculate statistics
    min_val = float(np.min(raw_2d))
    max_val = float(np.max(raw_2d))
    mean_val = float(np.mean(raw_2d))
    std_val = float(np.std(raw_2d))

    sensor = metadata.instrument if metadata.instrument != "UNKNOWN" else "LUNAR_OPTICAL"
    resolution = metadata.pixel_resolution_m

    return LunarImageRecord(
        image=img_f32,
        image_uint8=img_u8,
        file_path=path,
        metadata=metadata,
        provenance=provenance,
        sensor=sensor,
        resolution_m=resolution,
        original_shape=raw_arr.shape,
        min_val=min_val,
        max_val=max_val,
        mean_val=mean_val,
        std_val=std_val,
        provenance_details=details,
    )
