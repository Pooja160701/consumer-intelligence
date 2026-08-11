import json

REQUIRED_FIELDS = {
    "observation",
    "interpretation",
    "opportunity",
    "risk",
    "recommendation",
}

def test_golden_dataset_is_loaded(golden_dataset):
    assert len(golden_dataset) == 3

    for item in golden_dataset:
        assert "id" in item
        assert "signal" in item
        assert "expected_category" in item
        assert "expected_grounded" in item
        assert "required_fields" in item

def test_golden_dataset_insights_match_contract(
    golden_dataset,
    generator,
    scorer,
    make_brand,
):
    for item in golden_dataset:
        signal = item["signal"]
        brand = make_brand(signal)

        relevance = scorer.score(
            signal,
            brand,
        )

        evidence = [
            {
                "signal_id": item["id"],
                "title": signal["title"],
                "text": signal["text"],
                "category": signal["category"],
                "source_type": signal["signal_type"],
                "score": 1.0,
            }
        ]

        result = generator.generate(
            signal=signal,
            brand=brand,
            relevance=relevance,
            evidence=evidence,
        )

        assert result["prompt_version"] == (
            "insight_generation:v1"
        )

        assert result["evidence_count"] == 1
        assert result["grounded"] is item["expected_grounded"]

        parsed = json.loads(
            result["raw_response"]
        )

        for field in item["required_fields"]:
            assert field in parsed
            assert parsed[field]

        assert signal["category"] == (
            item["expected_category"]
        )

        assert isinstance(
            result["confidence_score"],
            float,
        )

        assert 0.0 <= result["confidence_score"] <= 1.0