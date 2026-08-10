from app.prompts.registry import PromptRegistry
from app.services.insight_generator import InsightGenerator
from app.services.insight_parser import InsightParser
from app.services.llm import MockLLMProvider

def create_signal() -> dict:
    return {
        "id": "signal_001",
        "title": "High protein snacks gain popularity",
        "text": (
            "Consumers increasingly want "
            "convenient high protein snacks."
        ),
        "category": "healthy_snacks",
        "signal_type": "consumer_trend",
    }

def create_brand() -> dict:
    return {
        "id": "brand_001",
        "name": "VitaBite",
        "category": "healthy_snacks",
    }

def create_evidence() -> list[dict]:
    return [
        {
            "signal_id": "evidence_001",
            "title": "Protein demand is increasing",
            "text": (
                "Consumers increasingly seek "
                "high protein snacks."
            ),
            "category": "healthy_snacks",
            "source_type": "trend",
            "score": 0.94,
        }
    ]

def test_insight_generator_uses_evidence() -> None:
    generator = InsightGenerator(
        llm=MockLLMProvider(),
        prompt_registry=PromptRegistry(),
    )

    result = generator.generate(
        signal=create_signal(),
        brand=create_brand(),
        relevance={
            "overall_score": 0.91,
        },
        evidence=create_evidence(),
    )

    assert result["raw_response"]
    assert (
        result["prompt_version"]
        == "insight_generation:v1"
    )
    assert result["evidence_count"] == 1
    assert result["grounded"] is True

def test_insight_generator_marks_missing_evidence() -> None:
    generator = InsightGenerator(
        llm=MockLLMProvider()
    )

    result = generator.generate(
        signal=create_signal(),
        brand=create_brand(),
        relevance={
            "overall_score": 0.30,
        },
        evidence=[],
    )

    assert result["evidence_count"] == 0
    assert result["grounded"] is False

def test_structured_response_can_be_parsed() -> None:
    generator = InsightGenerator(
        llm=MockLLMProvider()
    )

    result = generator.generate(
        signal=create_signal(),
        brand=create_brand(),
        relevance={
            "overall_score": 0.91,
        },
        evidence=create_evidence(),
    )

    parser = InsightParser()

    parsed = parser.parse(
        result["raw_response"]
    )

    assert parsed["observation"]
    assert parsed["interpretation"]
    assert parsed["opportunity"]
    assert parsed["risk"]
    assert parsed["recommendation"]