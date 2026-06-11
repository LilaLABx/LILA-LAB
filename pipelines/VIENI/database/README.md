# Database

## Purpose

Structured storage for article metadata, annotations, model predictions, and index values. Enables reproducible querying and analysis without reloading raw files.

## Schema (SQLite Reference)

```
articles
├── id              TEXT PRIMARY KEY    # Unique article identifier
├── source          TEXT                # Newspaper/source name
├── date            DATE                # Publication date
├── title           TEXT                # Article title
├── text_hash       TEXT                # Deduplication hash
├── domain_labels   JSON                # Per-domain annotation labels
└── created_at      TIMESTAMP           # Ingestion timestamp

predictions
├── id              TEXT PRIMARY KEY
├── article_id      TEXT → articles.id
├── model_type      TEXT                # tfidf, bert, ensemble
├── domain          TEXT                # eco, health, ...
├── label           TEXT                # Predicted label
├── probability     FLOAT               # Prediction confidence
└── created_at      TIMESTAMP

indices
├── id              TEXT PRIMARY KEY
├── domain          TEXT                # eco, health, ...
├── year_month      TEXT                # YYYY-MM
├── value           FLOAT               # Index value
├── lower_ci        FLOAT               # Confidence interval
├── upper_ci        FLOAT
└── created_at      TIMESTAMP
```

## Instructions

1. Choose your database engine (SQLite recommended for single-pipeline, PostgreSQL for multi-language)
2. Implement the database creation script
3. Set up ETL pipelines from raw data → articles → predictions → indices
4. Document schema migrations for versioning

## Deliverable

- Populated database with articles, annotations, predictions, and indices
- Database creation/migration scripts
- Query examples for common analysis tasks
