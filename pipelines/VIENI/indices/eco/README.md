# Economic Narrative Index

## Purpose

Measure monthly economic narrative pressure in your language's news media. The index tracks how economic topics are discussed, framed, and felt over time.

## Validation Targets

| Indicator | Why | Expected Signal |
|-----------|-----|-----------------|
| CPI (Consumer Price Index) | Inflation narratives should track price changes | Negative correlation (more inflation talk → higher CPI) |
| Exchange Rate (FX) | Currency narratives should mirror market sentiment | Negative correlation |
| Foreign Reserves | Reserve coverage narratives | Positive or negative depending on framing |
| GDP Growth | Growth/investment narratives | Positive correlation |
| Policy Rates | Central bank signal narratives | Mixed |

## Methodology (from BENI)

1. **Filter**: Keep only articles classified as economically relevant
2. **Score**: Average prediction probability per economic topic per month
3. **Weight**: Source-balance to prevent dominant newspapers from overwhelming
4. **Validate**: Pearson/Spearman correlation with macroeconomic indicators
5. **Report**: Document significance levels, lead/lag structure

## Instructions

1. Collect macroeconomic indicator data for your country
2. Align date ranges with your annotated article coverage
3. Implement `build_index.py` following BENI methodology
4. Implement `validate.py` with your chosen indicators
5. Test sensitivity to source weighting, topic inclusion, and aggregation method

## Deliverable

- `{language}_eco_monthly_index.csv` — Monthly index values (2014–2020 minimum recommended)
- `{language}_eco_validation_report.md` — Correlation results with interpretation
- `{language}_eco_figures/` — Time series plots
