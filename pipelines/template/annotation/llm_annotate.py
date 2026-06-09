#!/usr/bin/env python3
"""
[X]ENI — LLM Annotation Script

Multi-LLM annotation pipeline for native-language news articles.
Adapt this file for your language: configure models, prompts, and API keys.

Usage:
    python llm_annotate.py --input data/articles.jsonl --schema schemas/economic.json --output annotations/

Deliverable:
    - Annotated articles with per-field labels and confidence scores
    - Ready for adjudication and classifier training
"""

import argparse
import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_schema(schema_path: str) -> dict:
    with open(schema_path) as f:
        return json.load(f)


def load_articles(input_path: str) -> list[dict]:
    """Load articles from JSONL file."""
    articles = []
    with open(input_path) as f:
        for line in f:
            articles.append(json.loads(line))
    return articles


def annotate_article(article: dict, schema: dict) -> dict:
    """
    Annotate a single article using LLM ensemble.

    TODO: Implement multi-LLM annotation for your language.
    - Configure Claude, GPT-4o, or local model APIs
    - Design prompt templates using the schema
    - Handle your language's script and tokenization
    """
    raise NotImplementedError("Implement LLM annotation for your language")


def main():
    parser = argparse.ArgumentParser(description="LLM Annotation Pipeline")
    parser.add_argument("--input", required=True, help="Input JSONL file")
    parser.add_argument("--schema", required=True, help="Annotation schema JSON")
    parser.add_argument("--output", default="annotations/", help="Output directory")
    args = parser.parse_args()

    schema = load_schema(args.schema)
    articles = load_articles(args.input)
    logger.info(f"Loaded {len(articles)} articles, schema: {schema['domain']}")

    # TODO: Implement batch annotation loop
    # for article in articles:
    #     result = annotate_article(article, schema)
    #     save_result(result, args.output)

    logger.info("Annotation complete. Deliverable: labeled dataset ready for adjudication.")


if __name__ == "__main__":
    main()
