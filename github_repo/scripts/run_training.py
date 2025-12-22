#!/usr/bin/env python3
"""
NewsScope Training Script

Training requires full article text (not distributed in the public benchmark).

To prepare training data:
1. Download benchmark from GitHub Releases
2. Fetch article text using the URLs
3. Create: data/private/train_with_text.jsonl
   Each line: {"article_id": "...", "article_text": "...", "annotation": {...}}

Usage:
    python scripts/run_training.py --data data/private/train_with_text.jsonl --output ./newsscope-lora
"""

import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="NewsScope Training")
    parser.add_argument("--data", required=True, help="Training JSONL with article_text field")
    parser.add_argument("--output", default="./newsscope-lora", help="Output directory")
    args = parser.parse_args()

    if not Path(args.data).exists():
        print("")
        print("ERROR: Data file not found:", args.data)
        print("")
        print("Training requires full article text, which is NOT in the public benchmark.")
        print("")
        print("To prepare training data:")
        print("  1. Download benchmark from GitHub Releases")
        print("  2. Fetch article text using the URLs")
        print("  3. Create JSONL with: article_id, article_text, annotation")
        print("  4. Save to: data/private/train_with_text.jsonl")
        print("")
        return

    n = 0
    with open(args.data, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            obj = json.loads(line)
            if "article_text" not in obj:
                raise ValueError("Missing article_text field in training data.")
            n += 1

    print(f"[OK] Found {n} training examples with article_text.")
    print("")
    print("This script validates data format only.")
    print("For full training, use the Colab notebook or extend this script.")
    print("")
    print("Training configuration (from paper):")
    print("  - Base model: meta-llama/Meta-Llama-3.1-8B-Instruct")
    print("  - LoRA rank: 16, alpha: 16")
    print("  - Epochs: 3, batch size: 8, LR: 2e-4")
    print("  - Training time: ~57 min on Tesla T4")


if __name__ == "__main__":
    main()
