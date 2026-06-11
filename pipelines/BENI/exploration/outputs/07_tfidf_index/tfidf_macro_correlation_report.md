# TF-IDF Narrative Index — Macroeconomic Correlation Report

**Period:** 2015-01 — 2024-03  (111 months, 2015+)

**Significant at p<0.01:** 34 / 40  |  **p<0.05:** 34 / 40


## annual

| x | y | n | Pearson r | p | Spearman r | p | Sig |
|---|---|---|---|---|---|---|---|
| economic_share | reserves_usd | 10 | 0.0381 | 0.9167 | -0.1758 | 0.6272 |  |
| tfidf_index | reserves_usd | 10 | 0.0381 | 0.9167 | -0.1758 | 0.6272 |  |

## macro_leads_narrative_1m

| x | y | n | Pearson r | p | Spearman r | p | Sig |
|---|---|---|---|---|---|---|---|
| economic_share_lead1 | fx_bis | 110 | -0.6310 | 0.0000 | -0.7379 | 0.0000 | ** |
| economic_share_lead1 | cpi | 110 | -0.7910 | 0.0000 | -0.7996 | 0.0000 | ** |
| tfidf_index_lead1 | fx_bis | 110 | -0.6310 | 0.0000 | -0.7379 | 0.0000 | ** |
| tfidf_index_lead1 | cpi | 110 | -0.7910 | 0.0000 | -0.7996 | 0.0000 | ** |

## macro_leads_narrative_3m

| x | y | n | Pearson r | p | Spearman r | p | Sig |
|---|---|---|---|---|---|---|---|
| economic_share_lead3 | fx_bis | 108 | -0.6112 | 0.0000 | -0.7263 | 0.0000 | ** |
| economic_share_lead3 | cpi | 108 | -0.7757 | 0.0000 | -0.7824 | 0.0000 | ** |
| tfidf_index_lead3 | fx_bis | 108 | -0.6112 | 0.0000 | -0.7263 | 0.0000 | ** |
| tfidf_index_lead3 | cpi | 108 | -0.7757 | 0.0000 | -0.7824 | 0.0000 | ** |

## macro_leads_narrative_6m

| x | y | n | Pearson r | p | Spearman r | p | Sig |
|---|---|---|---|---|---|---|---|
| economic_share_lead6 | fx_bis | 105 | -0.5821 | 0.0000 | -0.7272 | 0.0000 | ** |
| economic_share_lead6 | cpi | 105 | -0.7635 | 0.0000 | -0.7751 | 0.0000 | ** |
| tfidf_index_lead6 | fx_bis | 105 | -0.5821 | 0.0000 | -0.7272 | 0.0000 | ** |
| tfidf_index_lead6 | cpi | 105 | -0.7635 | 0.0000 | -0.7751 | 0.0000 | ** |

## monthly_diff

| x | y | n | Pearson r | p | Spearman r | p | Sig |
|---|---|---|---|---|---|---|---|
| economic_share_d1 | fx_bis_d1 | 110 | 0.0727 | 0.4505 | 0.0440 | 0.6478 |  |
| economic_share_d1 | cpi_d1 | 110 | 0.0162 | 0.8667 | 0.0565 | 0.5579 |  |
| tfidf_index_d1 | fx_bis_d1 | 110 | 0.0727 | 0.4505 | 0.0440 | 0.6478 |  |
| tfidf_index_d1 | cpi_d1 | 110 | 0.0162 | 0.8667 | 0.0565 | 0.5579 |  |

## monthly_level

| x | y | n | Pearson r | p | Spearman r | p | Sig |
|---|---|---|---|---|---|---|---|
| economic_share | fx_bis | 111 | -0.6417 | 0.0000 | -0.7509 | 0.0000 | ** |
| economic_share | cpi | 111 | -0.7943 | 0.0000 | -0.8039 | 0.0000 | ** |
| tfidf_index | fx_bis | 111 | -0.6417 | 0.0000 | -0.7509 | 0.0000 | ** |
| tfidf_index | cpi | 111 | -0.7943 | 0.0000 | -0.8039 | 0.0000 | ** |

## monthly_level_bbd

| x | y | n | Pearson r | p | Spearman r | p | Sig |
|---|---|---|---|---|---|---|---|
| triple_share | fx_bis | 111 | 0.5768 | 0.0000 | 0.8134 | 0.0000 | ** |
| triple_share | cpi | 111 | 0.7385 | 0.0000 | 0.8137 | 0.0000 | ** |
| beni_index | fx_bis | 111 | 0.5768 | 0.0000 | 0.8134 | 0.0000 | ** |
| beni_index | cpi | 111 | 0.7385 | 0.0000 | 0.8137 | 0.0000 | ** |

## narrative_leads_1m

| x | y | n | Pearson r | p | Spearman r | p | Sig |
|---|---|---|---|---|---|---|---|
| economic_share | fx_bis_lead1 | 110 | -0.6586 | 0.0000 | -0.7609 | 0.0000 | ** |
| economic_share | cpi_lead1 | 110 | -0.8029 | 0.0000 | -0.8031 | 0.0000 | ** |
| tfidf_index | fx_bis_lead1 | 110 | -0.6586 | 0.0000 | -0.7609 | 0.0000 | ** |
| tfidf_index | cpi_lead1 | 110 | -0.8029 | 0.0000 | -0.8031 | 0.0000 | ** |

## narrative_leads_3m

| x | y | n | Pearson r | p | Spearman r | p | Sig |
|---|---|---|---|---|---|---|---|
| economic_share | fx_bis_lead3 | 108 | -0.6869 | 0.0000 | -0.7815 | 0.0000 | ** |
| economic_share | cpi_lead3 | 108 | -0.8056 | 0.0000 | -0.8081 | 0.0000 | ** |
| tfidf_index | fx_bis_lead3 | 108 | -0.6869 | 0.0000 | -0.7815 | 0.0000 | ** |
| tfidf_index | cpi_lead3 | 108 | -0.8056 | 0.0000 | -0.8081 | 0.0000 | ** |

## narrative_leads_6m

| x | y | n | Pearson r | p | Spearman r | p | Sig |
|---|---|---|---|---|---|---|---|
| economic_share | fx_bis_lead6 | 105 | -0.7123 | 0.0000 | -0.7937 | 0.0000 | ** |
| economic_share | cpi_lead6 | 105 | -0.8032 | 0.0000 | -0.8024 | 0.0000 | ** |
| tfidf_index | fx_bis_lead6 | 105 | -0.7123 | 0.0000 | -0.7937 | 0.0000 | ** |
| tfidf_index | cpi_lead6 | 105 | -0.8032 | 0.0000 | -0.8024 | 0.0000 | ** |

## tfidf_vs_bbd

| x | y | n | Pearson r | p | Spearman r | p | Sig |
|---|---|---|---|---|---|---|---|
| tfidf_index | beni_index | 111 | -0.5485 | 0.0000 | -0.5554 | 0.0000 | ** |
| tfidf_index | triple_share | 111 | -0.5485 | 0.0000 | -0.5554 | 0.0000 | ** |

## Summary Statistics

- **Mean TF-IDF economic_share:** 10.7% (range: 4.9% – 19.3%)
- **Mean TF-IDF index:** 100.0 (range: 85.2 – 121.6)
- **Mean CPI (2021=100):** 89.1
- **Mean FX (BDT/USD):** 86.61