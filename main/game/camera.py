import cv2
import numpy as np
import threading
import time


def center_square_zoom(frame, zoom=2.0, out_size=800):
    h, w = frame.shape[:2]
    s0 = min(h, w)
    s = int(s0 / zoom)
    x1 = (w - s) // 2
    y1 = (h - s) // 2
    crop = frame[y1 : y1 + s, x1 : x1 + s]
    return cv2.resize(crop, (out_size, out_size), interpolation=cv2.INTER_LINEAR)


def count_white_pips(frame_bgr):
    h, w = frame_bgr.shape[:2]
    crop = frame_bgr[int(h * 0.15) : int(h * 0.85), int(w * 0.15) : int(w * 0.85)]

    hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)

    lower_white = np.array([0, 0, 190], dtype=np.uint8)
    upper_white = np.array([180, 60, 255], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower_white, upper_white)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    pip_count = 0
    debug = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    for c in contours:
        area = cv2.contourArea(c)
        if area < 80 or area > 2000:
            continue

        peri = cv2.arcLength(c, True)
        if peri == 0:
            continue

        circularity = 4 * np.pi * area / (peri * peri)
        if circularity < 0.55:
            continue

        pip_count += 1
        x, y, ww, hh = cv2.boundingRect(c)
        cv2.rectangle(debug, (x, y), (x + ww, y + hh), (0, 255, 0), 2)

    return pip_count, mask, debug


class DiceCamera:
    def __init__(self, cam_index=0, zoom=2.5, out_size=800):
        # Try V4L2 first (reliable on Linux/RPi), fall back to default backend.
        self.cap = None
        tried = []
        for backend in (cv2.CAP_V4L2, 0):
            try:
                self.cap = (
                    cv2.VideoCapture(cam_index, backend)
                    if backend != 0
                    else cv2.VideoCapture(cam_index)
                )
                tried.append(backend)
                if self.cap.isOpened():
                    break
            except Exception:
                self.cap = None

        if not self.cap or not self.cap.isOpened():
            raise RuntimeError(
                f"Could not open camera index {cam_index}. Backends tried: {tried}"
            )

        # Reduce internal buffering to avoid stale/invalid frames
        try:
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        except Exception:
            pass

        self.zoom = zoom
        self.out_size = out_size

        self._latest = None
        self._lock = threading.Lock()
        self._running = False
        self._thread = None

        self._first_frame_event = threading.Event()

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def _loop(self):
        last_warn = 0
        while self._running:
            ok, frame = self.cap.read()
            if not ok or frame is None:
                # don't spam; print a warning once per 2s to help debugging
                if time.time() - last_warn > 2.0:
                    print(
                        "Warning: camera read failed (ok=False or frame=None)",
                        flush=True,
                    )
                    last_warn = time.time()
                time.sleep(0.1)
                continue

            frame = center_square_zoom(frame, zoom=self.zoom, out_size=self.out_size)
            with self._lock:
                self._latest = frame

            self._first_frame_event.set()

    def wait_for_first_frame(self, timeout=2.0) -> bool:
        """
        Blocks until the first frame is available or timeout occurs.
        Returns True if frame arrived, False if timed out.
        """
        return self._first_frame_event.wait(timeout)

    def get_latest_frame(self):
        with self._lock:
            return None if self._latest is None else self._latest.copy()

    def get_pips(self):
        frame = self.get_latest_frame()
        if frame is None:
            return None, None, None
        return count_white_pips(frame)

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=1)
        self.cap.release()


def main():
    cam = DiceCamera(cam_index=0, zoom=2.5, out_size=800)
    cam.start()

    last_read_time = 0
    READ_INTERVAL = 5.0

    try:
        while True:
            frame = cam.get_latest_frame()
            if frame is None:
                continue

            now = time.time()

            # every 5 seconds, read dice
            if now - last_read_time >= READ_INTERVAL:
                last_read_time = now

                count, mask, debug = cam.get_pips()
                print("Pips:", count)

                if mask is not None:
                    cv2.imshow("Mask", mask)
                if debug is not None:
                    cv2.imshow("Mask Debug", debug)

            # always show camera
            cv2.imshow("Camera", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

    finally:
        cam.stop()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
