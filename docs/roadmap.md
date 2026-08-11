# 30-Day MVP Roadmap

## Goal

Move the prototype toward a production-ready Consumer Intelligence MVP that can support Think9's multi-brand operating model.

---

## Days 1–7 — Data Foundation

### Deliver

- Production ingestion connectors
- Source configuration
- Signal validation
- Deduplication
- PostgreSQL schema hardening
- Data retention strategy
- Initial observability

### Success Criteria

A reliable pipeline can ingest, normalize, deduplicate and persist signals.

---

## Days 8–14 — Intelligence Layer

### Deliver

- Production embedding strategy
- Retrieval improvements
- Agent workflow hardening
- Structured model outputs
- Evidence validation
- Confidence scoring
- Failure/retry handling

### Success Criteria

A signal can reliably produce a structured, evidence-backed insight.

---

## Days 15–21 — Brand Intelligence + Review

### Deliver

- Multi-brand configuration
- Brand/category context
- Relevance scoring
- Priority scoring
- Review queue
- Approve/reject/modify workflow
- Audit history

### Success Criteria

The same signal can be evaluated against different brand contexts and reviewed by a human.

---

## Days 22–26 — Platform Hardening

### Deliver

- Authentication
- Authorization
- Secret management
- Rate limiting
- Structured logging
- Metrics
- Error monitoring
- Container hardening
- Load testing

### Success Criteria

The system has the controls required for a controlled internal deployment.

---

## Days 27–30 — Pilot

### Deliver

- Pilot brand configuration
- Production-like dataset
- Evaluation suite
- Regression baseline
- User feedback loop
- Deployment runbook
- Operational documentation

### Success Criteria

A small pilot group can use the system end-to-end and evaluate whether the generated intelligence is useful and trustworthy.

---

## Longer-Term Evolution

```text
Prototype
   ↓
MVP
   ↓
Pilot
   ↓
Multi-brand Rollout
   ↓
Continuous Intelligence Platform
````

Potential future capabilities:

* additional external signal sources
* streaming/event-driven ingestion
* richer internal company context
* advanced ranking
* feedback-driven evaluation
* model routing
* production vector infrastructure
* workflow integrations

---