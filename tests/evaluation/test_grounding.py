import json

def test_insight_is_grounded_when_evidence_exists(
    generator,
    scorer,
):
    signal = {
        "title": "High protein snacks are gaining popularity",
        "text": (
            "Consumers increasingly seek convenient "
            "high-protein snacks."
        ),
        "category": "healthy_snacks",
        "signal_type": "consumer_trend",
        "metadata": {
            "region": "India",
        },
    }

    brand = {
        "name": "Evaluation Brand",
        "category": "healthy_snacks",
        "keywords": [],
        "strategic_priorities": [],
        "target_consumer": [],
        "geography": ["india"],
    }

    relevance = scorer.score(
        signal,
        brand,
    )

    evidence = [
        {
            "signal_id": "grounding_001",
            "title": signal["title"],
            "text": signal["text"],
            "category": signal["category"],
            "source_type": "consumer_trend",
            "score": 0.95,
        }
    ]

    result = generator.generate(
        signal=signal,
        brand=brand,
        relevance=relevance,
        evidence=evidence,
    )

    assert result["grounded"] is True
    assert result["evidence_count"] == 1

    parsed = json.loads(
        result["raw_response"]
    )

    assert parsed["observation"]
    assert parsed["interpretation"]
    assert parsed["opportunity"]
    assert parsed["risk"]
    assert parsed["recommendation"]

def test_insight_is_not_marked_grounded_without_evidence(
    generator,
    scorer,
):
    signal = {
        "title": "Unknown consumer trend",
        "text": "There is no retrieved supporting evidence.",
        "category": "unknown",
        "signal_type": "consumer_trend",
        "metadata": {
            "region": "India",
        },
    }

    brand = {
        "name": "Evaluation Brand",
        "category": "unknown",
        "keywords": [],
        "strategic_priorities": [],
        "target_consumer": [],
        "geography": ["india"],
    }

    relevance = scorer.score(
        signal,
        brand,
    )

    result = generator.generate(
        signal=signal,
        brand=brand,
        relevance=relevance,
        evidence=[],
    )

    assert result["grounded"] is False
    assert result["evidence_count"] == 0

    assert result["confidence_score"] < 1.0