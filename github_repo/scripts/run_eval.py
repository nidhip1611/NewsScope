#!/usr/bin/env python3
"""
NewsScope Evaluation Script

NOTE: Benchmark JSONLs are distributed via GitHub Releases, not committed to the repo.
Download benchmark.zip from Releases and extract to data/benchmark/.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def check_exists(p: str) -> bool:
    if Path(p).exists():
        return True
    print("")
    print("ERROR: Benchmark file not found:", p)
    print("")
    print("The benchmark data is distributed via GitHub Releases.")
    print("To get it:")
    print("  1. Go to: https://github.com/nidhip1611/newsscope/releases")
    print("  2. Download: benchmark.zip")
    print("  3. Extract to: data/benchmark/")
    print("")
    return False


def load_jsonl(path: str) -> list:
    out = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def main():
    parser = argparse.ArgumentParser(description="NewsScope Evaluation")
    parser.add_argument("--predictions", required=True, help="Predictions JSONL")
    parser.add_argument("--benchmark", required=True, help="Benchmark JSONL (from Releases)")
    args = parser.parse_args()

    if not check_exists(args.benchmark):
        return
    if not Path(args.predictions).exists():
        print("ERROR: Predictions file not found:", args.predictions)
        return

    refs = load_jsonl(args.benchmark)
    preds = load_jsonl(args.predictions)

    print(f"Loaded references: {len(refs)}")
    print(f"Loaded predictions: {len(preds)}")
    print("")
    print("This script is a lightweight placeholder.")
    print("Extend with your preferred evaluation metrics.")


if __name__ == "__main__":
    main()
