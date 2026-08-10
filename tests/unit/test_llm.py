from app.services.llm import MockLLMProvider

def test_mock_llm_provider_generates_structured_response() -> None:
    provider = MockLLMProvider()

    response = provider.generate(
        "Analyze protein snack demand."
    )

    assert response

    assert '"observation"' in response
    assert '"interpretation"' in response
    assert '"opportunity"' in response
    assert '"risk"' in response
    assert '"recommendation"' in response

def test_mock_provider_accepts_system_prompt() -> None:
    provider = MockLLMProvider()

    response = provider.generate(
        "Generate an insight.",
        system_prompt=(
            "You are a consumer intelligence analyst."
        ),
        temperature=0.2,
    )

    assert response