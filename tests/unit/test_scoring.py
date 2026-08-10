from app.intelligence.scoring import BrandRelevanceScorer

def test_exact_category_has_high_relevance() -> None:
    scorer = BrandRelevanceScorer()

    signal = {
        "title": "High protein snacks gain popularity",
        "text": (
            "Consumers increasingly want convenient "
            "high protein snacks."
        ),
        "category": "healthy_snacks",
        "signal_type": "consumer_trend",
        "metadata": {
            "region": "india",
        },
    }

    brand = {
        "id": "brand_001",
        "name": "VitaBite",
        "category": "healthy_snacks",
        "strategic_priorities": [
            "health",
            "protein",
            "convenience",
        ],
        "keywords": [
            "protein",
            "healthy snacks",
            "high protein",
        ],
        "target_consumer": [
            "young_adults",
            "working_professionals",
        ],
        "geography": [
            "india",
        ],
    }

    result = scorer.score(
        signal,
        brand,
    )

    assert result["category_score"] == 1.0
    assert result["keyword_score"] > 0.0
    assert result["overall_score"] > 0.40

def test_unrelated_category_has_low_relevance() -> None:
    scorer = BrandRelevanceScorer()

    signal = {
        "title": "Sustainable packaging trends",
        "text": "Consumers care about packaging waste.",
        "category": "sustainable_products",
        "signal_type": "sustainability_trend",
        "metadata": {
            "region": "india",
        },
    }

    brand = {
        "id": "brand_005",
        "name": "ActiveFuel",
        "category": "sports_nutrition",
        "strategic_priorities": [
            "protein",
            "performance",
            "recovery",
        ],
        "keywords": [
            "protein",
            "sports nutrition",
            "recovery",
        ],
        "target_consumer": [
            "athletes",
        ],
        "geography": [
            "india",
        ],
    }

    result = scorer.score(
        signal,
        brand,
    )

    assert result["category_score"] == 0.0
    assert result["overall_score"] < 0.30

def test_geography_is_taken_into_account() -> None:
    scorer = BrandRelevanceScorer()

    signal = {
        "title": "Protein demand increases",
        "text": "Protein products are becoming popular.",
        "category": "protein_nutrition",
        "signal_type": "consumer_trend",
        "metadata": {
            "region": "India",
        },
    }

    brand = {
        "id": "brand_030",
        "name": "ProteinPeak",
        "category": "protein_nutrition",
        "strategic_priorities": [
            "protein",
            "performance",
        ],
        "keywords": [
            "protein",
        ],
        "target_consumer": [
            "athletes",
        ],
        "geography": [
            "india",
        ],
    }

    result = scorer.score(
        signal,
        brand,
    )

    assert result["geography_score"] == 1.0