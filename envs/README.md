# envs/ — Environment Configuration

This folder contains environment variable files used to configure FlaskControlCenter.
All files in this folder are required and are loaded at runtime by the application.

⚠️ These files contain sensitive data and MUST NOT be committed to version control.
Only variable names are documented here — never actual values.

---

## app.env

General application configuration.

- APP_NAME — Display name of the application
- APP_VERSION — Application version string
- APP_DEBUG — Enable or disable application debug mode

---

## Bambu_Keys.env

Configuration for the Bambu Lab P1S printer integration.

- BAMBU_DEVICE_NAME — Friendly name of the printer
- BAMBU_P1S_LAN_ID — LAN IP used for local printer communication
- BAMBU_P1S_ACCESS_CODE — Access code for the printer
- BAMBU_P1S_SERIAL — Printer serial number
- BAMBU_REGION — Bambu region (e.g. global, us)
- BAMBU_TOKEN_PATH — Path to the generated Bambu authentication token file

---

## Discord.env

Discord bot configuration.

- DISCORD_BOT_TOKEN — Discord bot token used for API access

---

## Discord_Text.env

Discord text and channel ID configuration.

- DISCORD_TEXT_TRASHTALK — Channel or message target for trash talk output
- DISCORD_TEXT_SWECRET — Secret or private Discord text channel
- DISCORD_TEXT_STAFF_CHAT — Staff chat channel ID
- DISCORD_TEXT_TEXT — Default text channel ID

---

## Govee_Keys.env

Govee lighting integration configuration.

- GOVEE_API_KEY — Govee OpenAPI key
- GOVEE_DEVICE_CLOUD_ID — Govee cloud device ID
- GOVEE_DEVICE_OPENAPI_ID — Govee OpenAPI device ID
- GOVEE_DEVICE_LAN_ID — LAN device ID for local control
- GOVEE_DEVICE_NAME — Friendly device name
- GOVEE_DEVICE_SKU — Govee device SKU or model identifier

---

## Network_Ip.env

PC network configuration for kiosk to PC communication.

- PC_IP — IP address of the target PC
- PC_PORT — Port used for PC communication
- SECRET_TOKEN — Shared secret used for request authentication

---

## steam.env

Steam API configuration.

- STEAM_KEY — Steam Web API key
- STEAM_ID — Primary Steam user ID

---

## system.env

Core system and Flask security settings.

- SYSTEM_PIN — PIN code used for system login
- FLASK_SECRET — Flask secret key
- FLASK_DEBUG — Enable or disable Flask debug mode

---

## Weather.env

Weather service configuration.

- OPENWEATHER_API_KEY — OpenWeather API key
- WEATHER_LAT — Latitude for weather location
- WEATHER_LON — Longitude for weather location

---

## Notes

- All files in this directory are required.
- Values are environment-specific and user-specific.
- This directory should never be committed with real values.
