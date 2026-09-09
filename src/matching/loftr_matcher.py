"""
LoFTR (Detector-Free Local Feature Matching with Transformers) Matcher.
SIH26166 Compliant.
"""
import time
from typing import Optional, Dict, Any
import numpy as np
import cv2
import logging

from src.matching.base import BaseMatcher, MatchResult

logger = logging.getLogger(__name__)


class LoFTRMatcher(BaseMatcher):
    def __init__(self, params: Optional[Dict[str, Any]] = None):
        super().__init__("LoFTR", params)
        self.pretrained = self.params.get("pretrained", "outdoor")
        self.max_dim = self.params.get("max_dim", 840)
        self.device = "cpu"
        self._initialized = False
        self._matcher = None

    def _lazy_init(self):
        if self._initialized:
            return
        import torch
        import ssl
        try:
            # Bypass Windows missing root cert for academic mirror download
            ssl._create_default_https_context = ssl._create_unverified_context
        except Exception:
            pass

        from kornia.feature import LoFTR

        self.torch = torch
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Initializing LoFTR ({self.pretrained}) on {self.device}...")
        self._matcher = LoFTR(pretrained=self.pretrained).eval().to(self.device)
        self._initialized = True

    def match(self, src_u8: np.ndarray, ref_u8: np.ndarray) -> MatchResult:
        t0 = time.perf_counter()
        try:
            self._lazy_init()
        except Exception as e:
            runtime = time.perf_counter() - t0
            logger.error(f"Failed to load LoFTR: {e}")
            return MatchResult(
                keypoints_src=np.empty((0, 2), dtype=np.float32),
                keypoints_ref=np.empty((0, 2), dtype=np.float32),
                confidence=np.empty((0,), dtype=np.float32),
                method_name=self.name,
                runtime_sec=runtime,
                num_raw_matches=0,
                success=False,
                error_message=f"LoFTR initialization error: {e}",
            )

        import torch

        # Compute scaling factors to keep dimensions bounded and multiples of 8
        h_src, w_src = src_u8.shape[:2]
        h_ref, w_ref = ref_u8.shape[:2]

        scale_src = min(1.0, self.max_dim / max(h_src, w_src))
        scale_ref = min(1.0, self.max_dim / max(h_ref, w_ref))

        new_w_src = int(round(w_src * scale_src / 8.0) * 8)
        new_h_src = int(round(h_src * scale_src / 8.0) * 8)
        new_w_ref = int(round(w_ref * scale_ref / 8.0) * 8)
        new_h_ref = int(round(h_ref * scale_ref / 8.0) * 8)

        # Ensure non-zero
        new_w_src = max(64, new_w_src)
        new_h_src = max(64, new_h_src)
        new_w_ref = max(64, new_w_ref)
        new_h_ref = max(64, new_h_ref)

        rs_src = cv2.resize(src_u8, (new_w_src, new_h_src), interpolation=cv2.INTER_AREA)
        rs_ref = cv2.resize(ref_u8, (new_w_ref, new_h_ref), interpolation=cv2.INTER_AREA)

        t_src = torch.from_numpy(rs_src).float()[None, None] / 255.0
        t_ref = torch.from_numpy(rs_ref).float()[None, None] / 255.0
        t_src = t_src.to(self.device)
        t_ref = t_ref.to(self.device)

        input_dict = {"image0": t_src, "image1": t_ref}

        with torch.no_grad():
            corr = self._matcher(input_dict)
            kpts0 = corr["keypoints0"].cpu().numpy()
            kpts1 = corr["keypoints1"].cpu().numpy()
            confs = corr["confidence"].cpu().numpy()

        # Rescale keypoint coordinates back to original image space
        if len(kpts0) > 0:
            scale_x0 = w_src / float(new_w_src)
            scale_y0 = h_src / float(new_h_src)
            scale_x1 = w_ref / float(new_w_ref)
            scale_y1 = h_ref / float(new_h_ref)

            kpts0[:, 0] *= scale_x0
            kpts0[:, 1] *= scale_y0
            kpts1[:, 0] *= scale_x1
            kpts1[:, 1] *= scale_y1

        runtime = time.perf_counter() - t0
        return MatchResult(
            keypoints_src=kpts0.astype(np.float32),
            keypoints_ref=kpts1.astype(np.float32),
            confidence=confs.astype(np.float32),
            method_name=self.name,
            runtime_sec=runtime,
            num_raw_matches=len(kpts0),
            success=len(kpts0) >= 4,
            error_message="" if len(kpts0) >= 4 else "Insufficient LoFTR correspondences.",
        )
