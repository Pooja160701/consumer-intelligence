from app.services.llm import MockLLMProvider

def test_mock_llm_provider_generates_response() -> None:
    provider = MockLLMProvider()

    response = provider.generate(
        "Analyze protein snack demand."
    )

    assert response
    assert "Mock intelligence response" in response

def test_mock_provider_accepts_system_prompt() -> None:
    provider = MockLLMProvider()

    response = provider.generate(
        "Generate an insight.",
        system_prompt="You are a consumer intelligence analyst.",
        temperature=0.2,
    )

    assert response