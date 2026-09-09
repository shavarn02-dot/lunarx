"""
Multi-Algorithm Benchmarking Script on Real Chandrayaan-2 Lunar Imagery.
SIH26166 Compliant — Strictly Real Lunar Data, Zero Mock Numbers.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import logging

from src.evaluation.benchmark import run_benchmark_on_pair, export_benchmark_results

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("LunarBenchmark")


def main():
    parser = argparse.ArgumentParser(description="SIH26166 Multi-Algorithm Lunar Registration Benchmark")
    parser.add_argument("--source", type=str, default="data/raw/ch2_tmc_crater_scene_src.png", help="Path to source image")
    parser.add_argument("--reference", type=str, default="data/raw/ch2_tmc_crater_scene_ref.png", help="Path to reference image")
    parser.add_argument("--output-dir", type=str, default="data/outputs", help="Directory for benchmark outputs")
    parser.add_argument("--methods", nargs="+", default=["sift", "orb", "superpoint_lightglue"], help="Matchers to benchmark")
    parser.add_argument("--preprocessing", nargs="+", default=["clahe", "gradient", "raw"], help="Preprocessing methods to benchmark")

    args = parser.parse_args()

    src_p = Path(args.source)
    ref_p = Path(args.reference)
    out_dir = Path(args.output_dir)

    if not src_p.exists() or not ref_p.exists():
        logger.error(
            f"Real Chandrayaan-2 imagery required. Please provide OHRC/TMC/IIRS data in the documented format. (Missing: {src_p} or {ref_p})"
        )
        sys.exit(1)

    logger.info("================================================================================")
    logger.info("SIH26166: Multi-Algorithm Benchmark on Real Chandrayaan-2 Data")
    logger.info(f"Source:        {src_p}")
    logger.info(f"Reference:     {ref_p}")
    logger.info(f"Methods:       {args.methods}")
    logger.info(f"Preprocessing: {args.preprocessing}")
    logger.info("================================================================================")

    results = run_benchmark_on_pair(
        source_path=src_p,
        reference_path=ref_p,
        methods=args.methods,
        preprocess_methods=args.preprocessing,
        model_type="affine"
    )

    export_benchmark_results(results, output_dir=out_dir, filename_stem="benchmark_results")
    logger.info("Benchmark complete!")


if __name__ == "__main__":
    main()
