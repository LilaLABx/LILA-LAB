# Public Data Sources for Extending BENI Beyond 2020

This note records public datasets found for extending BENI after the Potrika 2014-2020 period.

## Recommended Main Extension Source

### BNAD: Bangla News Article Dataset

Repository:

- https://zenodo.org/records/11111869

DOI:

- `10.5281/zenodo.11111869`

Paper:

- https://doi.org/10.1016/j.dib.2024.110874

Why it matters:

- 1.9M+ Bangla news articles.
- Nine Bangla news websites.
- JSONL format.
- Includes categories such as economy, politics, local news, technology, education, health, arts, sports, and others.
- Published in 2024 and described as an updated dataset relative to Potrika.
- CC BY 4.0 on Zenodo.

Files:

- `AjkerPatrika.jsonl`
- `BanglaTribune.jsonl`
- `DailyInqilab.jsonl`
- `DhakaTribuneBangla.jsonl`
- `ekattorTv.jsonl`
- `ittefaq.jsonl`
- `JanaKantha.jsonl`
- `ManabZamin.jsonl`
- `Samakal.jsonl`
- `category.txt`
- `source code.zip`

Direct file pattern:

```text
https://zenodo.org/records/11111869/files/<FILENAME>?download=1
```

Examples:

```text
https://zenodo.org/records/11111869/files/AjkerPatrika.jsonl?download=1
https://zenodo.org/records/11111869/files/BanglaTribune.jsonl?download=1
https://zenodo.org/records/11111869/files/DailyInqilab.jsonl?download=1
https://zenodo.org/records/11111869/files/DhakaTribuneBangla.jsonl?download=1
https://zenodo.org/records/11111869/files/ekattorTv.jsonl?download=1
https://zenodo.org/records/11111869/files/ittefaq.jsonl?download=1
https://zenodo.org/records/11111869/files/JanaKantha.jsonl?download=1
https://zenodo.org/records/11111869/files/ManabZamin.jsonl?download=1
https://zenodo.org/records/11111869/files/Samakal.jsonl?download=1
https://zenodo.org/records/11111869/files/category.txt?download=1
```

BENI use:

- Best candidate for BENI v2 extension.
- Use only records with parseable publication dates after 2020.
- Prioritize economy/finance/business categories and macro-relevant national/politics categories.
- Deduplicate against Potrika before merging, especially for Ittefaq and Inqilab.

Important caveat:

- This dataset likely extends the BENI time window beyond 2020, but its exact latest article date must be verified by parsing the `Time` field in each JSONL file.

## Smaller or Specialized Sources

### BARD Corpus

Repository:

- https://data.mendeley.com/datasets/ntg3m8mw8d/1

DOI:

- `10.17632/ntg3m8mw8d.1`

Notes:

- Published 2025.
- 2,500 Bangla news articles.
- Five balanced classes, including Economy.
- Sources include Prothom Alo, Jugantor, Ittefaq, Bdnews24, Kaler Kantho, Bangla Tribune, and Samakal.
- Useful for model testing or external validation, not enough for time-series extension.

### BanFakeNews-2.0

Repository:

- https://data.mendeley.com/datasets/kjh887ct4j/1

DOI:

- `10.17632/kjh887ct4j.1`

Notes:

- Published 2024.
- Around 47,000 authentic Bangla news articles plus 13,000 fake news articles.
- Useful only as auxiliary text/classification data unless timestamps and sources are usable.

### BEN-FND

Repository:

- https://data.mendeley.com/datasets/cxxpmb8ykh/1

DOI:

- `10.17632/cxxpmb8ykh.1`

Notes:

- Published 2025.
- 16,349 Bangla and English fake/real news samples.
- Includes title, article text/summary, language, category, and label.
- CC0 for curation, but original text remains publisher-owned.
- Useful for auxiliary classification robustness, not a primary BENI time-series source.

### BengaliNewspaperCommonCoverageArticleDataset

Repository:

- https://data.mendeley.com/datasets/msmhb5fmf6/1

DOI:

- `10.17632/msmhb5fmf6.1`

Notes:

- Published 2025.
- 1,056 common articles across five Bangladeshi newspapers.
- Includes dates, URLs, headlines, and descriptions.
- Useful for source-bias or framing comparison, not enough for macro time-series extension.

## Recommendation

For BENI extension, use this sequence:

1. Keep Potrika 2014-2020 as BENI v1.0.
2. Use BNAD as the main BENI v2 extension source.
3. Parse BNAD dates and identify actual coverage after 2020.
4. Build a source/category/date coverage table before merging.
5. Only after that, decide whether live scraping is needed for 2024-2026 gaps.

