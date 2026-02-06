# routes/uploads.py
from flask import (
    Blueprint,
    request,
    send_from_directory,
    render_template,
    redirect,
    url_for,
    current_app,
    abort,
)
from pathlib import Path
import time
import requests


BASE_DIR = Path(__file__).resolve().parent.parent
# ==================================================
# Blueprints
# ==================================================
uploads_bp = Blueprint("uploads", __name__)   # API + file serving
upload_bp = Blueprint("upload", __name__)     # UI + PIN gate

# ==================================================
# Upload directory (Pi)
# ==================================================
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# ==================================================
#Upload login (PIN required every time)
# ==================================================
@upload_bp.route("/upload-login", methods=["GET", "POST"])
def upload_login():
    if request.method == "POST":
        pin = request.form.get("pin")

        if pin == current_app.config.get("SYSTEM_PIN", "0000"):
            # Render upload page directly — no session, no memory
            return render_template("programs/upload/upload.html", pin_ok=True)

        return render_template("system/login.html", error="Wrong PIN")

    return render_template("system/login.html")

# ==================================================
#Upload page (always locked)
# ==================================================
@upload_bp.route("/upload")
def upload():
    return render_template("programs/upload/upload.html")

# ==================================================
# Upload endpoint (Pi)
# ==================================================
@uploads_bp.route("/api/upload", methods=["POST"])
def upload_file():
    cleanup_old_uploads()

    file = request.files.get("file")
    if not file or not file.filename:
        return {"success": False, "error": "No file provided"}, 400

    # Sanitize filename
    filename = Path(file.filename).name
    dest = UPLOAD_DIR / filename

    # Avoid overwrite
    if dest.exists():
        dest = UPLOAD_DIR / f"{dest.stem}_{int(time.time())}{dest.suffix}"

    # Save file to Pi
    file.save(dest)

    # ==================================================
    #Notify PC to download file
    # ==================================================
    pc_ip = current_app.config.get("PC_IP")
    pc_port = current_app.config.get("PC_PORT", 5001)
    token = current_app.config.get("SECRET_TOKEN")

    if pc_ip and token:
        try:
            requests.post(
                f"http://{pc_ip}:{pc_port}/download_file",
                params={"token": token},
                json={"filename": dest.name},
                timeout=5,
            )
        except Exception as e:
            # PC might be offline — upload still succeeds
            print("PC download trigger failed:", e, flush=True)

    return {
        "success": True,
        "filename": dest.name,
    }

# ==================================================
# Serve uploaded files (for PC to pull)
# ==================================================
@uploads_bp.route("/uploads/<path:filename>")
def get_uploaded_file(filename):
    return send_from_directory(UPLOAD_DIR, filename, as_attachment=True)


# ==================================================
# Auto-clean uploads older than 7 days
# ==================================================
UPLOAD_TTL = 7 * 24 * 60 * 60   # 7 days (seconds)


def cleanup_old_uploads():
    now = time.time()

    try:
        for path in UPLOAD_DIR.iterdir():
            if not path.is_file():
                continue

            age = now - path.stat().st_mtime
            if age > UPLOAD_TTL:
                path.unlink()

    except Exception as e:
        # Never let cleanup break uploads
        print("Upload cleanup error:", e, flush=True)
