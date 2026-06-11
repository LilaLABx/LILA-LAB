# Health Discourse Index

## Purpose

Measure monthly health discourse in your language's news media. Track how health topics are discussed, what narratives dominate, and how coverage correlates with real-world health outcomes.

## Potential Validation Targets

| Indicator | Why | Expected Signal |
|-----------|-----|-----------------|
| Disease incidence rates | Outbreak narratives should track case counts | Correlation during epidemics |
| Vaccination coverage | Vaccine discourse may correlate with uptake | Mixed — depends on narrative valence |
| Healthcare utilization | Access narratives may track hospital visits | Correlation |
| Health budget allocation | Policy narratives may track funding | Lagged correlation |
| Mortality rates | Long-term health outcome trends | Slow-moving |

## Methodology

Follow the same approach as the economic index, adapted for health:

1. **Filter**: Keep articles classified as health-relevant
2. **Score**: Average prediction probability per health topic per month
3. **Weight**: Source-balance as needed
4. **Validate**: Against health outcome indicators
5. **Report**: Significance, lead/lag structure, narrative dominance

## Instructions

1. Identify available health indicator data for your country/region
2. Consult with domain experts on relevant health metrics
3. Implement `build_index.py` following BENI methodology
4. Implement `validate.py` with health outcome data
5. Publish as a cross-domain extension paper

## Deliverable

- `{language}_health_monthly_index.csv` — Monthly discourse index
- `{language}_health_validation_report.md` — Correlation results
- `{language}_health_figures/` — Time series plots
