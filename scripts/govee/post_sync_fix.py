from pathlib import Path

BASE = Path(__file__).parent

FIXES = {
    "govee_diy_scene_aliases.py": [
        ("from govee_diy_scenes import *", "from .govee_diy_scenes import *"),
    ],
    "govee_device_aliases.py": [
        ("from govee_devices import *", "from .govee_devices import *"),
    ],
    "govee_scenes.py": [
        ("from govee_scenes import *", "from .govee_scenes import *"),
    ],
    "govee_diy_scenes.py": [
        ("from govee_diy_scenes import", "from .govee_diy_scenes import"),
        ("import govee_diy_scenes", "from . import govee_diy_scenes"),
    ],
}

def fix():
    for file, replacements in FIXES.items():
        path = BASE / file
        if not path.exists():
            continue

        text = path.read_text()
        original = text

        for old, new in replacements:
            text = text.replace(old, new)

        if text != original:
            path.write_text(text)
            print(f"fixed imports in {file}")

if __name__ == "__main__":
    fix()
