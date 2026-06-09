#!/usr/bin/env python3
"""Audit Potrika and BNAD schemas for BENI merge planning.

The script streams large files and writes compact JSON/CSV summaries.
It does not create a merged dataset.
"""

from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POTRIKA_DIR = ROOT / "data" / "raw" / "potrika"
BNAD_DIR = ROOT / "data" / "raw" / "bnad"
OUT_DIR = ROOT / "data" / "processed" / "schema_audit"

BN_DIGITS = str.maketrans("০১২৩৪৫৬৭৮৯", "0123456789")
BN_MONTHS = {
    "জানুয়ারি": 1,
    "জানুয়ারি": 1,
    "ফেব্রুয়ারি": 2,
    "ফেব্রুয়ারি": 2,
    "মার্চ": 3,
    "এপ্রিল": 4,
    "মে": 5,
    "জুন": 6,
    "জুলাই": 7,
    "আগস্ট": 8,
    "সেপ্টেম্বর": 9,
    "অক্টোবর": 10,
    "নভেম্বর": 11,
    "ডিসেম্বর": 12,
}


def parse_bangla_date(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    text = text.translate(BN_DIGITS)
    text = re.sub(r"^(প্রকাশ|প্রকাশিত|আপডেট)\s*:\s*", "", text).strip()
    text = text.split("|")[0].strip()
    text = text.replace(",", " ")
    text = re.sub(r"\s+", " ", text)

    iso_match = re.search(r"(20\d{2}|19\d{2})[-/](\d{1,2})[-/](\d{1,2})", text)
    if iso_match:
        y, m, d = map(int, iso_match.groups())
        try:
            return datetime(y, m, d).date().isoformat()
        except ValueError:
            return None

    for month_name, month in BN_MONTHS.items():
        pattern = rf"(\d{{1,2}})\s+{re.escape(month_name)}\s+(20\d{{2}}|19\d{{2}})"
        match = re.search(pattern, text)
        if match:
            d = int(match.group(1))
            y = int(match.group(2))
            try:
                return datetime(y, month, d).date().isoformat()
            except ValueError:
                return None
    return None


def classify_harmonised_category(category: object, source: str = "") -> str:
    raw = ("" if category is None else str(category)).strip().lower()
    raw_bn = raw
    if any(k in raw for k in ["economy", "business", "finance", "stock"]):
        return "economy"
    if any(k in raw_bn for k in ["অর্থ", "অর্থনীতি", "বাণিজ্য", "ব্যবসা", "ফাইন্যান্স", "শেয়ার", "শেয়ার", "বাজার"]):
        return "economy"
    if any(k in raw for k in ["politic"]):
        return "politics"
    if any(k in raw_bn for k in ["রাজনীতি"]):
        return "politics"
    if any(k in raw for k in ["national", "bangladesh", "country", "state", "local"]):
        return "national"
    if any(k in raw_bn for k in ["বাংলাদেশ", "জাতীয়", "জাতীয়", "দেশ", "সারাদেশ", "রাজধানী", "নগর", "বাংলারজমিন"]):
        return "national"
    if any(k in raw for k in ["world", "international"]):
        return "international"
    if any(k in raw_bn for k in ["আন্তর্জাতিক", "বিশ্ব"]):
        return "international"
    if any(k in raw for k in ["sport"]):
        return "sports"
    if any(k in raw_bn for k in ["খেলা", "ক্রীড়া", "ক্রীড়া"]):
        return "sports"
    if any(k in raw for k in ["education"]):
        return "education"
    if any(k in raw_bn for k in ["শিক্ষা"]):
        return "education"
    if any(k in raw for k in ["entertainment"]):
        return "entertainment"
    if any(k in raw_bn for k in ["বিনোদন"]):
        return "entertainment"
    if any(k in raw for k in ["technology", "science", "tech"]):
        return "technology_science"
    if any(k in raw_bn for k in ["প্রযুক্তি", "বিজ্ঞান"]):
        return "technology_science"
    if any(k in raw_bn for k in ["স্বাস্থ্য"]):
        return "health"
    return "other_or_unknown"


def audit_potrika() -> dict:
    file_rows = []
    total_rows = 0
    total_categories = Counter()
    total_sources = Counter()
    years = Counter()
    parseable_dates = 0

    for path in sorted(POTRIKA_DIR.glob("*.csv")):
        rows = 0
        categories = Counter()
        sources = Counter()
        fields = []
        date_min = None
        date_max = None
        parsed = 0
        with path.open("r", encoding="utf-8", errors="replace", newline="") as f:
            reader = csv.DictReader(f)
            fields = reader.fieldnames or []
            for row in reader:
                rows += 1
                category = row.get("category") or row.get("Category") or infer_category_from_filename(path.name)
                source = row.get("source") or infer_source_from_filename(path.name)
                categories[category] += 1
                sources[source] += 1
                parsed_date = parse_bangla_date(
                    row.get("publication_date")
                    or row.get("Date")
                    or row.get("date")
                    or row.get("Time")
                    or row.get("time")
                )
                if parsed_date:
                    parsed += 1
                    year = parsed_date[:4]
                    years[year] += 1
                    date_min = parsed_date if date_min is None or parsed_date < date_min else date_min
                    date_max = parsed_date if date_max is None or parsed_date > date_max else date_max
        total_rows += rows
        parseable_dates += parsed
        total_categories.update(categories)
        total_sources.update(sources)
        file_rows.append(
            {
                "dataset": "potrika",
                "file": path.name,
                "rows": rows,
                "fields": fields,
                "date_parseable_rows": parsed,
                "date_min": date_min,
                "date_max": date_max,
                "top_categories": categories.most_common(10),
                "top_sources": sources.most_common(5),
            }
        )

    return {
        "dataset": "potrika",
        "total_rows": total_rows,
        "files": len(file_rows),
        "date_parseable_rows": parseable_dates,
        "date_parseable_rate": parseable_dates / total_rows if total_rows else 0,
        "years": dict(sorted(years.items())),
        "top_categories": total_categories.most_common(30),
        "top_sources": total_sources.most_common(30),
        "file_summaries": file_rows,
    }


def infer_source_from_filename(name: str) -> str:
    low = name.lower()
    if "__" in name:
        return name.split("__", 1)[0]
    if low.startswith("ittefaq"):
        return "ittefaq"
    if low.startswith("jugantor"):
        return "jugantor"
    if low.startswith("jaijaidin"):
        return "jaijaidin"
    if low.startswith("kaler_kontho"):
        return "kaler_kontho"
    if low.startswith("somoyer_alo"):
        return "somoyer_alo"
    return "balanced_category_file"


def infer_category_from_filename(name: str) -> str:
    stem = Path(name).stem.lower()
    if "economy" in stem:
        return "economy"
    if "national" in stem:
        return "national"
    if "politics" in stem:
        return "politics"
    if "worldnews" in stem or "international" in stem:
        return "international"
    if "sports" in stem:
        return "sports"
    if "education" in stem:
        return "education"
    if "entertainment" in stem:
        return "entertainment"
    if "science" in stem:
        return "technology_science"
    return stem


def audit_bnad() -> dict:
    file_rows = []
    total_rows = 0
    total_fields = Counter()
    total_categories = Counter()
    total_harmonised = Counter()
    years = Counter()
    post_2020 = 0
    parseable_dates = 0

    for path in sorted(BNAD_DIR.glob("*.jsonl")):
        rows = 0
        field_counts = Counter()
        categories = Counter()
        harmonised = Counter()
        date_min = None
        date_max = None
        parsed = 0
        post = 0
        sample = None
        with path.open("r", encoding="utf-8", errors="replace") as f:
            for line in f:
                if not line.strip():
                    continue
                obj = json.loads(line)
                if sample is None:
                    sample = obj
                rows += 1
                field_counts.update(obj.keys())
                category = obj.get("Category")
                categories[str(category)] += 1
                harmonised[classify_harmonised_category(category, path.name)] += 1
                parsed_date = parse_bangla_date(obj.get("Time"))
                if parsed_date:
                    parsed += 1
                    year = parsed_date[:4]
                    years[year] += 1
                    if int(year) > 2020:
                        post += 1
                    date_min = parsed_date if date_min is None or parsed_date < date_min else date_min
                    date_max = parsed_date if date_max is None or parsed_date > date_max else date_max
        total_rows += rows
        parseable_dates += parsed
        post_2020 += post
        total_fields.update(field_counts)
        total_categories.update(categories)
        total_harmonised.update(harmonised)
        file_rows.append(
            {
                "dataset": "bnad",
                "file": path.name,
                "rows": rows,
                "fields_seen": sorted(field_counts),
                "date_parseable_rows": parsed,
                "date_min": date_min,
                "date_max": date_max,
                "post_2020_rows": post,
                "top_categories": categories.most_common(30),
                "harmonised_categories": harmonised.most_common(),
                "sample_keys": sorted(sample.keys()) if sample else [],
            }
        )

    return {
        "dataset": "bnad",
        "total_rows": total_rows,
        "files": len(file_rows),
        "date_parseable_rows": parseable_dates,
        "date_parseable_rate": parseable_dates / total_rows if total_rows else 0,
        "post_2020_rows": post_2020,
        "post_2020_rate_of_parseable": post_2020 / parseable_dates if parseable_dates else 0,
        "years": dict(sorted(years.items())),
        "fields": total_fields.most_common(),
        "top_categories": total_categories.most_common(80),
        "harmonised_categories": total_harmonised.most_common(),
        "file_summaries": file_rows,
    }


def write_csv_rows(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    fields = sorted({k for row in rows for k in row})
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            out = {}
            for field in fields:
                value = row.get(field)
                if isinstance(value, (list, dict)):
                    out[field] = json.dumps(value, ensure_ascii=False)
                else:
                    out[field] = value
            writer.writerow(out)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    potrika = audit_potrika()
    bnad = audit_bnad()
    summary = {"potrika": potrika, "bnad": bnad}

    (OUT_DIR / "source_schema_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    write_csv_rows(OUT_DIR / "potrika_file_summary.csv", potrika["file_summaries"])
    write_csv_rows(OUT_DIR / "bnad_file_summary.csv", bnad["file_summaries"])

    compact = {
        "potrika": {
            "total_rows": potrika["total_rows"],
            "files": potrika["files"],
            "date_parseable_rows": potrika["date_parseable_rows"],
            "years": potrika["years"],
            "top_sources": potrika["top_sources"][:10],
            "top_categories": potrika["top_categories"][:10],
        },
        "bnad": {
            "total_rows": bnad["total_rows"],
            "files": bnad["files"],
            "date_parseable_rows": bnad["date_parseable_rows"],
            "post_2020_rows": bnad["post_2020_rows"],
            "years": bnad["years"],
            "fields": bnad["fields"],
            "harmonised_categories": bnad["harmonised_categories"],
        },
    }
    print(json.dumps(compact, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
