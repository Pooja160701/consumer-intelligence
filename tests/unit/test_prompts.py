from app.prompts.registry import PromptRegistry

def test_prompt_registry_contains_insight_prompt() -> None:
    registry = PromptRegistry()

    prompt = registry.get(
        "insight_generation",
        "v1",
    )

    assert prompt.name == "insight_generation"
    assert prompt.version == "v1"
    assert prompt.template

def test_prompt_registry_renders_prompt() -> None:
    registry = PromptRegistry()

    rendered = registry.render(
        "insight_generation",
        "v1",
        brand_name="VitaBite",
        signal_text="Protein snacks are trending.",
        relevance="0.91",
        evidence="Consumer trend evidence.",
    )

    assert "VitaBite" in rendered
    assert "Protein snacks are trending." in rendered
    assert "0.91" in rendered

def test_unknown_prompt_raises_error() -> None:
    registry = PromptRegistry()

    try:
        registry.get(
            "does_not_exist",
            "v1",
        )
    except KeyError:
        pass
    else:
        raise AssertionError(
            "Expected KeyError for unknown prompt"
        )