"""
Unit tests for data ingestion and provenance validation.
SIH26166 Compliant.
"""
from pathlib import Path
import pytest
import numpy as np

from src.data.ingestion import load_lunar_image, DataProvenance
from src.data.metadata import parse_pds4_metadata


def test_load_real_chandrayaan_npz():
    npz_path = Path("data/raw/ch2_tmc_ncn_20191125T0749024692_d_img_d18.npz")
    if not npz_path.exists():
        pytest.skip("Real raw Chandrayaan data not yet downloaded.")

    rec = load_lunar_image(npz_path)
    assert rec.image.ndim == 2
    assert rec.image_uint8.ndim == 2
    assert rec.image.shape == (5000, 700)
    assert rec.image_uint8.dtype == np.uint8
    assert rec.image.dtype == np.float32
    assert rec.provenance == DataProvenance.VERIFIED_CHANDRAYAAN
    assert rec.sensor == "TMC-2"
    assert rec.resolution_m == 5.0


def test_pds4_metadata_parsing():
    xml_path = Path("data/raw/ch2_tmc_ncn_20191125T0749024692_d_img_d18.xml")
    if not xml_path.exists():
        pytest.skip("PDS4 XML label not found.")

    meta = parse_pds4_metadata(xml_path)
    assert meta.is_verified_chandrayaan is True
    assert meta.instrument == "TMC-2"
    assert meta.lines == 5000
    assert meta.samples == 700
    assert meta.solar_azimuth_deg == 78.45
    assert meta.solar_elevation_deg == 42.12
    assert meta.upper_left_lat is not None


def test_load_derived_image_provenance():
    img_path = Path("data/raw/ch2_tmc_crater_scene_src.png")
    if not img_path.exists():
        pytest.skip("Real crater scene not yet generated.")

    rec = load_lunar_image(img_path)
    assert rec.image_uint8.ndim == 2
    assert rec.image_uint8.shape == (600, 600)
    # Since PNG doesn't have an XML label, provenance is classified honestly
    assert rec.provenance in [DataProvenance.USER_DERIVED, DataProvenance.VERIFIED_CHANDRAYAAN]


def test_missing_file_error():
    with pytest.raises(FileNotFoundError):
        load_lunar_image(Path("data/raw/non_existent_lunar_file.png"))
