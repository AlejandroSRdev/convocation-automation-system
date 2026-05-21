# API Contracts — Sports Convocation Automation System V1

**Content-Type (all POST requests):** `application/json`

---

## 1. GET /matches

### Purpose

Returns all matches stored in the database. Used to select a `match_id` before calling `/convocations/generate`.

### Request

```
GET /matches
```

No headers, no body required.

### Response

**200 OK**

```json
[
  {
    "id": 1,
    "home_team": "CB Panteres Vallès",
    "away_team": "CB Badalona",
    "matchday": 5,
    "match_date": "2026-05-25",
    "match_time": "11:00:00",
    "location": "Camp Municipal de Granollers",
    "competition_type": "Lliga Catalana"
  }
]
```

| Field | Type | Description |
|---|---|---|
| `id` | `int` | Primary key. Use this as `match_id` in `/convocations/generate`. |
| `home_team` | `string` | Home team name. |
| `away_team` | `string` | Away team name. |
| `matchday` | `int` | Round/matchday number. |
| `match_date` | `string` | ISO 8601 date (`YYYY-MM-DD`). |
| `match_time` | `string` | Time with seconds (`HH:MM:SS`). |
| `location` | `string` | Venue name. |
| `competition_type` | `string` | League or cup name. |

**Empty database — 200 OK**

```json
[]
```

### Validation Rules

No input. No validation.

### Failure Cases

| Scenario | Status | Detail |
|---|---|---|
| DB unreachable | `500` | SQLAlchemy session error. Check `DATABASE_URL` in `.env`. |

### Operational Notes

- `id` is always an integer. No UUIDs.
- `match_time` includes seconds in the response (`HH:MM:SS`), even though the renderer displays only `HH:MM`.

---

## 2. POST /convocations/generate

### Purpose

Generates a deterministic WhatsApp-formatted convocation message from real database data. No AI involved. Output is fully controlled by backend logic.

### Request

```
POST /convocations/generate
Content-Type: application/json
```

**Complete example:**

```json
{
  "match_id": 1,
  "convocation_time": "09:30",
  "selected_staff_ids": [3, 7],
  "player_innings": {
    "12": "6/9",
    "18": "1/3",
    "25": "4/6"
  },
  "excluded_player_ids": [9],
  "invited_players": [
    { "name": "Jordi Puig", "number": 22 },
    { "name": "Marc Fernández" }
  ],
  "manual_notes": [
    "Porteu el material complet",
    "Reunió prèvia al vestidor a les 09:15h"
  ]
}
```

**Field reference:**

| Field | Type | Required | Description |
|---|---|---|---|
| `match_id` | `int` | Yes | ID from `GET /matches`. Must exist in DB. |
| `convocation_time` | `string` | Yes | Displayed verbatim as convocation call time (e.g. `"09:30"`). Not validated as a time format — raw string. |
| `selected_staff_ids` | `int[]` | No (default `[]`) | IDs of active staff members to include. Order is preserved in the rendered output. |
| `player_innings` | `dict[string, string]` | No (default `{}`) | Map of player ID (as string key) to innings string (e.g. `"6/9"`). Active players not present in this map receive default innings `"?/?"`. |
| `excluded_player_ids` | `int[]` | No (default `[]`) | IDs of active players to omit entirely from the convocation. |
| `invited_players` | `object[]` | No (default `[]`) | External players not in the database. `name` is required; `number` is optional. All receive innings `"?/?"`. |
| `manual_notes` | `string[]` | No (default `[]`) | Free-text lines appended to the attendance block, each prefixed with `📌`. |

### Response

**200 OK**

