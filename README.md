# NewsScope Benchmark Dataset

## Overview

This benchmark contains structured annotations for 395 news articles across 4 domains, designed for evaluating news claim extraction systems.

## Important Copyright Notice

**This release contains annotations and article URLs only, NOT full article text.**

To respect copyright:
- We provide article URLs for you to fetch the original content
- Annotations (claims, entities, timelines) are our original work
- Please comply with each source's terms of service when fetching articles

## Dataset Statistics

| Split | Articles | Purpose |
|-------|----------|---------|
| train.jsonl | 315 | Model training |
| test_indomain.jsonl | 80 | In-domain evaluation |
| test_oos.jsonl | 60 | Out-of-source generalization |

## Domains

| Domain | Train | Test (ID) | Test (OOS) |
|--------|-------|-----------|------------|
| Politics | 70 | 18 | 15 |
| Health | 80 | 20 | 15 |
| Science/Env | 82 | 21 | 15 |
| Business | 83 | 21 | 15 |

## Schema

Each annotation contains:
```json
{
  "article_id": "unique_id",
  "url": "https://...",
  "domain": "politics|health|science_env|business",
  "source": "NPR|BBC|...",
  "annotation": {
    "domain": "politics",
    "headline": "Neutral headline here",
    "key_points": ["point1", "point2", "point3"],
    "entities": [
      {"name": "Person Name", "role": "Title/Role"}
    ],
    "timeline": [
      {"date": "2024-01-15", "event": "Description"}
    ],
    "claims": [
      {
        "claim": "Verifiable statement",
        "evidence": "Supporting text from article"
      }
    ]
  }
}
```

## Usage
```python
import json

# Load training data
with open("train.jsonl", "r") as f:
    train_data = [json.loads(line) for line in f]

# Each item has: article_id, url, domain, source, annotation
for item in train_data[:3]:
    print(f"Domain: {item['domain']}")
    print(f"URL: {item['url']}")
    print(f"Claims: {len(item['annotation']['claims'])}")
```

## Fetching Articles

To reconstruct the full dataset:
```python
import requests

def fetch_article(url):
    # Respect robots.txt and rate limits
    response = requests.get(url, timeout=10)
    return response.text if response.ok else None

# Example
article_text = fetch_article(train_data[0]["url"])
```

**Please be respectful:**
- Add delays between requests (1-2 seconds)
- Check robots.txt for each domain
- Some articles may no longer be available

## Human Evaluation Data

The `human_eval/` folder contains:
- `claims_400.jsonl`: 400 claims evaluated (200 per model)
- `iaa_random.jsonl`: 80 claims for inter-annotator agreement
- `iaa_hard_negatives.jsonl`: 80 hard negative claims

## Citation
```bibtex
@article{pandya2024newsscope,
  title={NewsScope: Schema-Grounded Cross-Domain News Claim Extraction},
  author={Pandya, Nidhi},
  journal={arXiv preprint},
  year={2024}
}
```

## License

Annotations are released under MIT License.
Article content remains property of original publishers.
