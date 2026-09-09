# Real Chandrayaan-2 Registration Benchmark

| Method | Prep | Status | Raw | Inliers | Inlier % | RMSE Coarse (px) | RMSE Refined (px) | Δ RMSE | Spatial Coverage % | Runtime (s) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **sift** | clahe | SUCCESS | 2000 | 1329 | 99.8% | 0.148 | 1.500 | -1.353 | 96.1% | 0.16s |
| **sift** | gradient | SUCCESS | 524 | 287 | 99.0% | 0.229 | 1.722 | -1.493 | 93.2% | 0.11s |
| **sift** | raw | SUCCESS | 828 | 602 | 100.0% | 0.126 | 1.312 | -1.186 | 93.7% | 0.12s |
| **orb** | clahe | SUCCESS | 2000 | 950 | 97.9% | 1.054 | 2.090 | -1.036 | 92.2% | 0.95s |
| **orb** | gradient | SUCCESS | 1737 | 719 | 99.7% | 0.960 | 1.634 | -0.674 | 90.2% | 0.04s |
| **orb** | raw | SUCCESS | 1541 | 714 | 99.0% | 0.899 | 1.741 | -0.842 | 90.8% | 0.04s |
| **superpoint_lightglue** | clahe | SUCCESS | 798 | 601 | 99.8% | 0.837 | 1.617 | -0.780 | 94.2% | 9.94s |
| **superpoint_lightglue** | gradient | SUCCESS | 1024 | 770 | 100.0% | 0.792 | 1.503 | -0.711 | 95.3% | 7.62s |
| **superpoint_lightglue** | raw | SUCCESS | 799 | 583 | 99.5% | 0.894 | 1.798 | -0.904 | 96.0% | 6.71s |
| **loftr** | clahe | SUCCESS | 4683 | 4683 | 100.0% | 0.263 | 1.661 | -1.398 | 94.2% | 6.28s |
| **loftr** | gradient | SUCCESS | 4691 | 4691 | 100.0% | 0.264 | 1.860 | -1.597 | 93.9% | 6.24s |
| **loftr** | raw | SUCCESS | 4682 | 4682 | 100.0% | 0.257 | 1.636 | -1.379 | 94.5% | 6.23s |
