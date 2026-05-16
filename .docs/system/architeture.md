# Sports Convocation Automation System — Architecture Definition V1

## Architectural Objective
The system architecture is designed to support:
- Operational clarity
- Controlled automation
- Explicit workflow orchestration
- External dependency isolation
- Progressive extensibility

The architecture intentionally prioritizes:
- Simplicity
- Maintainability
- Operational reliability
- Separation of responsibilities

The system is **not designed as**:
- A large distributed platform
- A microservices architecture
- An AI-native autonomous system

It is **designed as**:
- A compact operational backend system with controlled external integrations.

---

## Architectural Style
**Layered Modular Monolith**  
with **Hexagonal-Inspired Boundaries**

The system is divided into four primary layers:
1. `presentation/`
2. `application/`
3. `domain/`
4. `infrastructure/`

The objective is not architectural purity, but clear operational responsibility separation.

---

### 1. DOMAIN LAYER
**Responsibility**: Defines operational entities, structural business rules, and workflow invariants.  
The domain must remain:
- Deterministic
- Dependency-independent
- Operationally focused

The domain does **NOT** know:
- Databases
- HTTP
- FastAPI
- OpenAI
- WhatsApp
- SQLAlchemy

**Core Domain Concepts**:
- **Convocation**: Central operational entity representing match communication.
- **Match**: Represents scheduled games.
- **Player**: Represents player identity and availability.
- **Team**: Represents rosters and staff members.
- **Delivery Status**: Tracks message delivery lifecycle.

---

### 2. APPLICATION LAYER
**Responsibility**: Orchestrates operational workflows, use-case execution, and dependency coordination.  
This is the **true operational center** of the system.

**Main Use Cases**:
- Generate Convocation
- Refine Convocation
- Send Convocation
- Get Match Players

---

### 3. INFRASTRUCTURE LAYER
**Responsibility**: Implements external integrations, persistence, and delivery providers.  
This layer contains all technical dependencies.

**Key Components**:
- **Database Infrastructure**: PostgreSQL, SQLAlchemy, Alembic.
- **AI Infrastructure**: OpenAI Adapter for optional textual refinement.
- **Messaging Infrastructure**: WhatsApp Provider Adapter for message delivery.

---

### 4. PRESENTATION LAYER
**Responsibility**: Exposes HTTP endpoints, request validation, and response formatting.  
This layer must remain intentionally thin.

---

## Dependency Direction
The dependency flow is strictly directional:
- `presentation → application → domain`
- `presentation → application → infrastructure`

---

## Strategic Architectural Outcome
The architecture is designed to produce:
- A real operational system
- Under real organizational conditions
- With controllable workflows
- Observable execution
- Replaceable external dependencies
- Progressively extensible automation capabilities