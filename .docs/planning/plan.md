# Sports Convocation Automation System — Current Implementation State & Next Steps

## Current Status

The system has already implemented the initial infrastructure foundation required for the Sports Convocation Automation System.

The project now includes:

### 1. Database Infrastructure

Implemented:
- PostgreSQL/Supabase integration
- SQLAlchemy models
- Alembic migration setup
- Core persistence foundation

The database layer provides the operational base for storing and retrieving:
- matches
- players
- staff members
- sent convocation messages

### 2. AI Refinement Infrastructure

Implemented:
- AI provider integration
- OpenAI adapter
- controlled refinement flow
- input/output validation strategy
- semantic retry with error hints
- graceful fallback behavior
- AI treated as optional refinement layer

The AI infrastructure is intentionally constrained.

AI does NOT:
- generate convocations autonomously
- decide operational content
- select players
- modify match data
- replace deterministic backend rendering

AI only refines an already valid rendered message.

---

## Architectural Principle Already Established

The system follows the principle:

```text
Deterministic operational composition
+
Optional constrained AI refinement

The backend remains the operational authority.

The LLM is only a non-deterministic external dependency governed by deterministic backend rules.
```

---

## What Is Still Missing

The system does NOT yet have the core operational use case implemented.

The missing part is:

> Create base convocation message deterministically from database data

This is the next critical implementation step.

**Planning complete.** Implementation strategy has been designed and the implementation prompt has been written to `.claude/prompts/implementation.md`.

---

## Required Next Implementation Scope

### 1. Domain/Application Use Case

Implement the primary use case: `GenerateConvocation`

Its responsibility is to:
- Receive selected match and runtime configuration
- Load match data from database
- Load active players from database
- Load selected staff members from database
- Build a structured rendering DTO
- Render the base convocation message deterministically
- Return the rendered message and its operational metadata

### 2. Runtime Configuration Required

The use case must support runtime operational inputs such as:
- `match_id`
- `convocation_time`
- selected staff member IDs
- player innings configuration
- invited players, if any
- manual notes, if any

These values are runtime configuration, not necessarily persistent domain entities.

### 3. Deterministic Rendering Requirement

The message must be generated through backend-controlled rendering.

The LLM must NOT be involved in base message creation.

The rendering layer must:
- interpolate match data
- insert player names and numbers
- insert innings values
- insert staff members
- insert location and schedule
- preserve predefined communication structure
- include operational links or notes if required

### 4. Critical Fragments

During deterministic rendering, the system should also derive critical operational fragments.

Examples:
- player names
- field/location
- match date
- match time
- convocation time
- staff names
- operational URLs

These fragments will later be useful for validating AI refinements.

The base message generation should therefore expose enough metadata for the refinement layer to validate preservation.

---

## Expected Endpoint

The next likely endpoint is:

```
POST /convocations/generate
```

Expected behavior:

**Input:**
- selected match
- runtime operational configuration

**Output:**
- deterministic rendered message
- match metadata
- selected players
- selected staff
- critical fragments for refinement validation if appropriate

---

## Implementation Priority

The priority is not theoretical domain purity.

The priority is:
- Operational correctness
- Deterministic message generation
- Clean application orchestration
- Simple but explicit DTO construction
- Maintainable rendering logic
- Clear boundary between generation and refinement

---

## Out of Scope For This Step

Do NOT implement yet:
- WhatsApp delivery
- draft persistence
- approval workflows
- multi-user coordination
- complex domain aggregates
- availability lifecycle
- AI-generated convocations
- autonomous player selection
- advanced frontend logic

---

## Next Strategic Goal

After this step, the full intended pipeline will exist:

```
Database entities
    ↓
Runtime configuration
    ↓
DTO composition
    ↓
Deterministic base message rendering
    ↓
Optional AI refinement
    ↓
Human validation
    ↓
Future WhatsApp delivery
```
