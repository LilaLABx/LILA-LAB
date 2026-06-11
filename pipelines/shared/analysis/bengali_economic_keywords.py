"""Curated Bangla economic keyword dictionary for BBD-style index construction.

Four categories matching the BBD (Baker-Bloom-Davis) triple-category paradigm,
extended with sentiment and sector dimensions for BENI:

  - **Economy (E)**: economic domain terms (inflation, trade, GDP, market, …)
  - **Policy (P)**: government/regulatory actions (budget, tax, interest rate, …)
  - **Narrative (N)**: state-of-the-economy descriptors (crisis, recovery, growth, …)
  - **Sentiment (S)**: positive / negative outlook terms

Usage::

    from shared.data.bengali_economic_keywords import ECONOMY_KEYWORDS, make_category_regex

    # Check if an article mentions any Economy term
    import re
    pattern = make_category_regex(ECONOMY_KEYWORDS)
    is_economic = bool(pattern.search(article_text))

To build a custom keyword set for a specific index variant::

    from shared.data.bengali_economic_keywords import ECONOMY_KEYWORDS, POLICY_KEYWORDS

    my_keywords = ECONOMY_KEYWORDS | POLICY_KEYWORDS  # union
"""

from __future__ import annotations

import re
from re import Pattern

# ═══════════════════════════════════════════════════════════════════════
#  Category Keywords
# ═══════════════════════════════════════════════════════════════════════

ECONOMY_KEYWORDS: set[str] = {
    # Core economic terms
    "অর্থনীতি",
    "অর্থনৈতিক",
    "অর্থনৈতিকভাবে",
    "ব্যবসা",
    "ব্যবসায়ী",
    "ব্যবসায়িক",
    "বাণিজ্য",
    "বাণিজ্যিক",
    "বাজার",
    "বাজারজাত",
    "শিল্প",
    "শিল্পায়ন",
    "কারখানা",
    # Money & finance
    "মুদ্রা",
    "মুদ্রাস্ফীতি",
    "মূল্যস্ফীতি",
    "মূল্য",
    "দাম",
    "টাকা",
    "অর্থ",
    "আর্থিক",
    "বিনিয়োগ",
    "বিনিয়োগকারী",
    "পুঁজি",
    "ব্যাংক",
    "ব্যাংকিং",
    "ঋণ",
    "কিস্তি",
    # Trade
    "রপ্তানি",
    "আমদানি",
    "পণ্য",
    "সেবা",
    "পরিষেবা",
    "চাহিদা",
    "যোগান",
    "উৎপাদন",
    "উৎপাদক",
    "উৎপাদিত",
    "কাঁচামাল",
    "মজুদ",
    # Fiscal
    "রাজস্ব",
    "কর",
    "শুল্ক",
    "ভ্যাট",
    "আয়কর",
    "বাজেট",
    "ঘাটতি",
    "উদ্বৃত্ত",
    # Labour
    "শ্রম",
    "শ্রমিক",
    "কর্মসংস্থান",
    "বেকারত্ব",
    "বেকার",
    "চাকরি",
    "বেতন",
    "মজুরি",
    # Growth
    "জিডিপি",
    "জিএনপি",
    "প্রবৃদ্ধি",
    "অর্থনৈতিক প্রবৃদ্ধি",
    "উন্নয়ন",
    "অগ্রগতি",
    "সম্প্রসারণ",
    # Sectors
    "কৃষি",
    "পরিষেবা খাত",
    "ব্যাংক খাত",
    "পোশাক শিল্প",
    "গার্মেন্টস",
    "বিদ্যুৎ",
    "জ্বালানি",
    "তেল",
    "গ্যাস",
    "খাদ্য",
    "খাদ্যশস্য",
    # Macro
    "জীবনযাত্রার ব্যয়",
    "জীবনযাত্রার ব্যয়",
    "ক্রয়ক্ষমতা",
    "ক্রয়ক্ষমতা",
    "নামমাত্র",
    "প্রকৃত",
    "মন্দা",
    "অর্থনৈতিক মন্দা",
    "স্ফীতি",
    "মুদ্রানীতি",
    "রাজস্ব নীতি",
}

