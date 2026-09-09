"""
SuperPoint + LightGlue Learned Keypoint Matching.
SIH26166 Compliant.
"""
import time
from typing import Optional, Dict, Any
import numpy as np
import logging

from src.matching.base import BaseMatcher, MatchResult

logger = logging.getLogger(__name__)


class SuperPointLightGlueMatcher(BaseMatcher):
    def __init__(self, params: Optional[Dict[str, Any]] = None):
        super().__init__("SuperPoint+LightGlue", params)
        self.max_keypoints = self.params.get("max_num_keypoints", 1024)
        self.device = "cpu"
        self._initialized = False
        self._extractor = None
        self._matcher = None

    def _lazy_init(self):
        if self._initialized:
            return
        import torch
        from lightglue import LightGlue, SuperPoint
        from lightglue.utils import rbd

        self.torch = torch
        self.rbd = rbd
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        logger.info(f"Initializing SuperPoint + LightGlue on {self.device}...")
        self._extractor = SuperPoint(max_num_keypoints=self.max_keypoints).eval().to(self.device)
        self._matcher = LightGlue(features="superpoint", depth_confidence=-1, width_confidence=-1).eval().to(self.device)
        self._initialized = True

    def match(self, src_u8: np.ndarray, ref_u8: np.ndarray) -> MatchResult:
        t0 = time.perf_counter()
        try:
            self._lazy_init()
        except Exception as e:
            runtime = time.perf_counter() - t0
            logger.error(f"Failed to load SuperPoint/LightGlue: {e}")
            return MatchResult(
                keypoints_src=np.empty((0, 2), dtype=np.float32),
                keypoints_ref=np.empty((0, 2), dtype=np.float32),
                confidence=np.empty((0,), dtype=np.float32),
                method_name=self.name,
                runtime_sec=runtime,
                num_raw_matches=0,
                success=False,
                error_message=f"Model initialization error: {e}",
            )

        import torch

        # Normalize images to float tensor (1, 1, H, W) in [0.0, 1.0]
        t_src = torch.from_numpy(src_u8).float()[None, None] / 255.0
        t_ref = torch.from_numpy(ref_u8).float()[None, None] / 255.0
        t_src = t_src.to(self.device)
        t_ref = t_ref.to(self.device)

        with torch.no_grad():
            feats_src = self._extractor.extract(t_src)
            feats_ref = self._extractor.extract(t_ref)

            num_raw = int(feats_src["keypoints"].shape[1])
            matches_data = self._matcher({"image0": feats_src, "image1": feats_ref})

            feats_src_b, feats_ref_b, matches_b = (
                self.rbd(feats_src),
                self.rbd(feats_ref),
                self.rbd(matches_data),
            )

            kpts0 = feats_src_b["keypoints"]  # (N, 2)
            kpts1 = feats_ref_b["keypoints"]  # (M, 2)
            matches = matches_b["matches"]    # (K, 2)
            scores = matches_b.get("scores", torch.ones(len(matches)))

            if len(matches) > 0:
                m_kpts0 = kpts0[matches[..., 0]].cpu().numpy()
                m_kpts1 = kpts1[matches[..., 1]].cpu().numpy()
                confs = scores.cpu().numpy()
            else:
                m_kpts0 = np.empty((0, 2), dtype=np.float32)
                m_kpts1 = np.empty((0, 2), dtype=np.float32)
                confs = np.empty((0,), dtype=np.float32)

        runtime = time.perf_counter() - t0
        return MatchResult(
            keypoints_src=m_kpts0.astype(np.float32),
            keypoints_ref=m_kpts1.astype(np.float32),
            confidence=confs.astype(np.float32),
            method_name=self.name,
            runtime_sec=runtime,
            num_raw_matches=num_raw,
            success=len(m_kpts0) >= 4,
            error_message="" if len(m_kpts0) >= 4 else "Insufficient LightGlue matches.",
        )
