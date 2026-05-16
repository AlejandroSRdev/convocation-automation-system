# PROJECT MANIFEST — Sports Convocation Automation System

## Purpose

This manifest defines:

* where project context is located
* how the system must be understood
* the required reading order before implementation
* the architectural constraints that must be preserved

The objective is to ensure:

* architectural consistency
* deterministic implementation
* operational alignment
* controlled AI integration

This project is a real operational backend system for sports organization workflows.

It is NOT:

* a generic sports platform
* an AI-first product
* a feature-heavy SaaS
* a chatbot system

The system prioritizes:

* deterministic workflows
* operational simplicity
* structured rendering
* backend authority
* constrained AI usage

---

# REQUIRED CONTEXT READING

Before planning or implementing anything, read ALL files inside:

```text
.docs/system/
```

The files define:

* operational objectives
* domain constraints
* architecture
* workflow behavior
* AI positioning
* persistence philosophy
* rendering strategy

Reading these files is mandatory before implementation.

---

# REQUIRED READING ORDER

Read files in this exact order:

## 1. operational-flow.md

Purpose:
Understand:

* the real-world workflow
* operational objectives
* human interaction model
* system boundaries

This file defines WHY the system exists.

---

## 2. domain.md

Purpose:
Understand:

* persistent entities
* runtime-only configuration
* deterministic rendering principles
* AI constraints
* domain exclusions

This file defines WHAT the system is.

---

## 3. architecture.md

Purpose:
Understand:
- layered modular monolith structure
- dependency direction
- domain/application/infrastructure boundaries
- repository and adapter responsibilities
- how deterministic workflows are protected from infrastructure concerns

This file defines HOW the system is architecturally organized.

---

## 4. technical-stack.md

Purpose:
Understand:
- selected backend framework
- database technology
- ORM and migration tooling
- external integrations
- deployment assumptions
- technical constraints

This file defines WITH WHAT the system is implemented.

---

## 5. use-cases.md

Purpose:
Understand:
- application responsibilities
- workflow orchestration boundaries
- backend operational flows
- implementation order for application behavior

This file defines HOW the system behaves at application level.

---

# CRITICAL ARCHITECTURAL PRINCIPLES

The following principles are NON-NEGOTIABLE.

## 1. Deterministic Backend Governance

Operational truth must come from:

* persistence
* backend rules
* controlled rendering

NOT from AI generation.

---

## 2. AI Is a Constrained Dependency

AI exists ONLY as:

* optional refinement layer

AI may:

* improve wording
* improve readability
* improve formatting

AI may NOT:

* alter operational structure
* generate convocations autonomously
* modify persisted operational truth

---

## 3. Runtime Configuration Must NOT Be Persisted

The following concepts are runtime-only:

* innings
* temporary invited players
* confirmation icons
* operational notes
* draft convocations
* runtime attendance

Do NOT introduce unnecessary persistence.

---

## 4. Operational Simplicity Over Premature Complexity

Avoid:

* unnecessary abstractions
* generic frameworks
* speculative scalability
* over-engineering

Prefer:

* explicitness
* controlled workflows
* operational clarity
* deterministic execution

---

# IMPLEMENTATION PRIORITY ORDER

The system must evolve in this order:

1. Persistence models
2. Repositories
3. Use cases
4. Rendering pipeline
5. AI refinement layer
6. Delivery integrations

Do NOT skip layers.

---

# ENGINEERING EXPECTATIONS

Implementation must:

* preserve architectural boundaries
* maintain deterministic behavior
* isolate infrastructure concerns
* avoid domain leakage into infrastructure
* avoid AI leakage into core workflows

The backend is the operational authority of the system.

Not the AI layer.

---

# FINAL RULE

If a technical decision introduces ambiguity between:

* deterministic backend governance
  and
* AI autonomy

the deterministic backend approach must always win.