POLICY_KEYWORDS: set[str] = {
    # Government
    "সরকার",
    "সরকারি",
    "প্রধানমন্ত্রী",
    "মন্ত্রী",
    "মন্ত্রণালয়",
    "সচিব",
    "সচিবালয়",
    "সংসদ",
    "জাতীয় সংসদ",
    "আইন",
    "বিধি",
    "নিয়ম",
    "নীতি",
    "প্রণয়ন",
    "বাস্তবায়ন",
    # Regulation
    "নিয়ন্ত্রণ",
    "নিয়ন্ত্রক",
    "কমিশন",
    "কর্তৃপক্ষ",
    "সংস্থা",
    "দপ্তর",
    "পরিদপ্তর",
    "অধিদপ্তর",
    "আইনসভা",
    "আদেশ",
    "প্রজ্ঞাপন",
    "স্মারক",
    # Budget & fiscal policy
    "বাজেট",
    "অর্থবছর",
    "বার্ষিক বাজেট",
    "বাজেট বক্তৃতা",
    "বরাদ্দ",
    "ব্যয়",
    "ঘাটতি বাজেট",
    "সরকারি ব্যয়",
    "ভর্তুকি",
    "সহায়তা",
    "প্রণোদনা",
    "প্যাকেজ",
    # Monetary policy
    "সুদ",
    "সুদের হার",
    "সুদহার",
    "মুদ্রানীতি",
    "কেন্দ্রীয় ব্যাংক",
    "বাংলাদেশ ব্যাংক",
    "গভর্নর",
    "নীতি সুদহার",
    "নগদ জমা",
    "সিআরআর",
    "এসএলআর",
    "রেপো",
    "রিভার্স রেপো",
    "তারল্য",
    # Trade policy
    "শুল্ক",
    "ট্যারিফ",
    "অ-শুল্ক বাধা",
    "বাণিজ্য নীতি",
    "বাণিজ্য চুক্তি",
    "বাণিজ্য যুদ্ধ",
    "কোটা",
    "সুবিধা",
    # Development
    "পরিকল্পনা",
    "পঞ্চবার্ষিকী পরিকল্পনা",
    "উন্নয়ন প্রকল্প",
    "সরকারি প্রকল্প",
    "বিদেশি সাহায্য",
    "ঋণ",
    "ঋণদাতা",
    "দাতা",
    # Tax
    "কর",
    "করপোরেট কর",
    "মূল্য সংযোজন কর",
    "আয়কর",
    "কর ছাড়",
    "কর হার",
    "কর আদায়",
    # Elections & political
    "নির্বাচন",
    "ভোট",
    "রাজনৈতিক",
    "রাজনীতি",
    "দল",
    "জোট",
    "ক্ষমতা",
    "শাসন",
    "প্রশাসন",
}

NARRATIVE_KEYWORDS: set[str] = {
    # State & condition
    "অবস্থা",
    "পরিস্থিতি",
    "অবস্থান",
    "দশা",
    "চিত্র",
    "দৃষ্টিভঙ্গি",
    # Trends
    "প্রবণতা",
    "ধারা",
    "পরিবর্তন",
    "পরিবর্তিত",
    "বৃদ্ধি",
    "পতন",
    "হ্রাস",
    "বৃদ্ধি পেয়েছে",
    "হ্রাস পেয়েছে",
    "বেড়েছে",
    "কমেছে",
    # Change dynamics
    "উন্নতি",
    "অবনতি",
    "সংকোচন",
    "সম্প্রসারণ",
    "স্থবির",
    "স্থিতিশীল",
    "অস্থির",
    "চঞ্চল",
    # Crisis & recovery
    "সংকট",
    "অর্থনৈতিক সংকট",
    "মন্দা",
    "দুর্বলতা",
    "দুর্বল",
    "পুনরুদ্ধার",
    "সুস্থ হওয়া",
    "সংশোধন",
    "সামঞ্জস্য",
    # Comparison
    "তুলনায়",
    "আগের চেয়ে",
    "পূর্বের চেয়ে",
    "গত বছরের",
    "গত মাসের",
    "সবচেয়ে বেশি",
    "সবচেয়ে কম",
    # Outlook
    "ভবিষ্যত",
    "সম্ভাবনা",
    "প্রত্যাশা",
    "পূর্বাভাস",
    "আশা",
    "আশঙ্কা",
    "ঝুঁকি",
    "নিশ্চিত নয়",
    "অনিশ্চয়তা",
    # Impact
    "প্রভাব",
    "ফল",
    "ফলাফল",
    "পরিণতি",
    "প্রতিক্রিয়া",
    "ক্ষতি",
    "লাভ",
    "সুবিধা",
    "অসুবিধা",
    # Urgency
    "জরুরি",
    "প্রয়োজনীয়",
    "অত্যাবশ্যক",
    "গুরুত্বপূর্ণ",
    "গুরুতর",
}

