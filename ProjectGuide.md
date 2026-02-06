# FlaskControlCenter – Project Guide

This file is the **single source of truth** for how FlaskControlCenter is structured, how it is expected to behave, and how to extend it safely.

If something feels fragile, confusing, or randomly breaks, the cause is almost always a **boundary violation** described in this document.

---

## 1. Project Philosophy

- Kiosk-first, long-running system
- Stability > cleverness
- Backend state is authoritative
- UI is optimistic but must resync
- Hardware, cloud APIs, and OS control must be isolated

**Rule of thumb:**
> Routes render. Scripts do work.

---

## 2. High-Level Architecture

```
Touch UI (Chromium Kiosk)
        │
        ▼
Flask Routes (/routes)
        │
        ▼
Scripts (/scripts)
        │
        ▼
Devices / APIs / OS
```

- Control flows upward
- State flows downward
- UI never owns truth

---

## 3. Top-Level Folder Responsibilities

### FlaskControlCenter.py

**Purpose:** Application entry point

- Create Flask app
- Register blueprints
- Start background services
- Load environment configuration

Must NOT:
- Contain feature logic
- Talk directly to hardware

---

### routes/

**Purpose:** HTTP + UI glue

Rules:
- One feature per route file
- Validate input
- Call scripts
- Return JSON or render templates

Routes must NOT:
- Poll devices
- Start threads
- Cache long-term state
- Import other routes

---

### scripts/

**Purpose:** Core system intelligence

This is where real work happens.

Allowed:
- Hardware access
- Cloud APIs
- MQTT / LAN / WebSocket
- Background threads
- State caching
- Retry logic

Rules:
- Scripts never import routes
- Scripts never render UI
- Scripts may block

Subfolders:
- scripts/govee → all Govee logic
- flat scripts → single-responsibility helpers

---

### templates/

**Purpose:** Jinja-rendered UI

Rules:
- No business logic
- No direct API calls
- Minimal JS inline (page-specific only)

Shared UI:
- templates/partials is the single source of truth

---

### static/

**Purpose:** Frontend assets

Structure:
- css/style.css → global styles
- js/ → behavior and polling
- icons/ → SVG icon library

Rules:
- Prefer CSS variables
- Avoid duplicated SVGs

---

### data/

**Purpose:** Runtime state persistence

Allowed:
- Cached API responses
- Device state snapshots
- User pin data

Rules:
- Volatile
- App must survive deletion
- No secrets

---

### envs/

**Purpose:** Secrets and configuration

Rules:
- .env files only
- Loaded via python-dotenv
- Never committed
- Never duplicated in code

---

### logs/

**Purpose:** Debug visibility

Rules:
- Append-only
- No logic depends on logs

---

### uploads/

**Purpose:** User-uploaded files

Rules:
- Treated as untrusted
- Accessed only via upload routes

---

### venv/

- Python virtual environment
- Never referenced in code
- Never modified manually

---

## 4. State & Sync Model

```
DEVICE / API
     │
     ▼
SCRIPT (authoritative)
     │
     ▼
DATA CACHE
     │
     ▼
ROUTE RESPONSE
     │
     ▼
UI
```

Implications:
- UI updates may revert
- Backend always wins
- Polling endpoints must be idempotent

If something snaps back, the backend disagreed.

---

## 5. Kiosk & Chromium Rules

- Chromium is managed by shell scripts
- Flask does not launch Chromium
- Restarting Chromium must not restart Flask

Scripts:
- scripts/start_chromium.sh
- scripts/restart_chromium.sh
- scripts/exit_kiosk.sh

---

## 6. Background Services

Examples:
- Govee polling
- Bambu MQTT
- Discord services
- MJPEG camera

Rules:
- Started once
- Restart-safe
- Network-failure tolerant
- Never started from routes or UI

---

## 7. Adding a New Feature

Checklist:
1. Implement script
2. Expose minimal route
3. Add UI
4. Add icons
5. Add JS only if needed
6. Persist state only if required

If step 1 doesn’t exist, step 2 is wrong.

---

## 8. Cleanup Rules

Safe to delete anytime:
- __pycache__
- logs
- cached data

Never delete without audit:
- scripts/
- routes/
- templates/partials/

---

## 9. Common Failure Patterns

- UI snaps back → backend authoritative
- Breaks after time → thread/API/network issue
- Breaks on kiosk restart → missing persistence
- UI frozen, Flask alive → Chromium issue

---

## 10. Final Rule

If you’re thinking:

“Why is this so hard?”

The answer is usually:
- Logic leaked into the wrong layer
- State exists in two places

Fix the boundary, not the symptom.

