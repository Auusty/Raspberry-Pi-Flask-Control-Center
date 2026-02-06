# FlaskControlCenter – Architecture Overview

This document describes **how the system is shaped and flows**, not rules or style. It exists to answer:

> “What talks to what, and where does state actually live?”

If something feels confusing, this file should make it click.

---

## 1. High-Level Mental Model

```
User (Touch UI)
   ↓
Templates (Jinja)
   ↓
Routes (Flask Blueprints)
   ↓
Scripts (Hardware / APIs / Threads)
   ↓
Devices • Cloud APIs • LAN Services
```

**Key idea:**
- Routes are *glue*
- Scripts are *authority*

Nothing skips layers.

---

## 2. Flask Core

**Entry point:** `FlaskControlCenter.py`

Responsibilities:
- Create the Flask app
- Load environment variables
- Register blueprints from `/routes`
- Start background threads (if needed)

It does **not**:
- Talk to hardware
- Contain feature logic
- Manage UI state

Think of it as the *wiring harness*.

---

## 3. Routes Layer (`/routes`)

**What routes are:**
- HTTP endpoints
- UI renderers
- Input validation

**What routes are NOT:**
- Device drivers
- Polling engines
- State owners

Typical route flow:
1. Receive request (UI or JS)
2. Validate / normalize input
3. Call one or more scripts
4. Return JSON or render a template

Routes should always be safe to call repeatedly.

---

## 4. Scripts Layer (`/scripts`)

This is where the app actually *does things*.

Scripts handle:
- Hardware access (Bambu, Govee, system)
- LAN / MQTT / HTTP APIs
- Background polling
- State caching

Scripts may:
- Keep in-memory state
- Write to `/data`
- Spawn threads

Scripts must:
- Be callable from routes
- Never import Flask routes

> If it talks to the outside world, it belongs here.

---

## 5. Polling & State Flow

### Polling Model

- UI polls backend periodically (2–5s typical)
- Backend queries scripts
- Scripts return current state

There is **no push model**.

### State Authority

- Backend state always wins
- UI may update optimistically
- UI must resync

If the UI value “snaps back”:
- That means backend disagreed

This is expected behavior, not a bug.

---

## 6. Persistent State (`/data`)

Purpose:
- Cache device snapshots
- Persist user pins / selections
- Recover state after restart

Properties:
- Volatile
- Regeneratable
- Non-secret

The app must survive:
- Deletion of individual files
- Full deletion of `/data`

---

## 7. Environment & Secrets (`/envs`)

- All secrets live in `.env` files
- Loaded at startup
- Never copied into code

If a value is required:
- Fail loudly on startup

---

## 8. Kiosk / Chromium Control

Chromium is:
- Started via shell scripts
- Restarted externally
- Treated as disposable

Flask:
- Does not manage Chromium state
- Does not depend on Chromium being alive

Safe operations:
- Restart Flask
- Restart Chromium
- Restart the Pi

Everything must reconnect cleanly.

---

## 9. Failure Philosophy

Failures are expected.

Design assumptions:
- Devices go offline
- APIs lag
- Network resets

System response:
- Log it
- Recover automatically
- Never wedge the UI

If a failure requires a reboot, that is a design bug.

---

## 10. One-Sentence Summary

**Flask Control Center is a polling-based kiosk UI where routes translate intent, scripts own reality, and the backend always tells the truth.**