POSITIVE_SENTIMENT: set[str] = {
    "উন্নতি",
    "বৃদ্ধি",
    "লাভ",
    "মুনাফা",
    "আয়",
    "সফল",
    "সাফল্য",
    "ইতিবাচক",
    "আশাবাদী",
    "আশাবাদ",
    "ভালো",
    "উত্তম",
    "চমৎকার",
    "শক্তিশালী",
    "মজবুত",
    "দৃঢ়",
    "স্থিতিশীল",
    "স্থিতিশীলতা",
    "সমৃদ্ধি",
    "সমৃদ্ধ",
    "উজ্জ্বল",
    "অগ্রগতি",
    "উন্নয়ন",
    "প্রসার",
    "পুনরুদ্ধার",
    "সুস্থ",
    "সক্ষম",
    "স্বচ্ছল",
    "স্বচ্ছলতা",
    "বর্ধিত",
    "উন্নত",
    "উৎকৃষ্ট",
    "সুবিধাজনক",
    "অনুকূল",
    "সহায়ক",
    "লাভজনক",
    "টেকসই",
    "দক্ষতা",
    "উদ্বৃত্ত",
}

NEGATIVE_SENTIMENT: set[str] = {
    "অবনতি",
    "পতন",
    "হ্রাস",
    "ক্ষতি",
    "ঘাটতি",
    "লস",
    "দেউলিয়া",
    "দেউলিয়াত্ব",
    "ব্যর্থ",
    "ব্যর্থতা",
    "নেতিবাচক",
    "হতাশাজনক",
    "হতাশা",
    "অনিশ্চয়তা",
    "অনিশ্চিত",
    "খারাপ",
    "মন্দ",
    "দুর্বল",
    "দুর্বলতা",
    "সংকট",
    "মন্দা",
    "অবনমিত",
    "অবনমন",
    "স্থবির",
    "স্থবিরতা",
    "চাপ",
    "চাপা",
    "উদ্বেগ",
    "উদ্বেগজনক",
    "দুশ্চিন্তা",
    "ভয়",
    "আশঙ্কা",
    "ঝুঁকি",
    "সংকুচিত",
    "স্ফীতি",
    "মূল্যস্ফীতি",
    "বেকারত্ব",
    "বেকার",
    "অস্থির",
    "অস্থিরতা",
    "অসুবিধা",
    "বিপর্যয়",
    "ধস",
    "পতনশীল",
    "ঋণগ্রস্ত",
    "বোঝা",
    "ত্যাগ",
    "ছাঁটাই",
    "কমানো",
    "সীমিত",
    "অপ্রতুল",
    "ঘাটতিপূর্ণ",
}

# ═══════════════════════════════════════════════════════════════════════
#  Convenience: full sets and combinators
# ═══════════════════════════════════════════════════════════════════════

ALL_ECONOMIC_KEYWORDS: set[str] = ECONOMY_KEYWORDS | POLICY_KEYWORDS | NARRATIVE_KEYWORDS

ALL_SENTIMENT_KEYWORDS: set[str] = POSITIVE_SENTIMENT | NEGATIVE_SENTIMENT

# ═══════════════════════════════════════════════════════════════════════
#  Category mapping (for BBD-style triple indexing)
# ═══════════════════════════════════════════════════════════════════════

# Each article can be classified into one or more of these BBD-style
# categories.  The standard triple is (Economy ∩ Policy ∩ Narrative).
# BENI also supports a sentiment dimension.

