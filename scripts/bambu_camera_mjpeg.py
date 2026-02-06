"""
Bambu MJPEG Camera Helper
========================

Pure helper module:
- Manages a persistent JPEGFrameStream connection
- Runs a background thread to pull frames
- Exposes latest JPEG frame and an MJPEG generator

NO Flask code in here.
"""

import time
import threading
from bambulab import JPEGFrameStream


class BambuMJPEGCamera:
    def __init__(self, printer_ip: str, access_code: str):
        self.printer_ip = printer_ip
        self.access_code = access_code

        self._latest_frame = None
        self._lock = threading.Lock()

        self._running = False
        self._thread = None

        # For debug / visibility
        self.started_at = None

    # -------------------------
    # Public API
    # -------------------------

    def start(self):
        """Start the camera worker thread (safe to call once)."""
        if self._running:
            return

        self._running = True
        self.started_at = time.time()

        self._thread = threading.Thread(
            target=self._camera_worker,
            daemon=True
        )
        self._thread.start()

    def get_frame(self):
        """Return the latest JPEG frame (bytes) or None."""
        with self._lock:
            return self._latest_frame

    def mjpeg_generator(self):
        """
        Generator yielding multipart MJPEG frames.
        Intended to be used directly in a Flask Response.
        """
        while True:
            frame = self.get_frame()

            if frame is None:
                time.sleep(0.1)
                continue

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n"
                + frame +
                b"\r\n"
            )

            time.sleep(0.03)

    # -------------------------
    # Internal worker
    # -------------------------

    def _camera_worker(self):
        """Background thread that keeps the camera alive."""
        stream = JPEGFrameStream(self.printer_ip, self.access_code)

        while self._running:
            try:
                stream.connect()

                while self._running:
                    frame = stream.get_frame()
                    if frame:
                        with self._lock:
                            self._latest_frame = frame
                    time.sleep(0.03)

            except Exception as e:
                # Swallow errors and retry
                time.sleep(2)

            finally:
                try:
                    stream.disconnect()
                except Exception:
                    pass
