# FlaskControlCenter – Project Guidelines

This document defines **structure, responsibilities, and rules** for the FlaskControlCenter project. The goal is to keep the project stable, predictable, and easy to extend without things randomly breaking.

---

## 1. Project Philosophy

- This is a **kiosk-first**, long-running Flask application
- Stability > cleverness
- UI polish is welcome, but **backend state must be authoritative**
- Anything that touches hardware, networks, or cloud APIs should be isolated

If you’re unsure where something belongs: **routes render, scripts do work**.

---

## 2. Top-Level Folder Responsibilities

### `/FlaskControlCenter.py`
- App entry point
- Flask app creation
- Blueprint registration
- Background threads / long-lived services
- Should NOT contain feature logic

---

### `/routes/`
**Purpose:** HTTP + UI glue layer

Rules:
- One feature = one route file
- Routes:
  - Validate input
  - Call scripts
  - Return JSON or render templates
- Routes should NOT:
  - Talk directly to hardware
  - Contain long-running loops
  - Store persistent state

Examples:
- `routes/hexa_glide.py` → UI + API endpoints
- `routes/p1s.py` → Printer status endpoints

---

### `/scripts/`
**Purpose:** Real work happens here

Rules:
- Hardware access lives here
- Cloud APIs live here
- Background threads live here
- Scripts may:
  - Cache state
  - Poll devices
  - Talk MQTT / LAN / Web APIs

Subfolders:
- `scripts/govee/` → All Govee-specific logic
- Flat scripts → Single-purpose helpers

Golden rule:
> Routes call scripts. Scripts never import routes.

---

### `/templates/`
**Purpose:** Jinja UI views

Rules:
- No business logic
- No API calls
- Keep JS inline only if page-specific

Shared UI:
- `templates/partials/` is the single source of truth
- Header, toast, screensaver, etc. live here

---

### `/static/`
**Purpose:** Frontend assets

Structure:
- `css/style.css` → Global styles only
- `js/` → Behavior (polling, transitions, theme, toast)
- `icons/` → SVG icons (single source)

Rules:
- No inline SVG duplication
- Prefer CSS variables over hardcoded colors

---

### `/data/`
**Purpose:** Runtime state persistence

Allowed contents:
- Cached API responses
- Device state snapshots
- User pin data

Rules:
- Treated as volatile
- App must survive deletion of this folder
- Never store secrets here

---

### `/envs/`
**Purpose:** Secrets and configuration

Rules:
- `.env` files only
- Loaded via `python-dotenv`
- NEVER committed
- NEVER duplicated into code

---

### `/logs/`
**Purpose:** Debug + forensic visibility

Rules:
- Logs may be noisy
- Logs are append-only
- No logic should depend on logs

---

### `/uploads/`
**Purpose:** User-uploaded assets

Rules:
- Accessed only via upload routes
- Treated as untrusted input

---

### `/venv/`
- Virtual environment
- Never touched manually
- Never referenced in code

---

## 3. State & Sync Rules

- **Backend is authoritative**
- UI may optimistically update, but must resync
- Polling endpoints should be idempotent
- If something “snaps back”, backend won

---

## 4. Kiosk / Chromium Rules

- Chromium is controlled via shell scripts in `/scripts/`
- Flask does NOT manage Chromium directly
- Restart logic must be:
  - Idempotent
  - Safe to call repeatedly

---

## 5. Adding a New Feature (Checklist)

1. Add script in `/scripts/`
2. Expose minimal API in `/routes/`
3. Add UI in `/templates/`
4. Add icons to `/static/icons/`
5. Add JS only if needed
6. Persist state only if required

If step 1 doesn’t exist, step 2 is wrong.

---

## 6. Cleanup Rules

Safe to delete anytime:
- `__pycache__/`
- Log files
- Cached data in `/data/`

Never delete without audit:
- `/scripts/`
- `/routes/`
- `/templates/partials/`

---

## 7. Known Design Constraints

- Long polling is preferred over WebSockets
- Threads are acceptable, async is isolated
- UI runs on touch-first assumptions
- Everything must survive kiosk restarts

---

## 8. Final Rule

If you’re asking:
> “Why is this so hard?”

The answer is usually:
- Logic leaked into the wrong layer
- Or state exists in two places

Fix the boundary, not the symptom.