CATEGORIES: dict[str, set[str]] = {
    "economy": ECONOMY_KEYWORDS,
    "policy": POLICY_KEYWORDS,
    "narrative": NARRATIVE_KEYWORDS,
    "sentiment_positive": POSITIVE_SENTIMENT,
    "sentiment_negative": NEGATIVE_SENTIMENT,
}

# ═══════════════════════════════════════════════════════════════════════
#  Utility functions
# ═══════════════════════════════════════════════════════════════════════


def make_category_regex(
    keywords: set[str],
    word_boundary: bool = False,
) -> Pattern[str]:
    """Build a compiled regex that matches any of the given keywords.

    Parameters
    ----------
    keywords:
        Set of Bangla keywords to match.
    word_boundary:
        If True, wrap each keyword with ``(?<![\\w])`` / ``(?![\\w])``
        lookarounds.  Defaults to **False** because Python's ``\\b``
        breaks inside Bangla words (combining marks like ``ু``, ``ে``
        are not ``\\w`` characters).  For Bangla, substring matching
        (``word_boundary=False``) is more reliable — keywords are long
        enough that false positives are rare.

    Returns
    -------
    re.Pattern
        Compiled case-insensitive regex.
    """
    # Sort by length descending so longer phrases (e.g. "বাংলাদেশ ব্যাংক")
    # are tried before their sub-strings ("ব্যাংক").
    escaped = sorted((re.escape(kw) for kw in keywords), key=len, reverse=True)
    if word_boundary:
        pattern = "|".join(f"(?<![\\w]){kw}(?![\\w])" for kw in escaped)
    else:
        pattern = "|".join(escaped)
    return re.compile(pattern, re.IGNORECASE)


def keyword_counts(
    text: str,
    keywords: set[str],
    word_boundary: bool = True,
) -> int:
    """Count how many distinct :paramref:`keywords` appear in *text*.

    Parameters
    ----------
    text:
        Article text to scan.
    keywords:
        Set of keywords to look for.
    word_boundary:
        Whether to enforce word boundaries (default True).

    Returns
    -------
    int
        Number of distinct keywords found (not total occurrences).
    """
    pattern = make_category_regex(keywords, word_boundary=word_boundary)
    return len(set(pattern.findall(text.lower())))


def has_category(
    text: str,
    category_name: str,
    min_matches: int = 1,
) -> bool:
    """Check if *text* contains enough keywords from a named category.

    Parameters
    ----------
    text:
        Article text.
    category_name:
        One of ``"economy"``, ``"policy"``, ``"narrative"``,
        ``"sentiment_positive"``, ``"sentiment_negative"``.
    min_matches:
        Minimum number of distinct keywords required (default 1).

    Returns
    -------
    bool
    """
    kw = CATEGORIES.get(category_name)
    if kw is None:
        msg = f"Unknown category: {category_name}. Choose from {set(CATEGORIES)}"
        raise ValueError(msg)
    return keyword_counts(text, kw) >= min_matches


def classify_bbd_triple(text: str) -> dict[str, bool]:
    """Classify an article into the BBD triple categories.

    Returns
    -------
    dict
        Keys: ``"E"`` (economy), ``"P"`` (policy), ``"N"`` (narrative),
        ``"S+"`` (positive), ``"S-"`` (negative).
    """
    return {
        "E": has_category(text, "economy", min_matches=1),
        "P": has_category(text, "policy", min_matches=1),
        "N": has_category(text, "narrative", min_matches=1),
        "S+": has_category(text, "sentiment_positive", min_matches=1),
        "S-": has_category(text, "sentiment_negative", min_matches=1),
    }


# ═══════════════════════════════════════════════════════════════════════
#  Utility: build a keyword frame for analysis
# ═══════════════════════════════════════════════════════════════════════


def keyword_frame() -> pd.DataFrame:  # noqa: F821
    """Return a DataFrame summarising all keywords by category.

    Useful for auditing the dictionary and for visualisation.
    """
    import pandas as pd

    rows: list[dict[str, str]] = []
    for cat_name, keywords in CATEGORIES.items():
        for kw in sorted(keywords):
            rows.append({"category": cat_name, "keyword": kw})
    return pd.DataFrame(rows)
