# NewsScope Benchmark Dataset

## Overview

This benchmark contains structured annotations for 395 news articles across 4 domains, designed for evaluating news claim extraction systems.

## Important Copyright Notice

**This release contains annotations and article URLs only, NOT full article text.**

To respect copyright:
- We provide article URLs for you to fetch the original content
- Annotations (claims, entities, timelines) are our original work
- Evidence snippets are kept brief (<100 words) for fair use
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
    "whos_involved": [
      {"name": "Person Name", "role": "Title/Role"}
    ],
    "how_it_unfolded": [
      {"date": "2025-01-15", "event": "Description"}
    ],
    "claims": [
      {
        "claim_text": "Verifiable statement",
        "evidence_from_article": "Supporting text from article"
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

## License

- **Annotations:** MIT License (our original work)
- **Article content:** Property of original publishers (not included)

## Citation
```bibtex
@article{pandya2025newsscope,
  title={NewsScope: Schema-Grounded Cross-Domain News Claim Extraction with Open Models},
  author={Pandya, Nidhi},
  journal={arXiv preprint},
  year={2025}
}
```
