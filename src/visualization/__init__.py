"""
Visualization modules: Match plotting, spatial grid overlays, and before/after composite tools.
"""
from src.visualization.matches import draw_correspondences, draw_spatial_grid_overlay
from src.visualization.overlays import (
    create_checkerboard_overlay,
    create_difference_heatmap,
    create_split_slider_composite,
)

__all__ = [
    "draw_correspondences",
    "draw_spatial_grid_overlay",
    "create_checkerboard_overlay",
    "create_difference_heatmap",
    "create_split_slider_composite",
]
