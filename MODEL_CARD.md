---
license: mit
language:
- en
library_name: peft
base_model: meta-llama/Meta-Llama-3.1-8B-Instruct
tags:
- llama
- lora
- fact-checking
- claim-extraction
- news
- nlp
datasets:
- custom
metrics:
- accuracy
pipeline_tag: text-generation
---

# NewsScope LoRA Adapter

**Schema-Grounded Cross-Domain News Claim Extraction**

## Model Description

NewsScope is a LoRA adapter for LLaMA 3.1 8B Instruct, fine-tuned to extract structured claims from news articles across 4 domains (politics, health, science/environment, business).

### Key Results

| Metric | NewsScope | GPT-4o-mini |
|--------|-----------|-------------|
| Human-Evaluated Accuracy | 89.4% | 93.7% |
| Schema Validity | 98.8% | 100% |
| Politics Accuracy | **94.3%** | 87.8% |

**Statistical Test:** Unpaired bootstrap (10,000 resamples) yields 95% CI [-1.51, 10.15], p=0.07. The difference is not statistically significant at α=0.05.

> **Note:** Accuracy computed on verifiable claims only (excluding UNCLEAR).

## Training Details

- **Base Model:** meta-llama/Meta-Llama-3.1-8B-Instruct
- **Method:** LoRA (Low-Rank Adaptation)
- **Rank:** 16
- **Alpha:** 16
- **Target Modules:** q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj
- **Training Data:** 315 news articles
- **Epochs:** 3
- **Training Time:** 57 minutes on Tesla T4

## Usage
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
model = PeftModel.from_pretrained(base_model, "nidhip1611/newsscope-lora")
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3.1-8B-Instruct")

# Prepare prompt
article = "Your news article text here..."
prompt = f"""Extract structured information from this news article.
Return valid JSON with: domain, headline, key_points, whos_involved, how_it_unfolded, claims.

Article:
{article}

JSON Output:"""

# Generate
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=2000, temperature=0.3, do_sample=True)
result = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(result)
```

## Output Schema

The model outputs JSON with:
```json
{
  "domain": "politics|health|science_env|business",
  "headline": "Neutral headline (10-200 chars)",
  "key_points": ["point1", "point2", "point3"],
  "whos_involved": [{"name": "Person Name", "role": "Title/Role"}],
  "how_it_unfolded": [{"date": "2025-01-15", "event": "Description"}],
  "claims": [
    {
      "claim_text": "Verifiable statement",
      "evidence_from_article": "Supporting text from article"
    }
  ]
}
```

## Limitations

- **English only:** Trained on US/UK English news sources
- **Numeric precision:** May occasionally misstate numbers (use numeric grounding filter)
- **Business domain:** Lower accuracy (80.4%) compared to other domains
- **No verification:** Extracts claims but does not verify against external sources

## Intended Use

- Fact-checking pipelines
- News analysis and monitoring
- Research on misinformation detection
- Educational purposes

**Not intended for:** Automated content moderation without human review.

## Citation
```bibtex
@article{pandya2025newsscope,
  title={NewsScope: Schema-Grounded Cross-Domain News Claim Extraction with Open Models},
  author={Pandya, Nidhi},
  journal={arXiv preprint},
  year={2025}
}
```

## Links

- **Paper:** [arXiv](https://arxiv.org/abs/TBD)
- **Code:** [GitHub](https://github.com/nidhip1611/newsscope)
- **Author:** [Nidhi Pandya](https://github.com/nidhip1611)
