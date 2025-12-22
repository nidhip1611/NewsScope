# NewsScope

**Schema-Grounded Cross-Domain News Claim Extraction with Open Models**

[![arXiv](https://img.shields.io/badge/arXiv-TBD-b31b1b.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## Overview

NewsScope is a cross-domain news claim extraction system that:
- Extracts structured claims from news articles using a strict JSON schema
- Fine-tunes LLaMA 3.1 8B with LoRA for **89.4% human-evaluated accuracy**
- Achieves competitive performance with GPT-4o-mini (93.7%) at **~$15 total cost**
- Includes a numeric grounding filter that improves accuracy to **91.6%**

> **Note:** Accuracy is computed on verifiable claims only (excluding UNCLEAR labels). See [Evaluation](#evaluation) for details.

**Key Finding:** The accuracy gap between our open model and GPT-4o-mini is **not statistically significant** (unpaired bootstrap, p=0.07, 95% CI includes 0).

## Results

| Model | Accuracy | Contradiction Rate | Decisiveness |
|-------|----------|-------------------|--------------|
| GPT-4o-mini | 93.7% | 1.0% | 87.5% |
| NewsScope | 89.4% | 2.5% | 85.0% |
| NewsScope + Filter | **91.6%** | 2.0% | 83.0% |

**Statistical Test:** Unpaired bootstrap over human-labeled claims (10,000 resamples) yields a 95% CI of [-1.51, 10.15] percentage points, which includes 0 (p=0.07, one-tailed). The observed difference is not statistically significant at α=0.05.

### Domain Performance

| Domain | NewsScope | GPT-4o-mini | Winner |
|--------|-----------|-------------|--------|
| Politics | **94.3%** | 87.8% | NewsScope (+6.5%) |
| Health | 88.9% | 95.5% | GPT-4o-mini |
| Science/Env | 95.5% | 98.0% | GPT-4o-mini |
| Business | 80.4% | 92.7% | GPT-4o-mini |

## Quick Start

### Installation
```bash
git clone https://github.com/nidhip1611/newsscope.git
cd newsscope
pip install -r requirements.txt
```

> **LLaMA License Required:** You must accept the [LLaMA license on Hugging Face](https://huggingface.co/meta-llama/Meta-Llama-3.1-8B-Instruct) before using the model. Then either:
> - Run huggingface-cli login and enter your token, OR
> - Set the HF_TOKEN environment variable


### Inference
```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch

# Load base model
base_model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Meta-Llama-3.1-8B-Instruct",
    torch_dtype=torch.float16,
    device_map="auto"
)

# Load LoRA adapter
model = PeftModel.from_pretrained(base_model, "nidhipandya/NewsScope-lora")
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3.1-8B-Instruct")

# Extract claims from article
article = "Your news article text here..."
prompt = f"""Extract structured claims from this news article.
Return valid JSON with: domain, headline, key_points, whos_involved, how_it_unfolded, claims.

Article:
{article}

JSON Output:"""

inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=2000, temperature=0.3)
result = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(result)
```

## Dataset

### Statistics

| Split | Articles | Purpose |
|-------|----------|---------|
| Training | 315 | Model training |
| In-domain Test | 80 | In-domain evaluation |
| Out-of-source Test | 60 | Generalization evaluation |

### Domains

- **Politics** (88 articles): NPR Politics, BBC News
- **Health** (100 articles): FDA News, NPR Health  
- **Science/Environment** (103 articles): NASA, Science Daily
- **Business** (104 articles): Yahoo Finance, BBC Business

### Schema

Each article is annotated with:
- `domain`: Category classification (politics, health, science_env, business)
- `headline`: Neutral headline (10-200 characters)
- `key_points`: 3 main takeaways
- `whos_involved`: List of `{name, role}` for entities mentioned
- `how_it_unfolded`: List of `{date, event}` for timeline
- `claims`: List of `{claim_text, evidence_from_article}` for verifiable claims

### Download

Download the benchmark from [GitHub Releases](https://github.com/nidhip1611/NewsScope/releases/tag/v1.0.0):

1. Download `benchmark.zip`
2. Extract to `data/benchmark/`

The benchmark includes annotations and article URLs only (no full text due to copyright).

> **Copyright Note:** We release annotations and article URLs only (no full text) to respect copyright. Evidence snippets are kept brief (<100 words) for fair use.

## Evaluation

### Metrics

- **Accuracy**: SUPPORTED / (SUPPORTED + CONTRADICTED + MIXED) — computed on verifiable claims only
- **Contradiction Rate**: CONTRADICTED / total evaluated claims
- **Decisiveness**: 1 - (UNCLEAR / total)

### Human Evaluation

We evaluated 400 claims (200 per model) with labels:
- **SUPPORTED**: Claim matches article
- **CONTRADICTED**: Claim conflicts with article
- **MIXED**: Partially supported
- **UNCLEAR**: Cannot determine from article

### Inter-Annotator Agreement

| Study | Claims | Agreement | Cohen's κ |
|-------|--------|-----------|-----------|
| Random Subset | 80 | 75.0% | 0.36 |
| Hard Negatives | 80 | 57.5% | 0.26 |

**Positive agreement on SUPPORTED judgments: 94.6%** (indicates high reliability for the primary accuracy component)

> **Note on automatic metrics:** Semantic similarity and Claims@0.75 measure agreement with silver references generated by GPT-4o-mini. They evaluate structural/teacher agreement rather than factual correctness. Human evaluation is the ground-truth metric reported in the paper.

## Numeric Grounding Filter

Improves accuracy by catching ungrounded numbers in claims:
```python
from newsscope.filter import NumericGroundingFilter

filter = NumericGroundingFilter()
claim = "The company reported 15% growth"
article = "The company reported 10% growth last quarter"

is_grounded, ungrounded = filter.check(claim, article)
# is_grounded = False, ungrounded = ["15%"]
```

**Filter Performance:**
- Catches 22.2% of errors (4/18)
- Improves accuracy: 89.4% → 91.6% (+2.2 points)
- Business domain: 80.4% → 86.0% (+5.6 points)

## Repository Structure
```
newsscope/
├── README.md
├── requirements.txt
├── CITATION.cff
├── LICENSE
├── newsscope/
│   ├── __init__.py
│   ├── schema.py
│   ├── validator.py
│   ├── filter.py
│   └── prompts.py
├── scripts/
│   ├── run_inference.py
│   ├── run_eval.py
│   └── run_training.py
├── data/
│   └── benchmark/
│       ├── README.md
│       ├── train.jsonl
│       ├── test_indomain.jsonl
│       └── test_oos.jsonl
└── paper/
    ├── main_standalone.tex
    └── references.bib
```

## Training

### Requirements
- GPU with 16GB+ VRAM (or Google Colab free tier with T4)
- ~57 minutes training time

### Configuration
```python
# LoRA Configuration
lora_config = LoraConfig(
    r=16,
    lora_alpha=16,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", 
                    "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)
```

See `scripts/run_training.py` for full training code.

## Citation
```bibtex
@article{pandya2025newsscope,
  title={NewsScope: Schema-Grounded Cross-Domain News Claim Extraction with Open Models},
  author={Pandya, Nidhi},
  journal={arXiv preprint},
  year={2025}
}
```

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- Meta AI for LLaMA 3.1
- Hugging Face for transformers and PEFT libraries
- Google Colab for free GPU access

## Contact

- **Author:** Nidhi Pandya
- **Email:** nidhipandya1606@gmail.com
- **GitHub:** [@nidhip1611](https://github.com/nidhip1611)
