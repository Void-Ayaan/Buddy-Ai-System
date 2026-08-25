import cv2
import os
import time
import base64
import numpy as np
import threading

CAMERA_SNAPSHOT_PATH = os.path.join("memory", "camera_view.jpg")
UI_CAMERA_SNAPSHOT_PATH = os.path.join("ui", "camera_view.jpg")

LAST_VISION_RESULT = "No camera image has been captured yet, Boss."
LAST_CAMERA_B64 = ""

# Live Continuous 24/7 Vision State
LIVE_VISION_ACTIVE = False
LIVE_VISION_THREAD = None
ENVIRONMENT_STATE = {
    "faces_count": 0,
    "lighting": "clear ambient room lighting",
    "motion_detected": False,
    "last_description": "Camera offline",
    "last_updated": 0
}

def get_last_vision_result():
    """Return description of last captured camera image or live vision state."""
    global LAST_VISION_RESULT, LIVE_VISION_ACTIVE, ENVIRONMENT_STATE
    if LIVE_VISION_ACTIVE and ENVIRONMENT_STATE["last_description"]:
        return f"Live Vision Eye is active, Boss! {ENVIRONMENT_STATE['last_description']}."
    if LAST_VISION_RESULT and "No camera image" not in LAST_VISION_RESULT:
        return f"Here are the details of the image, Boss: {LAST_VISION_RESULT}"
    return capture_vision()

def get_last_camera_b64():
    """Return the base64 string of the last captured image."""
    global LAST_CAMERA_B64
    return LAST_CAMERA_B64

def analyze_deep_visual_features(frame, prev_gray=None):
    """Deep Computer Vision Feature, Object & Motion Classifier."""
    analysis = []
    h, w, _ = frame.shape
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 1. Face & Person Detection
    faces = []
    try:
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        if os.path.exists(cascade_path):
            face_cascade = cv2.CascadeClassifier(cascade_path)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    except Exception:
        pass

    faces_count = len(faces)
    if faces_count == 1:
        analysis.append("I see you looking directly at the camera")
    elif faces_count > 1:
        analysis.append(f"I see {faces_count} people in front of the camera")
    else:
        analysis.append("I am scanning the room")

    # 2. Motion Detection between consecutive frames
    motion_detected = False
    if prev_gray is not None:
        try:
            diff = cv2.absdiff(prev_gray, gray)
            _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
            motion_pixels = np.sum(thresh > 0)
            if motion_pixels > (w * h * 0.05): # At least 5% pixel movement
                motion_detected = True
                analysis.append("movement detected in the room")
        except Exception:
            pass

    # 3. Smartphone & Rectangular Object Contour Detection
    phone_detected = False
    paper_detected = False

    try:
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > (w * h * 0.03):
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.04 * peri, True)

                if len(approx) == 4:
                    x_c, y_c, w_c, h_c = cv2.boundingRect(approx)
                    aspect_ratio = float(w_c) / h_c if h_c > 0 else 0
                    
                    if (0.4 <= aspect_ratio <= 0.7) or (1.4 <= aspect_ratio <= 2.3):
                        roi = gray[y_c:y_c+h_c, x_c:x_c+w_c]
                        if roi.size > 0 and np.mean(roi) > 100:
                            phone_detected = True
                            break
                    elif 0.7 <= aspect_ratio <= 1.3:
                        paper_detected = True
    except Exception:
        pass

    if phone_detected:
        analysis.append("a glowing smartphone screen or mobile device is held in view")
    elif paper_detected:
        analysis.append("a paper document or book is visible in front of the camera")

    # 4. Environment Lighting Assessment
    avg_brightness = int(np.mean(gray))
    if avg_brightness < 40:
        lighting = "dim room lighting"
    elif avg_brightness > 180:
        lighting = "bright room light"
    else:
        lighting = "clear ambient room lighting"

    analysis.append(f"the room has {lighting}")

    description_str = ", ".join(analysis)
    return description_str, faces_count, lighting, motion_detected, gray

