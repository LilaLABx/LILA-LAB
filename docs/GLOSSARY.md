# LILA Lab Glossary

Domain terms used across economics, NLP, and pipeline docs. Look up jargon here before opening an issue or PR.

## Economic Terms

| Term | Definition |
|------|------------|
| **BDT/USD** | Bangladesh Taka per US Dollar exchange rate — a key macro indicator for Bangla economic news validation. |
| **CPI** | Consumer Price Index — measures inflation; BENI index is validated against monthly CPI movements. |
| **Confidence (annotation)** | Annotator or model certainty (0–1) that a label is correct; low-confidence items go to human review. |
| **Economic relevance** | Binary or scored label: does this article discuss economic topics (inflation, trade, employment, etc.)? |
| **Fiscal policy** | Government spending and taxation decisions tracked in economic news narratives. |
| **FX** | Foreign exchange — currency rates, especially BDT/USD in the Bangla context. |
| **Inflation nowcasting** | Estimating current-month inflation from real-time news signals before official CPI is published. |
| **Monetary policy** | Central bank actions (interest rates, money supply) reflected in economic news. |
| **Narrative force** | Qualitative tone of an article: crisis, reform, stability, uncertainty, resilience, etc. |
| **Narrative index** | Monthly time series built from aggregated economic news sentiment and topic signals (e.g. BENI). |
| **Remittances** | Money sent home by overseas workers — a major Bangladesh economic indicator. |
| **Reserves** | Foreign currency reserves held by the central bank. |
| **Sentiment** | Positive, negative, or neutral tone of economic coverage in an article. |
| **Valuation target** | What economic variable an article implicitly discusses (inflation, FX, growth, etc.). |

## NLP / ML Terms

| Term | Definition |
|------|------------|
| **Active learning** | Iteratively selecting the most uncertain articles for human labeling to maximize model improvement per label. |
| **Adjudication** | Resolving disagreements between multiple LLM or human annotators on the same article. |
| **BanglaBERT** | Pre-trained Bangla language model used for article classification in BENI. |
| **BERT** | Bidirectional Encoder Representations from Transformers — foundation for BanglaBERT and similar models. |
| **Ensemble** | Combining predictions from multiple models or LLMs (e.g. Claude + GPT-4o) for robust labels. |
| **F1 score** | Harmonic mean of precision and recall; primary metric for economic relevance classification. |
| **Gold standard** | Human-verified reference labels used to train and evaluate models. |
| **LLM annotation** | Using large language models (Claude, GPT-4o) to label articles via structured prompts. |
| **Logistic regression** | Simple supervised classifier often paired with TF-IDF features in BENI experiments. |
| **Narrative force** | (ML context) Multi-class label capturing the emotional/policy tone of economic reporting. |
| **Precision** | Of predicted economic articles, what fraction are truly economic? |
| **Recall** | Of all truly economic articles, what fraction did the model find? |
| **Reference set** | Curated labeled articles used as a benchmark for model comparison. |
| **TF-IDF** | Term Frequency–Inverse Document Frequency — bag-of-words features for text classification. |
| **Tokenization** | Splitting Bangla (or other) text into units for model input. |

## Pipeline / Project Terms

| Term | English | বাংলা |
|------|---------|-------|
| **Annotation schema** | JSON fields an annotator fills per article (relevance, topic, sentiment, etc.) | অ্যানোটেশন স্কিমা |
| **BENI** | Bangla Exploration & Native-language Intelligence — the proven Bangla pipeline | বেনি |
| **AENI** | Assamese Exploration & Native-language Intelligence | এএনআই |
| **NENI** | Nepali Exploration & Native-language Intelligence | নেএনআই |
| **SENI** | Sylheti Exploration & Native-language Intelligence | সেএনআই |
| **CENI** | Chittagonian Exploration & Native-language Intelligence | সেএনআই (চিটাইঙ্গা) |
| **ENI suffix** | Exploration & Native-language Intelligence — shared suffix for all XENI pipelines | ইএনআই |
| **Gold standard** | Human-verified labels that models are trained and evaluated against | গোল্ড স্ট্যান্ডার্ড |
| **Index construction** | Building a monthly narrative index from classified articles | সূচক নির্মাণ |
| **Label Studio** | Open-source annotation UI used for human review workflows | লেবেল স্টুডিও |
| **OWNERS.csv** | Contributor registry — who worked on what, for credit and acknowledgements | ওনার্স.সিএসভি |
| **Potrika corpus** | Bangla news corpus used as a primary data source for BENI | পত্রিকা কর্পাস |
| **BNAD** | Bangla NLP Annotation Dataset — community annotation effort | বিএনএডি |
| **XENI** | [Language initial] + Exploration & Native-language Intelligence framework | জেনি |

## See Also

- [CONTRIBUTOR_QUICKSTART.md](CONTRIBUTOR_QUICKSTART.md) — five-minute onboarding
- [PIPELINE_FLOW.md](PIPELINE_FLOW.md) — visual pipeline stages
- [LINGUISTIC_CONTRIBUTION_GUIDE.md](../LINGUISTIC_CONTRIBUTION_GUIDE.md) — how to contribute language data