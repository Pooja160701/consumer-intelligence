# Architecture

## 1. Objective

Think9 Consumer Intelligence OS is designed as a centralized intelligence layer for a multi-brand consumer organization.

The system continuously transforms fragmented consumer and market signals into structured, evidence-backed intelligence that can be reviewed by humans before entering a business workflow.

Core flow:

```text
Signal
  ↓
Normalization
  ↓
Deduplication
  ↓
Storage
  ↓
Evidence Retrieval
  ↓
Agentic Analysis
  ↓
Brand Relevance
  ↓
Priority
  ↓
Human Review
  ↓
Decision
```

---

## 2. High-Level Architecture

```text
                 External / Internal Signals
                          │
                          ▼
                 ┌─────────────────┐
                 │    Ingestion    │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ Normalize +     │
                 │ Deduplicate     │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │   PostgreSQL    │
                 │ System of Record│
                 └────────┬────────┘
                          │
                    ┌─────┴─────┐
                    ▼           ▼
              Evidence      Structured
              Retrieval       Context
                    │           │
                    └─────┬─────┘
                          ▼
                 ┌─────────────────┐
                 │    LangGraph    │
                 │ Intelligence    │
                 │    Workflow     │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ Relevance +     │
                 │ Confidence +    │
                 │ Priority        │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ Human Review    │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ FastAPI /       │
                 │ Dashboard       │
                 └─────────────────┘
```

---

## 3. Core Components

### Ingestion

Responsible for collecting and normalizing incoming signals.

Signals contain:

* source
* source type
* title
* text
* URL
* timestamp
* category
* metadata
* content hash

Content hashing provides deterministic duplicate detection.

---

### PostgreSQL

PostgreSQL is the system of record for structured application data.

Primary entities include:

* brands
* sources
* signals
* insights
* reviews

The database provides durable storage and supports review/audit workflows.

---

### Retrieval

FAISS provides semantic retrieval over indexed signal/evidence content.

The retrieval layer is intentionally separated from PostgreSQL:

```text
PostgreSQL
    │
    │ source of truth
    ▼
Retrieval Builder
    │
    ▼
FAISS Index
```

The vector index can therefore be rebuilt from the database.

---

## 4. Agentic Workflow

The intelligence workflow is implemented as a stateful graph.

Conceptually:

```text
Input Signal
     │
     ▼
Context
     │
     ▼
Evidence Retrieval
     │
     ▼
Analysis
     │
     ▼
Brand Relevance
     │
     ▼
Insight Generation
     │
     ▼
Priority
     │
     ▼
Structured Insight
```

The graph is useful because the intelligence process contains multiple dependent reasoning stages rather than a single LLM call.

Each stage contributes structured state to the next stage.

---

## 5. Evidence Grounding

The system is designed around evidence-backed intelligence.

An insight should be traceable to:

* source
* source URL
* signal
* supporting evidence
* confidence
* affected brand/category

The retrieval layer provides supporting context before intelligence generation.

This reduces the risk of unsupported claims and makes review easier.

---

## 6. Multi-Brand Architecture

Brand configuration is separated from workflow logic.

A brand can define:

* name
* category
* description
* configuration/context

The same intelligence workflow can therefore operate against different brand configurations.

```text
                    Intelligence OS
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
          Brand A       Brand B       Brand N
             │             │             │
        Context A      Context B      Context N
             │             │             │
             └─────────────┼─────────────┘
                           ▼
                    Brand-specific
                      intelligence
```

The prototype demonstrates the pattern; production rollout would add additional operational isolation and access controls.

---

## 7. Human-in-the-Loop

AI is responsible for accelerating research and synthesis.

Humans remain responsible for business decisions.

```text
AI discovers
     ↓
AI analyzes
     ↓
AI retrieves evidence
     ↓
AI prioritizes
     ↓
AI recommends
     ↓
Human reviews
     ↓
Approve / Reject / Modify
```

Review actions are persisted so that decisions are not lost after the UI interaction.

---

## 8. API Layer

FastAPI exposes application capabilities to clients.

The API separates:

* request validation
* business logic
* persistence
* intelligence workflow execution

This keeps the dashboard from being tightly coupled to the underlying implementation.

---

## 9. Dashboard

The Streamlit dashboard provides a lightweight interface for demonstrating:

* intelligence outputs
* evidence
* prioritization
* review workflow

The dashboard is a prototype interface rather than a production frontend.

---

## 10. Data Flow

```text
Raw Signal
    ↓
Validated Signal
    ↓
Normalized Signal
    ↓
Deduplicated Signal
    ↓
Persisted Signal
    ↓
Indexed Evidence
    ↓
Retrieved Evidence
    ↓
Agent State
    ↓
Generated Insight
    ↓
Scored Insight
    ↓
Reviewed Insight
```

---

## 11. Failure Boundaries

The architecture separates failures by layer:

* ingestion failures do not require rebuilding the API
* retrieval can be rebuilt from PostgreSQL
* LLM/provider failures are isolated behind the provider abstraction
* review state is persisted independently of generation
* evaluation is independent from production execution

This makes individual components easier to test and replace.

---

## 12. Scaling Direction

The prototype is intentionally simple enough to run locally.

A production architecture could evolve toward:

```text
Scheduled / Event Ingestion
          ↓
Message Queue
          ↓
Processing Workers
          ↓
PostgreSQL + Vector Store
          ↓
Agent Workers
          ↓
Review Queue
          ↓
API + Web Application
```

The current repository demonstrates the logical boundaries required for that evolution without pretending that the prototype is already a distributed production platform.

---