"""
Chandrayaan-2 PDS4 and ISDA XML/LBL Metadata Parser.
SIH26166 Compliant.
"""
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict, Any, Tuple
import xml.etree.ElementTree as ET
import re
import logging

logger = logging.getLogger(__name__)

NAMESPACES = {
    "pds": "http://pds.nasa.gov/pds4/pds/v1",
    "isda": "https://isda.issdc.gov.in/pds4/isda/v1",
}


@dataclass
class ChandrayaanMetadata:
    product_id: str = "UNKNOWN"
    spacecraft: str = "UNKNOWN"
    instrument: str = "UNKNOWN"
    target: str = "MOON"
    start_time: Optional[str] = None
    stop_time: Optional[str] = None
    lines: int = 0
    samples: int = 0
    bands: int = 1
    data_type: str = "uint8"
    pixel_resolution_m: Optional[float] = None
    upper_left_lat: Optional[float] = None
    upper_left_lon: Optional[float] = None
    lower_right_lat: Optional[float] = None
    lower_right_lon: Optional[float] = None
    solar_azimuth_deg: Optional[float] = None
    solar_elevation_deg: Optional[float] = None
    incidence_angle_deg: Optional[float] = None
    emission_angle_deg: Optional[float] = None
    phase_angle_deg: Optional[float] = None
    is_verified_chandrayaan: bool = False
    validation_notes: list[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "product_id": self.product_id,
            "spacecraft": self.spacecraft,
            "instrument": self.instrument,
            "target": self.target,
            "start_time": self.start_time,
            "stop_time": self.stop_time,
            "dimensions": f"{self.lines} lines x {self.samples} samples x {self.bands} bands",
            "data_type": self.data_type,
            "pixel_resolution_m": self.pixel_resolution_m,
            "coordinates": {
                "upper_left": [self.upper_left_lat, self.upper_left_lon],
                "lower_right": [self.lower_right_lat, self.lower_right_lon],
            },
            "sun_angles": {
                "solar_azimuth_deg": self.solar_azimuth_deg,
                "solar_elevation_deg": self.solar_elevation_deg,
                "incidence_angle_deg": self.incidence_angle_deg,
                "emission_angle_deg": self.emission_angle_deg,
                "phase_angle_deg": self.phase_angle_deg,
            },
            "is_verified_chandrayaan": self.is_verified_chandrayaan,
            "validation_notes": self.validation_notes,
        }


def _safe_float(element: Optional[ET.Element]) -> Optional[float]:
    if element is not None and element.text:
        try:
            return float(element.text.strip())
        except (ValueError, TypeError):
            return None
    return None


def _safe_int(element: Optional[ET.Element]) -> Optional[int]:
    if element is not None and element.text:
        try:
            return int(element.text.strip())
        except (ValueError, TypeError):
            return None
    return None


def _find_text(root: ET.Element, xpath: str, namespaces: Dict[str, str]) -> Optional[str]:
    elem = root.find(xpath, namespaces=namespaces)
    if elem is not None and elem.text:
        return elem.text.strip()
    # Fallback without namespaces if prefix matching fails
    plain_tag = xpath.split(":")[-1] if ":" in xpath else xpath
    for e in root.iter():
        if e.tag.endswith(plain_tag) and e.text:
            return e.text.strip()
    return None


