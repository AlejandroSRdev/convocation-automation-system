# Sports Convocation Automation System — Implementation Roadmap V1

# Current Status

The following areas are already defined:

## Strategic Scope
- Operational objective
- Workflow boundaries
- AI positioning
- System constraints

## Architecture
- Layered modular monolith
- Hexagonal-inspired boundaries
- Responsibility separation
- Infrastructure direction

## Operational Flow
- Match selection
- Runtime configuration
- Deterministic rendering
- Optional AI refinement
- WhatsApp delivery

## Domain
- Persistent entities
- Runtime operational configuration
- Rendering model
- DTO structure
- Message composition strategy

The system scope is now considered:
- operationally clear
- technically bounded
- implementation-ready

---

# Implementation Order

## 1. Database Layer

### Objective
Establish deterministic operational persistence before implementing workflows.

### Tasks

#### Define SQLAlchemy models
- Match
- Player
- StaffMember
- SentConvocationMessage

#### Configure Alembic migrations

#### Create initial schema

#### Seed initial operational data
- Players
- Staff members
- Matches

### Outcome
Stable operational persistence foundation.

---

## 2. AI Infrastructure

### Objective
Introduce AI as a controlled optional refinement dependency.

### Tasks

#### Configure OpenAI provider
- API client
- environment variables
- provider abstraction

#### Create AI refinement service

#### Define prompting strategy
The prompt must:
- preserve operational structure
- avoid modifying metadata
- constrain output behavior
- operate only as refinement layer

#### Define refinement constraints
AI may:
- improve wording
- shorten text
- improve readability

AI may NOT:
- alter operational structure
- modify player information
- generate autonomous convocations

### Outcome
Controlled AI refinement infrastructure.

---

## 3. Application Use Cases

### Objective
Implement operational workflows over stable persistence and infrastructure.

### Use Cases

#### GetScheduledMatches

#### GenerateConvocation
Responsibilities:
- load operational entities
- build runtime DTO
- render deterministic message

#### RefineConvocation
Responsibilities:
- receive rendered message
- apply constrained AI refinement

#### SendConvocation
Responsibilities:
- send final validated message
- persist sent artifact

#### GetDeliveryStatus
Simplified V1 delivery retrieval.

### Outcome
Operationally functional backend workflows.

---

# Important Architectural Principle

Implementation must preserve:

```text
Deterministic operational composition
+
Optional constrained AI refinement
```

The AI layer must remain:

- subordinate
- replaceable
- operationally constrained

The rendering pipeline remains:

- deterministic
- backend-controlled
- operationally authoritative

---

# Immediate Next Step

Proceed with:

- SQLAlchemy model definition
- Alembic initial migration
- database schema creation