"""
Unit tests for illumination-invariant preprocessing methods.
SIH26166 Compliant.
"""
import numpy as np
from src.data.preprocessing import preprocess_image


def test_preprocessing_methods():
    # Synthetic test pattern simulating crater rim gradient
    img = np.zeros((100, 100), dtype=np.uint8)
    img[20:80, 20:80] = 120
    img[30:70, 30:70] = 40

    for method in ["raw", "clahe", "gradient", "phase_congruency"]:
        out = preprocess_image(img, method=method)
        assert out.shape == img.shape
        assert out.dtype == np.uint8
        assert not np.isnan(out).any()
        assert not np.isinf(out).any()
        assert out.max() <= 255
        assert out.min() >= 0