def _continuous_vision_loop():
    """Background daemon continuously capturing live webcam frames every 1.2 seconds."""
    global LIVE_VISION_ACTIVE, LAST_CAMERA_B64, LAST_VISION_RESULT, ENVIRONMENT_STATE

    os.makedirs("memory", exist_ok=True)
    os.makedirs("ui", exist_ok=True)

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    if not cap.isOpened():
        LIVE_VISION_ACTIVE = False
        print("[ ⚠️ Could not open webcam for Live Vision Eye Daemon. ]")
        return

    prev_gray = None

    while LIVE_VISION_ACTIVE:
        ret, frame = cap.read()
        if ret and frame is not None:
            # Save latest JPEG files
            cv2.imwrite(CAMERA_SNAPSHOT_PATH, frame)
            cv2.imwrite(UI_CAMERA_SNAPSHOT_PATH, frame)

            # Update Base64 string for HUD rendering
            _, buffer = cv2.imencode('.jpg', frame)
            b64_str = base64.b64encode(buffer).decode('utf-8')
            LAST_CAMERA_B64 = f"data:image/jpeg;base64,{b64_str}"

            # Analyze visual features & motion
            desc, faces_cnt, light, motion, gray_frame = analyze_deep_visual_features(frame, prev_gray)
            prev_gray = gray_frame

            ENVIRONMENT_STATE["faces_count"] = faces_cnt
            ENVIRONMENT_STATE["lighting"] = light
            ENVIRONMENT_STATE["motion_detected"] = motion
            ENVIRONMENT_STATE["last_description"] = desc
            ENVIRONMENT_STATE["last_updated"] = time.time()

            LAST_VISION_RESULT = f"Live Vision Eye active: {desc}"

        time.sleep(1.2) # Sample frame every 1.2s

    cap.release()
    print("[ LIVE VISION EYE DAEMON STOPPED. ]")

def toggle_live_vision(enable=True):
    """Toggle continuous 24/7 Live Vision Eye camera daemon on/off."""
    global LIVE_VISION_ACTIVE, LIVE_VISION_THREAD

    if enable:
        if LIVE_VISION_ACTIVE:
            return "Live Vision Eye is already active and watching your environment, Boss!"
        
        LIVE_VISION_ACTIVE = True
        LIVE_VISION_THREAD = threading.Thread(target=_continuous_vision_loop, daemon=True)
        LIVE_VISION_THREAD.start()
        return "Live Vision Eye activated, Boss! I am now continuously watching through your camera and monitoring your environment in real-time."
    else:
        LIVE_VISION_ACTIVE = False
        return "Deactivated Live Vision Eye, Boss."

def capture_vision():
    """Capture single snapshot or activate Live Vision Eye."""
    global LIVE_VISION_ACTIVE
    if LIVE_VISION_ACTIVE:
        return get_last_vision_result()

    os.makedirs("memory", exist_ok=True)
    os.makedirs("ui", exist_ok=True)

    print("\n[ ACTIVATING BUDDY VISION CAMERA (CAP_DSHOW)... ]")

    try:
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not cap.isOpened():
            cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

        if not cap.isOpened():
            msg = "Could not access camera hardware, Boss. Please check if camera is connected."
            return msg

        for _ in range(5):
            ret, frame = cap.read()
            time.sleep(0.04)

        ret, frame = cap.read()
        cap.release()

        if not ret or frame is None:
            return "Failed to grab image from camera hardware, Boss."

        cv2.imwrite(CAMERA_SNAPSHOT_PATH, frame)
        cv2.imwrite(UI_CAMERA_SNAPSHOT_PATH, frame)

        _, buffer = cv2.imencode('.jpg', frame)
        b64_str = base64.b64encode(buffer).decode('utf-8')
        LAST_CAMERA_B64 = f"data:image/jpeg;base64,{b64_str}"

        description, _, _, _, _ = analyze_deep_visual_features(frame)

        full_msg = f"Camera analysis complete, Boss! {description}."
        print(f"[ VISION RESULT ]: {full_msg} (Saved to memory/camera_view.jpg)\n")
        return full_msg

    except Exception as e:
        return f"Camera vision error: {e}"