```json
{
  "rendered_message": "*CB Panteres Vallès vs CB Badalona*\nJornada 5 — Lliga Catalana\n\n🗓️ Diumenge 25/05/2026\n⏰ Partido: 11:00h\n🕤 Convocatoria: 09:30h\n🏟️ Camp Municipal de Granollers\n\n👨‍💼 *Staff Técnico:*\n  Manager: Joan Costa\n\n⚾ *Convocados (4):*\n#7 Carles Serra (6/9) ✅\n#12 Miquel Valls (1/3) ✅\n#22 Jordi Puig (?/?) ✅\nMarc Fernández (?/?) ✅\n\n🔗 *Enllaços operacionals:*\n📊 Estadístiques: https://stats.example.com\n📋 Plantilla: https://roster.example.com\n📅 Calendari: https://calendar.example.com\n\n📢 *Instrucciones de asistencia:*\nConfirmad asistencia por WhatsApp antes de las 20h del viernes, gracias.\n\n📌 Porteu el material complet\n📌 Reunió prèvia al vestidor a les 09:15h\n\n🐾 *CB Panteres Vallès*",
  "match_metadata": {
    "home_team": "CB Panteres Vallès",
    "away_team": "CB Badalona",
    "matchday": 5,
    "match_date": "2026-05-25",
    "match_time": "11:00",
    "location": "Camp Municipal de Granollers",
    "competition_type": "Lliga Catalana"
  },
  "selected_players": [
    { "number": 7, "name": "Carles Serra", "innings": "6/9", "category_badge": null },
    { "number": 12, "name": "Miquel Valls", "innings": "1/3", "category_badge": null },
    { "number": 22, "name": "Jordi Puig", "innings": "?/?", "category_badge": null },
    { "number": null, "name": "Marc Fernández", "innings": "?/?", "category_badge": null }
  ],
  "selected_staff": [
    { "role": "Manager", "name": "Joan Costa" }
  ],
  "critical_fragments": [
    "CB Panteres Vallès",
    "CB Badalona",
    "Camp Municipal de Granollers",
    "Carles Serra",
    "Miquel Valls",
    "Jordi Puig",
    "Marc Fernández",
    "Joan Costa"
  ]
}
```

**Field reference:**

| Field | Type | Description |
|---|---|---|
| `rendered_message` | `string` | Complete WhatsApp-formatted message. Ready to send. |
| `match_metadata` | `object` | Match data used in the message. `match_date` is ISO string; `match_time` is `HH:MM` (no seconds). |
| `selected_players` | `object[]` | All players included in the message (DB players + invited). `number` is `null` for players without a shirt number. |
| `selected_staff` | `object[]` | Staff members included in the message, in request order. |
| `critical_fragments` | `string[]` | Strings that must survive AI refinement verbatim. Pass these directly to `POST /convocations/refine`. |

**Rendered message block order:**

1. Header — `*{home} vs {away}*` + matchday + competition
2. Match info — date (Catalan format `dd/mm/yyyy`), match time, convocation time, location
3. Staff — only rendered if `selected_staff_ids` is non-empty
4. Players — count includes DB players + invited players
5. Links — static operational URLs
6. Attendance — WhatsApp confirmation instruction + `manual_notes`
7. Footer — `🐾 *CB Panteres Vallès*`

### Validation Rules

| Field | Rule |
|---|---|
| `match_id` | Must be an integer. Must exist in DB — otherwise 404. |
| `convocation_time` | Must be a string. No format enforcement; displayed verbatim. |
| `selected_staff_ids` | Must be an array of integers. Non-existent or inactive IDs are silently ignored. |
| `player_innings` | Keys must be string representations of integer IDs. Values are free strings. |
| `excluded_player_ids` | Must be an array of integers. |
| `invited_players[].name` | Required string. |
| `invited_players[].number` | Optional integer. Omit for players without a number. |

### Failure Cases

| Scenario | Status | Body |
|---|---|---|
| `match_id` not found in DB | `404` | `{"detail": "Match not found: {match_id}"}` |
| Wrong field types (e.g. `match_id` as string) | `422` | FastAPI Pydantic validation error |
| DB unreachable | `500` | SQLAlchemy session error |

### Operational Notes

- **Excluded players** are removed before any processing. They will not appear in `selected_players` or in the rendered message.
- **Invited players** are always appended after DB players in the players block, always with innings `"?/?"`.
- **Players not in `player_innings`** automatically receive `"?/?"` as innings. You do not need to list every player.
- **Staff block is omitted** from the message entirely if `selected_staff_ids` is empty or all IDs are inactive.
- **`manual_notes`** are rendered under the attendance instruction, each on its own line with `📌` prefix. Empty array produces no extra lines.
- **`critical_fragments`** must be passed verbatim to `/convocations/refine`. They are the backend's enforcement mechanism against AI hallucination.
- Rendering is fully deterministic. Same inputs always produce the same `rendered_message`.

---

## 3. POST /convocations/refine

### Purpose

Submits a generated convocation message to an AI model (GPT-4o-mini) for stylistic refinement. The backend validates the AI output before returning it. If validation fails or the AI provider is unavailable, the original message is returned unchanged.

**System contract:**
```
Backend = deterministic operational layer  (source of truth)
AI      = constrained probabilistic dependency  (style only)
```

### Request

