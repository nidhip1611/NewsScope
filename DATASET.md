# NewsScope Dataset

## Overview

NewsScope contains **455 news articles** for claim extraction evaluation:
- **395 in-domain articles** across 4 domains
- **60 out-of-source articles** for generalization testing

## Dataset Statistics

| Split | Articles | Description |
|-------|----------|-------------|
| Training | 315 | For model fine-tuning |
| In-domain Test | 80 | Same sources as training |
| Out-of-source Test | 60 | New sources for generalization |
| **Total** | **455** | |

## Domain Distribution

| Domain | Articles |
|--------|----------|
| Politics | 88 |
| Health | 100 |
| Science/Environment | 103 |
| Business | 104 |
| **Total** | **395** |

## Data Release

**Benchmark JSONL files are distributed via GitHub Releases (not committed to the repo).**

### What We Release
- Article URLs
- Metadata (domain, source)
- Our annotations (headline, key_points, entities, timeline, claims)

### What We Do NOT Release
- Full article text (copyrighted by publishers)

### How to Get the Benchmark
1. Go to GitHub Releases
2. Download benchmark.zip
3. Extract into data/benchmark/

## Training Data

Training requires **full article text**, which is not publicly released.

To reproduce training:
1. Fetch article text using the URLs from the benchmark
2. Create data/private/train_with_text.jsonl with fields: article_id, article_text, annotation
3. Run: python scripts/run_training.py --data data/private/train_with_text.jsonl

## Schema

Each annotation contains:
- article_id: unique identifier
- url: article URL
- domain: politics, health, science_env, or business
- source: source name
- annotation object with:
  - domain
  - headline (10-200 chars)
  - key_points (exactly 3)
  - whos_involved (list of name/role pairs)
  - how_it_unfolded (list of date/event pairs)
  - claims (2-3 items with claim_text and evidence_from_article)

## Citation

Update arXiv ID after submission:

    @article{pandyaNewsscope,
      title={NewsScope: Schema-Grounded Cross-Domain News Claim Extraction with Open Models},
      author={Pandya, Nidhi},
      journal={arXiv preprint arXiv:TBD},
      year={TBD}
    }
