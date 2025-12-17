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
    crop = frame[y1:y1+s, x1:x1+s]
    return cv2.resize(crop, (out_size, out_size), interpolation=cv2.INTER_LINEAR)

def count_white_pips(frame_bgr):
    h, w = frame_bgr.shape[:2]
    crop = frame_bgr[int(h*0.15):int(h*0.85), int(w*0.15):int(w*0.85)]

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
        self.cap = cv2.VideoCapture(cam_index)
        if not self.cap.isOpened():
            raise RuntimeError(f"Could not open camera index {cam_index}")

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
        while self._running:
            ok, frame = self.cap.read()
            if not ok:
                time.sleep(0.01)
                continue

            frame = center_square_zoom(frame, zoom=self.zoom, out_size=self.out_size)
            with self._lock:
                self._latest = frame

            self._first_frame_event.set()

    def wait_for_first_frame(self, timeout=10.0) -> bool:
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
            self._thread.join(timeout=1.0)
        self.cap.release()