```
POST /convocations/refine
Content-Type: application/json
```

**Complete example** — use `rendered_message` and `critical_fragments` directly from a `/convocations/generate` response:

```json
{
  "message": "*CB Panteres Vallès vs CB Badalona*\nJornada 5 — Lliga Catalana\n\n🗓️ Diumenge 25/05/2026\n⏰ Partido: 11:00h\n🕤 Convocatoria: 09:30h\n🏟️ Camp Municipal de Granollers\n\n👨‍💼 *Staff Técnico:*\n  Manager: Joan Costa\n\n⚾ *Convocados (3):*\n#7 Carles Serra (6/9) ✅\n#12 Miquel Valls (1/3) ✅\n\n🐾 *CB Panteres Vallès*",
  "critical_fragments": [
    "CB Panteres Vallès",
    "CB Badalona",
    "Camp Municipal de Granollers",
    "Carles Serra",
    "Miquel Valls",
    "Joan Costa"
  ],
  "style": "make it more concise and energetic"
}
```

**Field reference:**

| Field | Type | Required | Description |
|---|---|---|---|
| `message` | `string` | Yes | The full convocation message to refine. Non-empty, max 5000 characters. |
| `critical_fragments` | `string[]` | Yes | Strings the AI output must contain verbatim. Take from `critical_fragments` in the `/generate` response. |
| `style` | `string \| null` | No | Natural language style instruction passed to the AI. If omitted, the AI defaults to improving readability and clarity. |

### Response

**200 OK — refinement succeeded**

```json
{
  "refined_message": "*CB Panteres Vallès vs CB Badalona*\nJornada 5 — Lliga Catalana\n\n🗓️ Diumenge 25/05/2026 | ⏰ 11:00h | 🕤 09:30h\n🏟️ Camp Municipal de Granollers\n\n👨‍💼 Joan Costa (Manager)\n\n⚾ *Convocats (3):* #7 Carles Serra (6/9) ✅  #12 Miquel Valls (1/3) ✅\n\n🐾 *CB Panteres Vallès*",
  "was_refined": true
}
```

**200 OK — refinement skipped (AI failure or validation failure)**

```json
{
  "refined_message": "<original message verbatim, unchanged>",
  "was_refined": false
}
```

| Field | Type | Description |
|---|---|---|
| `refined_message` | `string` | The refined message if successful, or the original message if refinement failed. |
| `was_refined` | `bool` | `true` if the AI produced a valid output. `false` if the original was returned. |

### Validation Rules

| Field | Rule |
|---|---|
| `message` | Required. Non-empty, non-whitespace-only, maximum 5000 characters. |
| `critical_fragments` | Required array. May be empty — no constraints enforced if empty. |
| `style` | Optional. Any string or omit entirely. |

### Failure Cases

| Scenario | Status | Body |
|---|---|---|
| `message` is empty or whitespace | `422` | `{"detail": "Message cannot be empty"}` |
| `message` exceeds 5000 characters | `422` | `{"detail": "..."}` from input validator |
| Wrong field types | `422` | FastAPI Pydantic validation error |
| Invalid or missing `OPENAI_API_KEY` | `200` | `was_refined: false`, original message returned |
| OpenAI timeout or connection error | `200` | `was_refined: false`, original message returned (single retry attempted internally) |
| AI output missing a critical fragment (first attempt) | internal retry | Backend retries once with explicit fragment preservation instruction |
| AI output missing a critical fragment (retry also fails) | `200` | `was_refined: false`, original message returned |

### Operational Notes

**AI governance constraints — what the AI is instructed to preserve:**

- Every player name and jersey number exactly as written
- Every URL exactly as written
- All schedule data: date, time, location
- WhatsApp formatting syntax (`*bold*`, `_italic_`)
- All emojis

**What the AI must not do:**

- Remove or rename any player, staff member, or role
- Modify any date, time, or location
- Add information not present in the original message
- Change the operational structure of the message

**Backend enforcement mechanism:**

After the AI responds, the backend validates that every string in `critical_fragments` appears verbatim in the refined output. If any fragment is missing:
1. A single retry is attempted with an explicit instruction listing the missing fragments.
2. If the retry also fails validation, the original message is returned with `was_refined: false`.

This means `was_refined: false` is not an error — it is the designed safe fallback. The frontend can use either `refined_message` unconditionally (it is always a valid, usable message).

**Refinement is purely stylistic.** Tone, phrasing, and layout may change. Operational data — teams, players, times, locations, URLs — may not.
