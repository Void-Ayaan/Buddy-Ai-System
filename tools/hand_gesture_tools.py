import cv2
import time
import math
import threading
import numpy as np

HAND_GESTURE_ACTIVE = False
HAND_THREAD = None

HAND_GESTURE_STATE = {
    "detected": False,
    "pinch_distance": 100.0,
    "zoom_scale": 1.0,
    "gesture": "HAND_IDLE",
    "last_updated": 0
}

def calculate_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def _hand_tracking_loop():
    global HAND_GESTURE_ACTIVE, HAND_GESTURE_STATE

    # Try importing MediaPipe for 100% accurate hand landmark tracking
    use_mediapipe = False
    try:
        import mediapipe as mp
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        use_mediapipe = True
        print("[ HAND GESTURE CONTROLLER ]: MediaPipe Hand Tracking Active.")
    except Exception:
        print("[ HAND GESTURE CONTROLLER ]: MediaPipe unavailable, using OpenCV Contour Tracking.")

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    if not cap.isOpened():
        HAND_GESTURE_ACTIVE = False
        print("[ ⚠️ Could not open webcam for Hand Gesture Controller. ]")
        return

    smooth_zoom = 1.0

    while HAND_GESTURE_ACTIVE:
        ret, frame = cap.read()
        if not ret or frame is None:
            time.sleep(0.04)
            continue

        h, w, _ = frame.shape
        detected = False
        dist = 100.0
        gesture = "NO_HAND"

        if use_mediapipe:
            try:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(rgb_frame)

                if results.multi_hand_landmarks:
                    detected = True
                    for hand_landmarks in results.multi_hand_landmarks:
                        # Thumb tip (Landmark 4) & Index tip (Landmark 8)
                        thumb_tip = hand_landmarks.landmark[4]
                        index_tip = hand_landmarks.landmark[8]

                        thumb_px = (int(thumb_tip.x * w), int(thumb_tip.y * h))
                        index_px = (int(index_tip.x * w), int(index_tip.y * h))

                        dist = calculate_distance(thumb_px, index_px)

                        # Normalizing pinch distance (30px = 0.5x zoom, 220px = 2.2x zoom)
                        raw_zoom = max(0.4, min(2.5, dist / 110.0))
                        smooth_zoom = smooth_zoom * 0.7 + raw_zoom * 0.3

                        if dist < 45:
                            gesture = "PINCH_ZOOM_IN"
                        elif dist > 150:
                            gesture = "ENLARGE_ZOOM_OUT"
                        else:
                            gesture = "HAND_HOLDING"
                        break
            except Exception:
                pass
        else:
            # OpenCV Skin & Contour Fallback
            try:
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                lower_skin = np.array([0, 20, 70], dtype=np.uint8)
                upper_skin = np.array([20, 255, 255], dtype=np.uint8)
                mask = cv2.inRange(hsv, lower_skin, upper_skin)

                blurred = cv2.GaussianBlur(mask, (5, 5), 0)
                contours, _ = cv2.findContours(blurred, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                if contours:
                    max_cnt = max(contours, key=cv2.contourArea)
                    if cv2.contourArea(max_cnt) > (w * h * 0.04):
                        detected = True
                        hull = cv2.convexHull(max_cnt, returnPoints=False)
                        defects = cv2.convexityDefects(max_cnt, hull)

                        if defects is not None and len(defects) > 0:
                            # Distance of convex defects as proxy for pinch span
                            dist = min(200.0, max(30.0, float(len(defects) * 18.0)))
                            raw_zoom = max(0.5, min(2.2, dist / 100.0))
                            smooth_zoom = smooth_zoom * 0.7 + raw_zoom * 0.3
                            gesture = "HAND_CONTOUR_TRACKING"
            except Exception:
                pass

        HAND_GESTURE_STATE["detected"] = detected
        HAND_GESTURE_STATE["pinch_distance"] = round(dist, 1)
        HAND_GESTURE_STATE["zoom_scale"] = round(smooth_zoom, 2)
        HAND_GESTURE_STATE["gesture"] = gesture
        HAND_GESTURE_STATE["last_updated"] = time.time()

        time.sleep(0.04) # Smooth 25 FPS tracking loop

    cap.release()
    print("[ HAND GESTURE CONTROLLER STOPPED. ]")

def toggle_hand_controller(enable=True):
    """Toggle Hand Controller Agent tracking loop on/off."""
    global HAND_GESTURE_ACTIVE, HAND_THREAD

    if enable:
        if HAND_GESTURE_ACTIVE:
            return "Hand Controller Agent is already active and tracking your gestures, Boss!"

        HAND_GESTURE_ACTIVE = True
        HAND_THREAD = threading.Thread(target=_hand_tracking_loop, daemon=True)
        HAND_THREAD.start()
        return "Hand Controller Agent activated, Boss! Bring your hand in front of the camera and pinch/expand your thumb and index finger to scale the 3D spherical swarm in real-time."
    else:
        HAND_GESTURE_ACTIVE = False
        return "Deactivated Hand Controller Agent, Boss."

def get_hand_telemetry():
    """Return real-time gesture telemetry for API and HUD rendering."""
    global HAND_GESTURE_STATE
    return HAND_GESTURE_STATE
