import pytest

@pytest.mark.parametrize(
    "relevance_score,evidence_score,expected",
    [
        (1.0, 1.0, 1.0),
        (0.8, 1.0, 0.88),
        (0.5, 0.5, 0.5),
        (0.0, 1.0, 0.4),
        (1.0, 0.0, 0.6),
        (0.0, 0.0, 0.0),
    ],
)
def test_confidence_score_regression(
    generator,
    relevance_score,
    evidence_score,
    expected,
):
    result = generator.generate(
        signal={
            "title": "Regression signal",
            "text": "Regression test signal",
            "category": "test",
            "signal_type": "test",
        },
        brand={
            "name": "Regression Brand",
            "category": "test",
            "keywords": [],
            "strategic_priorities": [],
            "target_consumer": [],
            "geography": [],
        },
        relevance={
            "overall_score": relevance_score,
        },
        evidence=[
            {
                "signal_id": "regression_001",
                "title": "Regression evidence",
                "text": "Evidence",
                "category": "test",
                "source_type": "test",
                "score": evidence_score,
            }
        ],
    )

    assert result["confidence_score"] == expected

def test_confidence_uses_bounded_evidence_score(
    generator,
):
    result = generator.generate(
        signal={
            "title": "Boundary test",
            "text": "Boundary test",
            "category": "test",
            "signal_type": "test",
        },
        brand={
            "name": "Test Brand",
            "category": "test",
            "geography": [],
        },
        relevance={
            "overall_score": 0.5,
        },
        evidence=[
            {
                "score": 10.0,
            }
        ],
    )

    assert result["confidence_score"] == 0.7

def test_negative_scores_are_clamped(
    generator,
):
    result = generator.generate(
        signal={
            "title": "Boundary test",
            "text": "Boundary test",
            "category": "test",
            "signal_type": "test",
        },
        brand={
            "name": "Test Brand",
            "category": "test",
            "geography": [],
        },
        relevance={
            "overall_score": -5.0,
        },
        evidence=[
            {
                "score": -5.0,
            }
        ],
    )

    assert result["confidence_score"] == 0.0

def test_prompt_version_is_regression_protected(
    generator,
):
    result = generator.generate(
        signal={
            "title": "Prompt version test",
            "text": "Prompt version test",
            "category": "test",
            "signal_type": "test",
        },
        brand={
            "name": "Test Brand",
            "category": "test",
            "geography": [],
        },
        relevance={
            "overall_score": 0.5,
        },
        evidence=[],
    )

    assert result["prompt_version"] == (
        "insight_generation:v1"
    )