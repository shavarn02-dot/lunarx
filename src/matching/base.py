"""
Abstract Base Matcher and MatchResult dataclass.
SIH26166 Compliant.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import numpy as np


@dataclass
class MatchResult:
    keypoints_src: np.ndarray  # Shape (N, 2), float32 (x, y)
    keypoints_ref: np.ndarray  # Shape (N, 2), float32 (x, y)
    confidence: np.ndarray     # Shape (N,), float32 in [0, 1]
    method_name: str
    runtime_sec: float
    num_raw_matches: int
    success: bool = True
    error_message: str = ""

    def __post_init__(self):
        if len(self.keypoints_src) != len(self.keypoints_ref):
            raise ValueError("keypoints_src and keypoints_ref must have the same length.")
        if len(self.keypoints_src) == 0:
            self.success = False
            self.error_message = self.error_message or "Zero correspondences detected."

    @property
    def count(self) -> int:
        return len(self.keypoints_src)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "method": self.method_name,
            "raw_matches": self.num_raw_matches,
            "valid_matches": self.count,
            "runtime_sec": round(self.runtime_sec, 4),
            "success": self.success,
            "error_message": self.error_message,
        }


class BaseMatcher(ABC):
    """Abstract interface for all feature matching algorithms."""

    def __init__(self, name: str, params: Optional[Dict[str, Any]] = None):
        self.name = name
        self.params = params or {}

    @abstractmethod
    def match(self, src_u8: np.ndarray, ref_u8: np.ndarray) -> MatchResult:
        """
        Detect and match features between source and reference 8-bit images.
        Returns MatchResult with matched keypoint coordinates (x, y).
        """
        pass
