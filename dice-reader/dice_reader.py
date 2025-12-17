import cv2
import numpy as np

def center_square_zoom(frame, zoom=2.0, out_size=800):
    # zoom = 1.0 -> largest possible center square
    # zoom = 2.0 -> 2x zoom (crop half-size square)
    h, w = frame.shape[:2]
    s0 = min(h, w)              # biggest square side
    s = int(s0 / zoom)          # smaller square side for zoom
    x1 = (w - s) // 2
    y1 = (h - s) // 2
    crop = frame[y1:y1+s, x1:x1+s]
    return cv2.resize(crop, (out_size, out_size), interpolation=cv2.INTER_LINEAR)



def count_white_pips(frame_bgr):
    min_area = 250        # increase this to ignore smaller blobs
    max_area = 10000      # keep as a safety cap

    min_wh = 12           # minimum bounding box width/height
    min_circularity = 0.70


    # Optional: crop center region if the die is roughly centered (reduces false detections)
    h, w = frame_bgr.shape[:2]
    crop = frame_bgr[int(h*0.15):int(h*0.85), int(w*0.15):int(w*0.85)]

    hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)

    # White pips: low saturation, high value
    lower_white = np.array([0, 0, 190], dtype=np.uint8)
    upper_white = np.array([180, 60, 255], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower_white, upper_white)

    # Cleanup noise
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

def main():
    cap = cv2.VideoCapture(1) 
 


    if not cap.isOpened():
        raise RuntimeError("Could not open camera. Try changing VideoCapture(0) to (1).")

    while True:
        ok, frame = cap.read()
        frame = center_square_zoom(frame, zoom=2.5, out_size=800)  # try 1.5, 2.0, 2.5, 3.0


        if not ok:
            break

        count, mask, debug = count_white_pips(frame)

        overlay = frame.copy()
        cv2.putText(overlay, f"Pips: {count}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 255, 0), 2)

        cv2.imshow("Camera", overlay)
        cv2.imshow("Mask", mask)
        cv2.imshow("Mask Debug", debug)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
