"""
Unit and integration tests for feature matching methods.
SIH26166 Compliant.
"""
from pathlib import Path
import pytest
import numpy as np
import cv2

from src.matching import SIFTMatcher, ORBMatcher, SuperPointLightGlueMatcher, get_matcher
from src.data.ingestion import load_lunar_image


@pytest.fixture
def real_lunar_pair():
    p1 = Path("data/raw/ch2_tmc_crater_scene_src.png")
    p2 = Path("data/raw/ch2_tmc_crater_scene_ref.png")
    if not p1.exists() or not p2.exists():
        pytest.skip("Real Chandrayaan data pairs not found.")
    img1 = cv2.imread(str(p1), cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(str(p2), cv2.IMREAD_GRAYSCALE)
    return img1, img2


def test_sift_matching_real_data(real_lunar_pair):
    img1, img2 = real_lunar_pair
    matcher = SIFTMatcher({"ratio_threshold": 0.75})
    res = matcher.match(img1, img2)

    assert res.success is True
    assert res.count > 50
    assert res.keypoints_src.shape[1] == 2
    assert res.keypoints_ref.shape[1] == 2
    assert res.confidence.min() >= 0.0
    assert res.confidence.max() <= 1.0
    assert res.runtime_sec > 0.0


def test_orb_matching_real_data(real_lunar_pair):
    img1, img2 = real_lunar_pair
    matcher = ORBMatcher({"ratio_threshold": 0.80})
    res = matcher.match(img1, img2)

    assert res.success is True
    assert res.count > 20
    assert res.keypoints_src.shape[1] == 2
    assert res.keypoints_ref.shape[1] == 2


def test_superpoint_lightglue_real_data(real_lunar_pair):
    img1, img2 = real_lunar_pair
    matcher = SuperPointLightGlueMatcher({"max_num_keypoints": 512})
    res = matcher.match(img1, img2)

    assert res.success is True
    assert res.count > 20
    assert res.keypoints_src.shape[1] == 2
    assert res.keypoints_ref.shape[1] == 2


def test_get_matcher_factory():
    m_sift = get_matcher("sift")
    assert isinstance(m_sift, SIFTMatcher)
    m_orb = get_matcher("orb")
    assert isinstance(m_orb, ORBMatcher)
    m_sp = get_matcher("superpoint_lightglue")
    assert isinstance(m_sp, SuperPointLightGlueMatcher)

    with pytest.raises(ValueError):
        get_matcher("unsupported_matcher_name")
