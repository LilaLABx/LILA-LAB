import importlib.util
from pathlib import Path

import pytest

SOURCE = (
    Path(__file__).resolve().parents[1] / "pipelines/LAB/audio-annotation-lab/quality/agreement.py"
)
SPEC = importlib.util.spec_from_file_location("audio_agreement", SOURCE)
AGREEMENT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AGREEMENT)


def annotations(ratings):
    return [
        {"segment_id": str(unit), "annotator": str(rater), "labels": {"primary_field": value}}
        for rater, row in enumerate(ratings)
        for unit, value in enumerate(row)
    ]


@pytest.mark.parametrize(
    ("ratings", "expected"),
    [
        ([[0, 0], [0, 1]], 0.0),
        ([[0, 0, 1], [0, 1, 1], [0, None, None]], 0.5),
        ([[0, 0], [1, 1]], -0.5),
        ([[0, 1], [0, 1]], 1.0),
    ],
    ids=["finite_population", "unequal_coverage", "disagreement", "perfect_agreement"],
)
def test_nominal_alpha_exact_examples(ratings, expected):
    assert AGREEMENT.krippendorff_alpha(annotations(ratings)) == pytest.approx(expected)


def test_nominal_alpha_ignores_unpaired_and_missing_ratings():
    records = annotations([[0, 0, 1], [0, 1, 1], [0, None, None]])
    records += [
        {"segment_id": "unpaired", "annotator": "0", "labels": {"primary_field": 2}},
        {"segment_id": "unpaired", "annotator": "1", "labels": {}},
        {"segment_id": "missing", "annotator": "0", "labels": {"primary_field": None}},
    ]
    assert AGREEMENT.krippendorff_alpha(records) == pytest.approx(0.5)


def test_nominal_alpha_is_invariant_to_record_order():
    records = annotations([[0, 0, 1], [0, 1, 1], [0, None, None]])
    assert AGREEMENT.krippendorff_alpha(list(reversed(records))) == pytest.approx(0.5)


def test_nominal_alpha_is_invariant_to_category_names():
    records = annotations(
        [["speech", "speech", "noise"], ["speech", "noise", "noise"], ["speech", None, None]]
    )
    assert AGREEMENT.krippendorff_alpha(records) == pytest.approx(0.5)
