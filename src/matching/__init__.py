"""
Feature matching package: Classical (SIFT, ORB), SuperPoint+LightGlue, and LoFTR.
"""
from typing import Optional, Dict, Any

from src.matching.base import BaseMatcher, MatchResult
from src.matching.classical import SIFTMatcher, ORBMatcher
from src.matching.superpoint_lightglue import SuperPointLightGlueMatcher
from src.matching.loftr_matcher import LoFTRMatcher

__all__ = [
    "BaseMatcher",
    "MatchResult",
    "SIFTMatcher",
    "ORBMatcher",
    "SuperPointLightGlueMatcher",
    "LoFTRMatcher",
    "get_matcher",
]


def get_matcher(method_name: str, params: Optional[Dict[str, Any]] = None) -> BaseMatcher:
    """Factory function for matching algorithms."""
    m = method_name.lower().replace("_", "").replace("+", "").replace("-", "")
    if m in ["sift"]:
        return SIFTMatcher(params)
    elif m in ["orb"]:
        return ORBMatcher(params)
    elif m in ["superpointlightglue", "lightglue", "superpoint"]:
        return SuperPointLightGlueMatcher(params)
    elif m in ["loftr"]:
        return LoFTRMatcher(params)
    else:
        raise ValueError(f"Unknown matching method: {method_name}. Supported: SIFT, ORB, SuperPoint+LightGlue, LoFTR.")
