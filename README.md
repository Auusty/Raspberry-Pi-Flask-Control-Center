# FlaskControlCenter

FlaskControlCenter is a kiosk-first Flask application designed to run on a Raspberry Pi with a touchscreen, providing a unified control panel for system status, smart devices, and external services.

This project was built for a real, always-on environment and prioritizes stability, recoverability, and clear separation of concerns.

---

## 🖥 PC Integration

This control center can optionally connect to a Windows PC listener service:

- **PC Listener (Windows)**  
  https://github.com/Auusty/pc_listener

The PC listener enables:
- Steam game launching
- Discord voice automation
- Screen sharing
- Local app launching
- File transfers from Pi → PC

## Hardware / Environment

Designed for:
- Raspberry Pi (touchscreen kiosk)
- Chromium in kiosk mode
- Bambu P1S printer
- Govee smart lighting
- Steam API
- Discord bot / automation
- OpenWeather API

---

## Quick Start (High Level)

1. Clone the repository
2. Create a Python virtual environment
3. Install dependencies
4. Configure environment files
5. Start the Flask service or run manually

Detailed setup instructions live in the documentation below.

---

## Required Configuration

Before running the app, you must configure:

- **Credentials**
  - See [`credentials/README.md`](credentials/README.md)

- **Environment variables**
  - See [`envs/README.md`](envs/README.md)

- **Runtime data files**
  - See [`data/README.md`](data/README.md)

---

## Documentation

- Architecture & mental model:  
  👉 [`ProjectGuide.md`](ProjectGuide.md)

- Design principles & boundaries:  
  👉 [`guidelines.md`](guidelines.md)

---

## Philosophy

This project follows a few strict rules:

- Backend state is authoritative
- UI is touch-first and disposable
- Hardware access never happens in routes
- The system must survive restarts and partial failures

If something feels hard to debug, the issue is almost always a boundary violation.