def parse_pds4_metadata(xml_path: Path) -> ChandrayaanMetadata:
    """
    Parse a Chandrayaan-2 PDS4 XML label file.
    Gracefully handles missing optional tags and verifies mission provenance.
    """
    meta = ChandrayaanMetadata()
    if not xml_path.exists():
        meta.validation_notes.append(f"File not found: {xml_path}")
        return meta

    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
    except Exception as e:
        meta.validation_notes.append(f"XML parse error: {e}")
        return meta

    # Spacecraft / Instrument Identification
    meta.spacecraft = _find_text(root, ".//pds:Observing_System_Component[pds:type='Spacecraft']/pds:name", NAMESPACES) or "UNKNOWN"
    meta.instrument = _find_text(root, ".//pds:Observing_System_Component[pds:type='Instrument']/pds:name", NAMESPACES) or "UNKNOWN"
    
    # Fallback search for instrument in title or product ID
    prod_id = _find_text(root, ".//pds:logical_identifier", NAMESPACES) or xml_path.stem
    meta.product_id = prod_id

    # If instrument is still unknown, infer from product ID naming convention
    id_lower = prod_id.lower()
    if "ohr" in id_lower or "ch2_ohr" in id_lower:
        meta.instrument = "OHRC"
        meta.pixel_resolution_m = meta.pixel_resolution_m or 0.25
    elif "tmc" in id_lower or "ch2_tmc" in id_lower:
        meta.instrument = "TMC-2"
        meta.pixel_resolution_m = meta.pixel_resolution_m or 5.0
    elif "iir" in id_lower or "ch2_iir" in id_lower:
        meta.instrument = "IIRS"
        meta.pixel_resolution_m = meta.pixel_resolution_m or 80.0

    # Observation times
    meta.start_time = _find_text(root, ".//pds:start_date_time", NAMESPACES)
    meta.stop_time = _find_text(root, ".//pds:stop_date_time", NAMESPACES)

    # Geometry & Dimensions
    line_elem = root.find(".//pds:Axis_Array[pds:axis_name='Line']/pds:elements", namespaces=NAMESPACES)
    if line_elem is None:
        # Check without namespace
        for axis in root.iter():
            if axis.tag.endswith("Axis_Array"):
                name = axis.find("axis_name") if axis.find("axis_name") is not None else axis.find("{http://pds.nasa.gov/pds4/pds/v1}axis_name")
                if name is not None and name.text == "Line":
                    elem = axis.find("elements") if axis.find("elements") is not None else axis.find("{http://pds.nasa.gov/pds4/pds/v1}elements")
                    line_elem = elem
    meta.lines = _safe_int(line_elem) or 0

    sample_elem = root.find(".//pds:Axis_Array[pds:axis_name='Sample']/pds:elements", namespaces=NAMESPACES)
    if sample_elem is None:
        for axis in root.iter():
            if axis.tag.endswith("Axis_Array"):
                name = axis.find("axis_name") if axis.find("axis_name") is not None else axis.find("{http://pds.nasa.gov/pds4/pds/v1}axis_name")
                if name is not None and name.text == "Sample":
                    elem = axis.find("elements") if axis.find("elements") is not None else axis.find("{http://pds.nasa.gov/pds4/pds/v1}elements")
                    sample_elem = elem
    meta.samples = _safe_int(sample_elem) or 0

    band_elem = root.find(".//pds:Axis_Array[pds:axis_name='Band']/pds:elements", namespaces=NAMESPACES)
    meta.bands = _safe_int(band_elem) or 1

    # Data Type
    dt_elem = root.find(".//pds:data_type", namespaces=NAMESPACES)
    if dt_elem is not None and dt_elem.text:
        meta.data_type = dt_elem.text.strip()

    # Coordinates from ISDA namespace
    meta.upper_left_lat = _safe_float(root.find(".//isda:upper_left_latitude", namespaces=NAMESPACES))
    meta.upper_left_lon = _safe_float(root.find(".//isda:upper_left_longitude", namespaces=NAMESPACES))
    meta.lower_right_lat = _safe_float(root.find(".//isda:lower_right_latitude", namespaces=NAMESPACES))
    meta.lower_right_lon = _safe_float(root.find(".//isda:lower_right_longitude", namespaces=NAMESPACES))

    # Sun Angles
    meta.solar_azimuth_deg = _safe_float(root.find(".//isda:solar_azimuth_angle", namespaces=NAMESPACES))
    meta.solar_elevation_deg = _safe_float(root.find(".//isda:solar_elevation_angle", namespaces=NAMESPACES))
    meta.incidence_angle_deg = _safe_float(root.find(".//isda:incidence_angle", namespaces=NAMESPACES))
    meta.emission_angle_deg = _safe_float(root.find(".//isda:emission_angle", namespaces=NAMESPACES))
    meta.phase_angle_deg = _safe_float(root.find(".//isda:phase_angle", namespaces=NAMESPACES))

    # Provenance Validation
    is_ch2 = (
        "chandrayaan" in meta.spacecraft.lower()
        or "ch2" in meta.product_id.lower()
        or "ch-2" in meta.spacecraft.lower()
        or any("isda" in elem.tag for elem in root.iter())
    )
    is_valid_sensor = any(s in meta.instrument.upper() for s in ["OHRC", "TMC", "IIRS"])

    if is_ch2 and is_valid_sensor:
        meta.is_verified_chandrayaan = True
        meta.validation_notes.append("Verified official Chandrayaan-2 PDS4 XML label.")
    else:
        meta.is_verified_chandrayaan = False
        meta.validation_notes.append("Unverified provenance: Missing explicit Chandrayaan-2 or payload tag.")

    return meta
