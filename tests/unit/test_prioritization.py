from app.intelligence.ranking import InsightRanker

def test_ranker_orders_highest_priority_first() -> None:
    ranker = InsightRanker()

    items = [
        {
            "brand_id": "brand_001",
            "relevance_score": 0.40,
            "priority_score": 0.45,
        },
        {
            "brand_id": "brand_002",
            "relevance_score": 0.90,
            "priority_score": 0.91,
        },
        {
            "brand_id": "brand_003",
            "relevance_score": 0.70,
            "priority_score": 0.72,
        },
    ]

    ranked = ranker.rank(items)

    assert ranked[0]["brand_id"] == "brand_002"
    assert ranked[1]["brand_id"] == "brand_003"
    assert ranked[2]["brand_id"] == "brand_001"

def test_priority_labels() -> None:
    ranker = InsightRanker()

    assert ranker.priority_label(0.90) == "P1"
    assert ranker.priority_label(0.70) == "P2"
    assert ranker.priority_label(0.50) == "P3"
    assert ranker.priority_label(0.20) == "P4"