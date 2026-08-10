from typing import Any
from langgraph.graph import END, START, StateGraph
from app.agents.context_agent import BrandContextAgent
from app.agents.evidence_agent import EvidenceAgent
from app.agents.insight_agent import InsightGenerationAgent
from app.agents.prioritization_agent import PrioritizationAgent
from app.agents.signal_agent import SignalAnalysisAgent
from app.agents.state import IntelligenceState
from app.intelligence.scoring import BrandRelevanceScorer
from app.services.retrieval import FAISSRetriever

class IntelligenceWorkflow:
    """LangGraph workflow for consumer intelligence generation."""

    def __init__(
        self,
        retriever: FAISSRetriever,
    ) -> None:
        self.signal_agent = SignalAnalysisAgent()

        self.context_agent = BrandContextAgent(
            scorer=BrandRelevanceScorer()
        )

        self.evidence_agent = EvidenceAgent(
            retriever=retriever,
            top_k=3,
        )

        self.insight_agent = InsightGenerationAgent()

        self.prioritization_agent = (
            PrioritizationAgent()
        )

        self.graph = self._build_graph()

    def _build_graph(self):
        """Build the LangGraph state machine."""

        builder = StateGraph(
            IntelligenceState
        )

        builder.add_node(
            "signal_analysis",
            self._signal_analysis,
        )

        builder.add_node(
            "brand_context",
            self._brand_context,
        )

        builder.add_node(
            "evidence_retrieval",
            self._evidence_retrieval,
        )

        builder.add_node(
            "insight_generation",
            self._insight_generation,
        )

        builder.add_node(
            "prioritization",
            self._prioritization,
        )

        builder.add_edge(
            START,
            "signal_analysis",
        )

        builder.add_edge(
            "signal_analysis",
            "brand_context",
        )

        builder.add_edge(
            "brand_context",
            "evidence_retrieval",
        )

        builder.add_edge(
            "evidence_retrieval",
            "insight_generation",
        )

        builder.add_edge(
            "insight_generation",
            "prioritization",
        )

        builder.add_edge(
            "prioritization",
            END,
        )

        return builder.compile()

    def run(
        self,
        signal: dict[str, Any],
        brand: dict[str, Any],
    ) -> IntelligenceState:
        """Execute the intelligence workflow."""

        initial_state: IntelligenceState = {
            "signal": signal,
            "brand": brand,
            "errors": [],
        }

        return self.graph.invoke(
            initial_state
        )

    def _signal_analysis(
        self,
        state: IntelligenceState,
    ) -> dict[str, Any]:
        return self.signal_agent.run(
            state["signal"]
        )

    def _brand_context(
        self,
        state: IntelligenceState,
    ) -> dict[str, Any]:
        return self.context_agent.run(
            state["signal"],
            state["brand"],
        )

    def _evidence_retrieval(
        self,
        state: IntelligenceState,
    ) -> dict[str, Any]:
        return self.evidence_agent.run(
            state["signal"]
        )

    def _insight_generation(
        self,
        state: IntelligenceState,
    ) -> dict[str, Any]:
        return self.insight_agent.run(
            signal=state["signal"],
            brand=state["brand"],
            relevance=state["relevance"],
            evidence=state.get(
                "evidence",
                [],
            ),
        )

    def _prioritization(
        self,
        state: IntelligenceState,
    ) -> dict[str, Any]:
        return self.prioritization_agent.run(
            relevance=state["relevance"],
            confidence_score=state.get(
                "confidence_score",
                0.0,
            ),
        )