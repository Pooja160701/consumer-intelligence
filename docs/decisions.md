# Architecture Decisions

## ADR-001: PostgreSQL as the System of Record

### Decision

Use PostgreSQL as the authoritative store for application data.

### Why

Signals, sources, brands, insights and reviews require durable structured storage.

PostgreSQL also provides transactional behavior for workflows that need persistence.

### Alternative

Using only a vector database was rejected because semantic retrieval is not sufficient as the system of record for transactional application state.

---

## ADR-002: FAISS for Prototype Retrieval

### Decision

Use FAISS for semantic retrieval in the prototype.

### Why

FAISS is lightweight, local and sufficient for demonstrating evidence retrieval without introducing another hosted infrastructure dependency.

### Trade-off

FAISS is not intended to represent the final production-scale vector architecture.

A production deployment could move to a managed or distributed vector store while retaining the same retrieval abstraction.

---

## ADR-003: LangGraph for Intelligence Orchestration

### Decision

Use LangGraph for the stateful intelligence workflow.

### Why

The workflow contains multiple dependent stages:

```text
Context
  ↓
Evidence
  ↓
Analysis
  ↓
Relevance
  ↓
Insight
  ↓
Priority
```

A graph makes these transitions explicit and testable.

### Alternative

A single LLM prompt was rejected because it makes workflow state, retries and individual reasoning stages harder to isolate.

---

## ADR-004: Evidence Before Insight

### Decision

Retrieve supporting evidence before generating the final insight.

### Why

Consumer intelligence can influence product and marketing decisions.

The system should therefore be able to answer:

> Why does the system believe this?

Evidence is treated as a first-class part of the output.

---

## ADR-005: Human Approval

### Decision

Keep final business decisions with humans.

### Why

The system recommends; it does not autonomously decide what a brand should launch, change or invest in.

This creates a clear accountability boundary:

```text
AI → Research + Synthesis + Recommendation
Human → Business Decision
```

---

## ADR-006: Provider Abstraction

### Decision

Keep LLM execution behind a provider abstraction.

### Why

The intelligence workflow should not be tightly coupled to a single model provider.

The repository also supports a mock provider for deterministic testing.

### Benefit

Tests can execute without depending on external LLM availability.

---

## ADR-007: Content Hashing for Deduplication

### Decision

Generate deterministic content hashes for incoming signals.

### Why

The same signal can appear through multiple ingestion runs or sources.

Hash-based comparison provides a simple deterministic first layer for duplicate detection.

---

## ADR-008: Configuration-Driven Brands

### Decision

Keep brand information outside the core workflow logic.

### Why

Think9's requirement is fundamentally multi-brand.

Hard-coding brand-specific logic would make the system difficult to extend.

Configuration allows the same workflow to operate against different brand contexts.

---

## ADR-009: Human Review Is Persisted

### Decision

Persist review actions instead of treating them as UI-only state.

### Why

A review is a business action.

Approval, rejection and modification should survive page refreshes and be available for audit/history.

---

## ADR-010: Prototype Before Distributed Infrastructure

### Decision

Keep the current implementation locally runnable.

### Why

The assignment asks for a working prototype.

Introducing Kafka, Kubernetes and multiple distributed services before proving the core workflow would increase operational complexity without improving the POC.

The architecture leaves clear boundaries for future scaling.

---