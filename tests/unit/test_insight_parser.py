import pytest
from app.services.insight_parser import InsightParser

def test_parser_accepts_valid_json() -> None:
    parser = InsightParser()

    response = """
    {
        "observation": "Protein demand is increasing.",
        "interpretation": "The signal aligns with the brand.",
        "opportunity": "Explore a protein-focused offering.",
        "risk": "Demand may not persist.",
        "recommendation": "Validate with additional evidence."
    }
    """

    result = parser.parse(response)

    assert result["observation"]
    assert result["recommendation"]

def test_parser_rejects_invalid_json() -> None:
    parser = InsightParser()

    with pytest.raises(ValueError):
        parser.parse(
            "This is not JSON."
        )

def test_parser_rejects_missing_fields() -> None:
    parser = InsightParser()

    response = """
    {
        "observation": "Something happened."
    }
    """

    with pytest.raises(ValueError):
        parser.parse(response)