# Data

## Purpose

Store raw and processed data for the pipeline. This directory contains the input (raw news articles) and intermediate artifacts (processed, deduplicated, cleaned data).

## Structure

```
data/
├── README.md       # ← You are here
├── raw/            # Raw news articles from scraping/crawling
│   └── .gitkeep
├── processed/      # Cleaned, deduplicated, tokenized articles
│   └── .gitkeep
└── external/       # External data (macro indicators, health stats, etc.)
    └── .gitkeep
```

## Instructions

1. **Raw data**: Place original scraped/crawled news articles here
   - Keep source provenance (newspaper name, crawl date)
   - Document format (JSONL, CSV, etc.)
2. **Processed data**: Cleaned versions after deduplication, date parsing, text normalization
   - One file per processing stage
   - Document all transformations applied
3. **External data**: Real-world indicators for validation
   - CPI, exchange rates, reserves (for economic indices)
   - Disease incidence, vaccination rates (for health indices)
   - Always cite the original source

## Data Policy

- **Full article text**: Subject to upstream corpus terms. Do not redistribute without permission.
- **Derived data**: Labels, predictions, and indices are CC BY 4.0.
- **Large files**: Use Git LFS or store externally (Zenodo, OSF) with pointers here.

## Deliverable

- Clean, deduplicated article corpus ready for annotation
- External validation data with provenance documented
- Data processing scripts in `infrastructure/scripts/`
