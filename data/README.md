# data/

This directory contains **runtime-generated data files** used by the Flask Control Center.

All files in this folder are **created, updated, and managed automatically** by the application at runtime.
Users should not manually edit any files in this directory.

The contents are used for state caching, UI persistence, and backend synchronization.

---

## Files

### hexa_scenes.json

Generated mapping of Hexa Glide scene slots.

- Populated automatically after syncing scenes from the Govee API
- Used to map internal scene IDs to UI slots
- Updated when scenes are refreshed

---

### hexa_state.json

Runtime state cache for the Hexa Glide device.

- Stores power state, brightness, color, kelvin, and active scene
- Used to keep UI state consistent across page reloads
- Continuously updated by the backend

---

### p1s_finish_time.txt

Estimated finish timestamp for the active print job.

- Written during print execution
- Used to calculate and display remaining time
- Automatically overwritten as needed

---

### p1s_full_state.json

Full printer state retrieved from the Bambu API.

- Generated while the application is running
- Contains detailed printer, AMS, job, and filament metadata
- Used internally for status and monitoring pages

---

### pinned_friends.json

Cached list of pinned Steam friends.

- Generated through UI interactions
- Stores SteamID64 mappings for pinned slots
- Used by the Steam Friends dashboard

---

### pinned_games.json

Cached list of pinned Steam games.

- Generated through UI interactions
- Stores Steam App ID mappings for pinned slots
- Used by Steam dashboards for quick access

---

## Important Notes

- No sensitive credentials are stored here

---

