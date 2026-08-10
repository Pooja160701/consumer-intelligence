from functools import lru_cache
from app.agents.workflow import IntelligenceWorkflow
from app.services.llm import MockLLMProvider
from app.services.retrieval import FAISSRetriever

@lru_cache(maxsize=1)
def get_workflow() -> IntelligenceWorkflow:
    """
    Return the application intelligence workflow.

    The workflow is cached so that the retrieval index and
    service objects are not recreated for every request.
    """

    raise RuntimeError(
        "Application workflow has not been initialized."
    )