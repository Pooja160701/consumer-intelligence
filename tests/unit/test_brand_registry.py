from pathlib import Path
from app.services.brand_registry import BrandRegistry

BRANDS_FILE = Path("data/brands.yaml")

def test_brand_registry_loads_brands() -> None:
    registry = BrandRegistry(BRANDS_FILE)

    assert registry.brand_count() == 32

def test_brand_can_be_retrieved() -> None:
    registry = BrandRegistry(BRANDS_FILE)

    brand = registry.get_brand("brand_001")

    assert brand["name"] == "VitaBite"
    assert brand["category"] == "healthy_snacks"

def test_relevant_brand_detection() -> None:
    registry = BrandRegistry(BRANDS_FILE)

    results = registry.find_relevant_brands(
        text="Consumers are increasingly interested in high protein snacks.",
        category="healthy_snacks",
    )

    assert results
    assert results[0]["brand"]["id"] == "brand_001"