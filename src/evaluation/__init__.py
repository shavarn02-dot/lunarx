"""
Evaluation and benchmarking package.
"""
from src.evaluation.metrics import (
    RegistrationQualityReport,
    compute_photometric_consistency,
)
from src.evaluation.benchmark import (
    run_benchmark_on_pair,
    export_benchmark_results,
)

__all__ = [
    "RegistrationQualityReport",
    "compute_photometric_consistency",
    "run_benchmark_on_pair",
    "export_benchmark_results",
]
