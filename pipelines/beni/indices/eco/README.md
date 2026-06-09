# BENI Economic Index

## Purpose

The BENI Economic Index measures monthly economic narrative pressure in Bangla news media. This is the first validated XENI index — proven across 79 months (2014–2020).

## Code Location

The actual index construction code lives in the sibling `index/` directory:

```
beni/index/
├── build_narrative_index.py    # Main index builder
├── visualize.py                # Index visualization
└── outputs/                    # Generated index files
```

This directory (`indices/eco/`) exists to align with the canonical XENI template structure. Use `index/` for the actual working code.

## Validation Results

| Indicator | Correlation | Significance |
|-----------|-------------|-------------|
| CPI | r = −0.75 | p < 0.001 |
| Exchange Rate (Taka/USD) | r = −0.72 | p < 0.001 |
| Foreign Reserves | — | In progress |

## Methodology

1. **Filter**: Keep articles classified as economically relevant (label from LLM ensemble)
2. **Score**: Mean prediction probability per month across economic topics
3. **Weight**: Source-balance to prevent dominant newspapers from overwhelming
4. **Validate**: Pearson correlation with macroeconomic indicators
5. **Report**: Monthly index values with confidence intervals

## Deliverable

- Monthly BENI Economic Index CSV (79 months)
- Validation report with macroeconomic correlations
- Published papers (2 submitted, 4 in pipeline)
