from __future__ import annotations
import json
from pathlib import Path
from app.intelligence.scoring import BrandRelevanceScorer
from app.services.insight_generator import InsightGenerator
from app.services.llm import MockLLMProvider

ROOT = Path(__file__).resolve().parents[2]
DATASET_PATH = ROOT / "data" / "evaluation" / "golden_dataset.json"

def build_brand(signal: dict) -> dict:
    return {
        "name": "Evaluation Brand",
        "category": signal.get("category", ""),
        "keywords": [],
        "strategic_priorities": [],
        "target_consumer": [],
        "geography": ["india"],
    }

def main() -> None:
    with DATASET_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:
        dataset = json.load(file)

    generator = InsightGenerator(
        llm=MockLLMProvider(),
    )

    scorer = BrandRelevanceScorer()

    passed = 0

    for item in dataset:
        signal = item["signal"]
        brand = build_brand(signal)

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

        parsed = json.loads(
            result["raw_response"]
        )

        required_fields = set(
            item["required_fields"]
        )

        fields_present = required_fields.issubset(
            parsed.keys()
        )

        grounded_match = (
            result["grounded"]
            == item["expected_grounded"]
        )

        category_match = (
            signal["category"]
            == item["expected_category"]
        )

        record_passed = (
            fields_present
            and grounded_match
            and category_match
        )

        if record_passed:
            passed += 1

        status = "PASS" if record_passed else "FAIL"

        print(
            f"[{status}] {item['id']} "
            f"category={signal['category']} "
            f"grounded={result['grounded']} "
            f"confidence={result['confidence_score']:.4f}"
        )

    print()
    print(
        f"Evaluation: {passed}/{len(dataset)} passed"
    )

    if passed != len(dataset):
        raise SystemExit(1)

if __name__ == "__main__":
    main()