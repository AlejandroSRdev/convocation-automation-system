# Sports Convocation Automation System — Domain Definition V1

## Domain Objective

The system is designed to support structured operational generation of sports convocations inside a real baseball club environment.

The domain prioritizes:
- operational simplicity
- deterministic behavior
- structured rendering
- low-friction workflows
- controlled AI usage

The system is NOT designed as:
- a generic sports management platform
- a player availability system
- a real-time coordination platform
- an autonomous AI communication system

The system IS designed as:
- a controlled operational message composition system.

---

# Core Domain Principles

## 1. Match-Centered Domain

The operational center of the system is the Match.

The system:
- loads a match
- loads operational entities
- composes a structured convocation message
- optionally refines it through AI
- sends the final validated communication

The system does NOT manage complex convocation lifecycles.

---

## 2. Deterministic Message Composition

The convocation message is NOT generated freely by AI.

The system:
- composes a structured DTO
- renders a deterministic operational template
- optionally applies AI-assisted refinement afterwards

AI is never responsible for:
- operational structure
- player selection
- message integrity
- workflow orchestration

---

## 3. Human Operational Authority

The coach remains the final operational authority.

The system:
- assists
- structures
- accelerates

But never autonomously decides or sends without explicit confirmation.

---

# Persistent Domain Entities

## Match

Represents a scheduled game.

### Attributes

- id
- home_team
- away_team
- matchday
- match_date
- match_time
- location
- competition_type

### Notes

- Matches are retrieved from database persistence.
- Multiple matches may exist against the same opponent.
- Convocation time is NOT persisted in the Match entity.
- Convocation time is runtime operational configuration.

---

## Player

Represents a player available for convocation rendering.

### Attributes

- id
- number (nullable)
- name
- category_badge (nullable)
- active

### Notes

- Players are included by default in generated convocations.
- Availability is NOT modeled in the domain.
- Parents manually indicate absence through WhatsApp after message delivery.
- Innings assignment is NOT persisted.
- Innings are runtime rendering configuration selected by the coach.

---

## StaffMember

Represents technical staff members.

### Attributes

- id
- name
- role
- active

### Notes

- Staff members are explicitly selectable.
- Staff rotation occurs operationally depending on availability.

---

## SentConvocationMessage

Represents the final delivered message artifact.

### Attributes

- id
- match_id
- final_message
- sent_at

### Notes

- Drafts are NOT persisted.
- Refinement history is NOT persisted.
- Delivery workflows are intentionally simplified in V1.

---

# Explicitly Excluded From Domain V1

The following concepts are intentionally NOT modeled:

- Draft lifecycle
- Player availability entities
- Persistent innings tracking
- Convocation aggregates
- Approval workflows
- Multi-user coordination
- Retry orchestration
- Delivery state machines
- Historical refinement tracking
- Structured player attendance persistence

These concerns are operationally outside the current real workflow.

---

# Runtime Operational Configuration

Some operational parameters exist only during rendering execution.

These values are NOT persisted as domain entities.

## Runtime Parameters

### Convocation Time
Selected manually by the coach before rendering.

### Player Innings
Selected dynamically during rendering.

Example:
- 6/7
- 4/7
- 0/7

### Invited Players
Temporary players may be added operationally.

These players:
- may not belong to the official roster
- may not have a player number
- are runtime-only additions

### Manual Notes
Operational notes may be added dynamically.

---

# Convocation Rendering Model

## Core Principle

The system does NOT generate messages probabilistically.

Instead:
- structured operational data is composed
- deterministic rendering generates the base message
- AI optionally refines already valid text afterwards

---

# Operational DTO Structure

The system constructs a rendering-oriented DTO.

## Conceptual Structure

```json
{
  "match_info": {},
  "staff_members": [],
  "players": [],
  "links": [],
  "notes": []
}
```

### `match_info`

Contains:

- teams
- matchday
- date
- time
- convocation_time
- location
- competition_type
- players

Each player contains:

- number
- name
- innings
- category_badge
- confirmation icon

### `staff_members`

Each staff member contains:

- role
- name
- confirmation icon

### `links`

Contains operational links such as:

- statistics
- roster
- calendar
- external references

### `notes`

Contains operational informational blocks.

Example:

- attendance instructions
- coach rotation notes
- operational reminders

---

# Message Rendering

## Rendering Responsibility

The backend deterministically renders the operational message.

The rendering layer:

- interpolates DTO data
- iterates over players and staff
- composes fixed operational blocks
- preserves predefined communication structure

The rendering process is NOT delegated to AI.

---

## AI Positioning

AI exists only as:

- an optional refinement layer

AI may:

- improve wording
- shorten text
- improve readability
- improve formatting
- add motivational tone

AI may NOT:

- alter operational structure
- select players
- modify match metadata
- generate autonomous convocations

---

# Operational Flow

## 1. Match Selection

The coach selects a match.

## 2. Runtime Configuration

The coach:

- selects staff members
- adjusts innings
- defines convocation time
- optionally adds invited players

## 3. DTO Composition

The backend composes the operational DTO.

## 4. Deterministic Rendering

The backend renders the base operational message.

## 5. Optional AI Refinement

The coach may optionally refine the message through AI.

## 6. Final Validation

The coach manually validates the final message.

## 7. WhatsApp Delivery

The final validated message is delivered through WhatsApp.

---

# Strategic Architectural Outcome

The domain intentionally prioritizes:

- operational clarity
- deterministic composition
- simplicity
- controllability
- low operational friction

The system is designed to:

- support real workflows
- under real club conditions
- without unnecessary architectural complexity
- while maintaining extensibility for future operational growth