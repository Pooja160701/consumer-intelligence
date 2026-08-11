import json
from pathlib import Path
import pytest
from app.intelligence.scoring import BrandRelevanceScorer
from app.services.insight_generator import InsightGenerator
from app.services.llm import MockLLMProvider

PROJECT_ROOT = Path(__file__).resolve().parents[2]
GOLDEN_DATASET = (
    PROJECT_ROOT / "data" / "evaluation" / "golden_dataset.json"
)

@pytest.fixture(scope="session")
def golden_dataset():
    with GOLDEN_DATASET.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)

@pytest.fixture
def generator():
    return InsightGenerator(
        llm=MockLLMProvider(),
    )

@pytest.fixture
def scorer():
    return BrandRelevanceScorer()

@pytest.fixture
def evaluation_brand():
    return {
        "name": "Evaluation Brand",
        "category": "healthy_snacks",
        "keywords": [],
        "strategic_priorities": [],
        "target_consumer": [],
        "geography": ["india"],
    }

def build_evaluation_brand(signal):
    return {
        "name": "Evaluation Brand",
        "category": signal.get("category", ""),
        "keywords": [],
        "strategic_priorities": [],
        "target_consumer": [],
        "geography": ["india"],
    }

@pytest.fixture
def make_brand():
    return build_evaluation_brand