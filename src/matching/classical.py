"""
Classical Feature Matchers: SIFT and ORB with Lowe's Ratio Test.
SIH26166 Compliant.
"""
import time
from typing import Optional, Dict, Any
import numpy as np
import cv2
import logging

from src.matching.base import BaseMatcher, MatchResult

logger = logging.getLogger(__name__)


class SIFTMatcher(BaseMatcher):
    def __init__(self, params: Optional[Dict[str, Any]] = None):
        super().__init__("SIFT", params)
        self.n_features = self.params.get("n_features", 2000)
        self.ratio_threshold = self.params.get("ratio_threshold", 0.75)
        self.sift = cv2.SIFT_create(nfeatures=self.n_features)
        self.matcher = cv2.BFMatcher(cv2.NORM_L2)

    def match(self, src_u8: np.ndarray, ref_u8: np.ndarray) -> MatchResult:
        t0 = time.perf_counter()
        kp1, des1 = self.sift.detectAndCompute(src_u8, None)
        kp2, des2 = self.sift.detectAndCompute(ref_u8, None)

        if des1 is None or des2 is None or len(kp1) < 4 or len(kp2) < 4:
            runtime = time.perf_counter() - t0
            return MatchResult(
                keypoints_src=np.empty((0, 2), dtype=np.float32),
                keypoints_ref=np.empty((0, 2), dtype=np.float32),
                confidence=np.empty((0,), dtype=np.float32),
                method_name=self.name,
                runtime_sec=runtime,
                num_raw_matches=0,
                success=False,
                error_message="Insufficient keypoints detected by SIFT.",
            )

        knn_matches = self.matcher.knnMatch(des1, des2, k=2)
        raw_count = len(knn_matches)
        good_pts_src = []
        good_pts_ref = []
        confidences = []

        for m_pair in knn_matches:
            if len(m_pair) == 2:
                m, n = m_pair
                if m.distance < self.ratio_threshold * n.distance:
                    good_pts_src.append(kp1[m.queryIdx].pt)
                    good_pts_ref.append(kp2[m.trainIdx].pt)
                    # Confidence as normalized inverted distance ratio
                    conf = max(0.0, min(1.0, 1.0 - (m.distance / (n.distance + 1e-6))))
                    confidences.append(conf)

        runtime = time.perf_counter() - t0
        kps_src = np.array(good_pts_src, dtype=np.float32).reshape(-1, 2)
        kps_ref = np.array(good_pts_ref, dtype=np.float32).reshape(-1, 2)
        confs = np.array(confidences, dtype=np.float32)

        return MatchResult(
            keypoints_src=kps_src,
            keypoints_ref=kps_ref,
            confidence=confs,
            method_name=self.name,
            runtime_sec=runtime,
            num_raw_matches=raw_count,
            success=len(kps_src) >= 4,
            error_message="" if len(kps_src) >= 4 else "Insufficient ratio-filtered SIFT matches.",
        )


class ORBMatcher(BaseMatcher):
    def __init__(self, params: Optional[Dict[str, Any]] = None):
        super().__init__("ORB", params)
        self.n_features = self.params.get("n_features", 2000)
        self.ratio_threshold = self.params.get("ratio_threshold", 0.75)
        self.orb = cv2.ORB_create(nfeatures=self.n_features)
        self.matcher = cv2.BFMatcher(cv2.NORM_HAMMING)

    def match(self, src_u8: np.ndarray, ref_u8: np.ndarray) -> MatchResult:
        t0 = time.perf_counter()
        kp1, des1 = self.orb.detectAndCompute(src_u8, None)
        kp2, des2 = self.orb.detectAndCompute(ref_u8, None)

        if des1 is None or des2 is None or len(kp1) < 4 or len(kp2) < 4:
            runtime = time.perf_counter() - t0
            return MatchResult(
                keypoints_src=np.empty((0, 2), dtype=np.float32),
                keypoints_ref=np.empty((0, 2), dtype=np.float32),
                confidence=np.empty((0,), dtype=np.float32),
                method_name=self.name,
                runtime_sec=runtime,
                num_raw_matches=0,
                success=False,
                error_message="Insufficient keypoints detected by ORB.",
            )

        knn_matches = self.matcher.knnMatch(des1, des2, k=2)
        raw_count = len(knn_matches)
        good_pts_src = []
        good_pts_ref = []
        confidences = []

        for m_pair in knn_matches:
            if len(m_pair) == 2:
                m, n = m_pair
                if m.distance < self.ratio_threshold * n.distance:
                    good_pts_src.append(kp1[m.queryIdx].pt)
                    good_pts_ref.append(kp2[m.trainIdx].pt)
                    conf = max(0.0, min(1.0, 1.0 - (m.distance / (n.distance + 1e-6))))
                    confidences.append(conf)

        runtime = time.perf_counter() - t0
        kps_src = np.array(good_pts_src, dtype=np.float32).reshape(-1, 2)
        kps_ref = np.array(good_pts_ref, dtype=np.float32).reshape(-1, 2)
        confs = np.array(confidences, dtype=np.float32)

        return MatchResult(
            keypoints_src=kps_src,
            keypoints_ref=kps_ref,
            confidence=confs,
            method_name=self.name,
            runtime_sec=runtime,
            num_raw_matches=raw_count,
            success=len(kps_src) >= 4,
            error_message="" if len(kps_src) >= 4 else "Insufficient ratio-filtered ORB matches.",
        )
