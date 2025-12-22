#!/usr/bin/env python3
"""
NewsScope Inference Script

Extracts structured claims from a news article.

PREREQUISITES:
    1. Accept LLaMA license: https://huggingface.co/meta-llama/Meta-Llama-3.1-8B-Instruct
    2. Login to HuggingFace: huggingface-cli login
       OR set HF_TOKEN environment variable

Usage:
    python scripts/run_inference.py --article "Your article text here"
    python scripts/run_inference.py --file article.txt
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def load_model(model_path: str = "nidhip1611/newsscope-lora"):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import PeftModel
    
    print("Loading base model...")
    base_model = AutoModelForCausalLM.from_pretrained(
        "meta-llama/Meta-Llama-3.1-8B-Instruct",
        torch_dtype=torch.float16,
        device_map="auto"
    )
    
    print(f"Loading LoRA adapter from {model_path}...")
    model = PeftModel.from_pretrained(base_model, model_path)
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3.1-8B-Instruct")
    
    return model, tokenizer


def extract_claims(model, tokenizer, article: str) -> dict:
    from newsscope.prompts import get_chat_messages
    from newsscope.validator import validate_output
    
    messages = get_chat_messages(article)
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    outputs = model.generate(
        **inputs,
        max_new_tokens=2000,
        temperature=0.3,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id
    )
    
    input_length = inputs["input_ids"].shape[1]
    result = tokenizer.decode(outputs[0][input_length:], skip_special_tokens=True)
    
    is_valid, parsed, errors = validate_output(result)
    
    if is_valid and parsed:
        return parsed
    else:
        return {"error": "Failed to parse", "raw_output": result[:500]}


def main():
    parser = argparse.ArgumentParser(description="NewsScope Inference")
    parser.add_argument("--article", type=str, help="Article text")
    parser.add_argument("--file", type=str, help="Path to article file")
    parser.add_argument("--model", type=str, default="nidhip1611/newsscope-lora")
    parser.add_argument("--output", type=str, help="Path to save JSON")
    args = parser.parse_args()
    
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            article = f.read()
    elif args.article:
        article = args.article
    else:
        print("Error: Provide --article or --file")
        return
    
    model, tokenizer = load_model(args.model)
    result = extract_claims(model, tokenizer, article)
    print(json.dumps(result, indent=2))
    
    if args.output:
        with open(args.output, "w") as f:
            json.dump(result, f, indent=2)


if __name__ == "__main__":
    main()
