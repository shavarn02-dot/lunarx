# Real Chandrayaan-2 Registration Benchmark

| Method | Prep | Status | Raw | Inliers | Inlier % | RMSE Coarse (px) | RMSE Refined (px) | Δ RMSE | Spatial Coverage % | Runtime (s) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **sift** | clahe | SUCCESS | 2000 | 1329 | 99.8% | 0.148 | 0.148 | +0.000 | 96.1% | 0.16s |
| **sift** | gradient | SUCCESS | 524 | 287 | 99.0% | 0.229 | 0.229 | +0.000 | 93.2% | 0.11s |
| **sift** | raw | SUCCESS | 828 | 602 | 100.0% | 0.126 | 0.126 | +0.000 | 93.7% | 0.12s |
| **orb** | clahe | SUCCESS | 2000 | 950 | 97.9% | 1.054 | 1.054 | +0.000 | 92.2% | 0.95s |
| **orb** | gradient | SUCCESS | 1737 | 719 | 99.7% | 0.960 | 0.960 | +0.000 | 90.2% | 0.04s |
| **orb** | raw | SUCCESS | 1541 | 714 | 99.0% | 0.899 | 0.899 | +0.000 | 90.8% | 0.04s |
| **superpoint_lightglue** | clahe | SUCCESS | 798 | 601 | 99.8% | 0.837 | 0.837 | +0.000 | 94.2% | 9.94s |
| **superpoint_lightglue** | gradient | SUCCESS | 1024 | 770 | 100.0% | 0.792 | 0.792 | +0.000 | 95.3% | 7.62s |
| **superpoint_lightglue** | raw | SUCCESS | 799 | 583 | 99.5% | 0.894 | 0.894 | +0.000 | 96.0% | 6.71s |
| **loftr** | clahe | SUCCESS | 4683 | 4683 | 100.0% | 0.263 | 0.263 | +0.000 | 94.2% | 6.28s |
| **loftr** | gradient | SUCCESS | 4691 | 4691 | 100.0% | 0.264 | 0.264 | +0.000 | 93.9% | 6.24s |
| **loftr** | raw | SUCCESS | 4682 | 4682 | 100.0% | 0.257 | 0.257 | +0.000 | 94.5% | 6.23s |
