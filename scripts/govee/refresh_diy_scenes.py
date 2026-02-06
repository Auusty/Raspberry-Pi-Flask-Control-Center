from govee import GoveeClient
from pathlib import Path
import os, json, shutil
import sys
from dotenv import load_dotenv

BASE = Path(__file__).parent
TMP = BASE / "_export_tmp"

hexa_env = BASE.parents[1] / "envs" / "Govee_Keys.env"
load_dotenv(hexa_env)

API_KEY = os.getenv("GOVEE_API_KEY")
assert API_KEY, "GOVEE_API_KEY not set"

client = GoveeClient(api_key=API_KEY)

# -------------------------
# Discover devices + scenes
# -------------------------
devices = client.discover_devices()
client.discover_diy_scenes(devices)

# -------------------------
# Export to temp directory
# -------------------------
if TMP.exists():
    shutil.rmtree(TMP)

TMP.mkdir(parents=True)

client.export_as_modules(TMP)

GEN = TMP / "govee"
assert GEN.exists(), "Expected govee export folder missing"

# -------------------------
# Move generated files UP
# -------------------------
for file in GEN.iterdir():
    if file.is_file():
        target = BASE / file.name
        shutil.move(str(file), str(target))

shutil.rmtree(TMP)

# -------------------------
# Persist DIY scene IDs
# -------------------------
diy_ids = []
for d in devices:
    for cap in d.capabilities:
        if isinstance(cap, dict) and cap.get("instance") == "diyScene":
            diy_ids.extend(
                o["value"]
                for o in cap.get("parameters", {}).get("options", [])
            )

(BASE / "diy_scene_ids.json").write_text(
    json.dumps(sorted(set(diy_ids)), indent=2)
)

print("DIY scenes refreshed (flat export, no nested folder)")


# -------------------------------------------------
# Post-sync fix (rewrite imports for package usage)
# -------------------------------------------------
from subprocess import run

fixer = BASE / "post_sync_fix.py"

if fixer.exists():
    print("Running post_sync_fix.py...")
    result = run(
        [sys.executable, str(fixer)],
        cwd=str(BASE),
        capture_output=True,
        text=True,
    )

    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
else:
    print("post_sync_fix.py not found, skipping")
