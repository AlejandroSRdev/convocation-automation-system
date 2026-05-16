# Sports Convocation Automation System — Use Cases V1

## 1. Get Scheduled Matches

### Purpose
Retrieve available matches for convocation generation.

### Endpoint
GET /matches

---

## 2. Generate Convocation

### Purpose
Generate a structured convocation draft from:
- selected match
- team roster
- operational metadata
- predefined template

The generated result is editable before confirmation.

### Endpoint
POST /convocations/generate

---

## 3. Refine Convocation

### Purpose
Apply optional AI-assisted refinement over an already valid convocation draft.

AI only refines:
- wording
- formatting
- readability
- tone

AI does NOT:
- select players
- modify operational data
- generate convocations autonomously

### Endpoint
POST /convocations/refine

---

## 4. Send Convocation

### Purpose
Deliver the final validated convocation through WhatsApp.

Delivery only occurs after explicit human confirmation.

### Endpoint
POST /convocations/send

---

## 5. Get Delivery Status

### Purpose
Retrieve delivery execution status.

### Endpoint
GET /convocations/{convocation_id}/delivery-status