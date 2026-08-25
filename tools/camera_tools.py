import cv2
import os
import time
import base64
import numpy as np

CAMERA_SNAPSHOT_PATH = os.path.join("memory", "camera_view.jpg")
UI_CAMERA_SNAPSHOT_PATH = os.path.join("ui", "camera_view.jpg")

LAST_VISION_RESULT = "No camera image has been captured yet, Boss."
LAST_CAMERA_B64 = ""

def get_last_vision_result():
    """Return the description of the last captured camera image, or capture a fresh image if none exists."""
    global LAST_VISION_RESULT
    if LAST_VISION_RESULT and "No camera image" not in LAST_VISION_RESULT:
        return f"Here are the details of the image, Boss: {LAST_VISION_RESULT}"
    return capture_vision()

def get_last_camera_b64():
    """Return the base64 string of the last captured image."""
    global LAST_CAMERA_B64
    return LAST_CAMERA_B64

def analyze_deep_visual_features(frame):
    """Deep Computer Vision Feature & Object Classifier."""
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

    if len(faces) == 1:
        analysis.append("I see you looking directly at the camera")
    elif len(faces) > 1:
        analysis.append(f"I see {len(faces)} people in front of the camera")

    # 2. Smartphone & Rectangular Screen Device Detection
    phone_detected = False
    paper_detected = False

    try:
        # Blur and Canny edge detection for structural contours
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > (w * h * 0.03): # At least 3% of frame
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.04 * peri, True)

                if len(approx) == 4:
                    x_c, y_c, w_c, h_c = cv2.boundingRect(approx)
                    aspect_ratio = float(w_c) / h_c if h_c > 0 else 0
                    
                    # Smartphone aspect ratio (vertical ~0.45-0.65 or horizontal ~1.5-2.2)
                    if (0.4 <= aspect_ratio <= 0.7) or (1.4 <= aspect_ratio <= 2.3):
                        # Check region brightness for screen glow
                        roi = gray[y_c:y_c+h_c, x_c:x_c+w_c]
                        if roi.size > 0 and np.mean(roi) > 100:
                            phone_detected = True
                            break
                    # Paper / Document aspect ratio (~0.7-1.3)
                    elif 0.7 <= aspect_ratio <= 1.3:
                        paper_detected = True
    except Exception:
        pass

    if phone_detected:
        analysis.append("you are holding up a glowing smartphone screen / mobile device to the camera")
    elif paper_detected:
        analysis.append("I see a paper document or book held up in front of the camera")

    # 3. Text Recognition / OCR (if Tesseract or text contours exist)
    extracted_text = ""
    try:
        import pytesseract
        from PIL import Image
        for tess_path in [r'C:\Program Files\Tesseract-OCR\tesseract.exe', r'C:\Users\anshp\AppData\Local\Programs\Tesseract-OCR\tesseract.exe']:
            if os.path.exists(tess_path):
                pytesseract.pytesseract.tesseract_cmd = tess_path
                break

        pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        raw_text = pytesseract.image_to_string(pil_img).strip()
        cleaned_words = [w for w in raw_text.split() if len(w) > 1]
        if cleaned_words:
            extracted_text = " ".join(cleaned_words[:15])
    except Exception:
        pass

    if extracted_text:
        analysis.append(f"I read text on screen/object: '{extracted_text}'")

    # 4. Environment Lighting & Color Tone
    avg_brightness = int(np.mean(gray))
    if avg_brightness < 40:
        lighting = "dim room lighting"
    elif avg_brightness > 180:
        lighting = "bright screen/room light"
    else:
        lighting = "clear ambient room lighting"

    analysis.append(f"the environment has {lighting}")

    return ", ".join(analysis)

def capture_vision():
    """Capture snapshot from webcam via CAP_DSHOW, analyze deep visual features, generate Base64, and save."""
    global LAST_VISION_RESULT, LAST_CAMERA_B64

    os.makedirs("memory", exist_ok=True)
    os.makedirs("ui", exist_ok=True)

    print("\n[ ACTIVATING BUDDY VISION CAMERA (CAP_DSHOW)... ]")

    try:
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not cap.isOpened():
            cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

        if not cap.isOpened():
            msg = "Could not access camera hardware, Boss. Please check if camera is connected."
            LAST_VISION_RESULT = msg
            return msg

        # Warm up camera exposure
        for _ in range(5):
            ret, frame = cap.read()
            time.sleep(0.04)

        ret, frame = cap.read()
        cap.release()

        if not ret or frame is None:
            msg = "Failed to grab image from camera hardware, Boss."
            LAST_VISION_RESULT = msg
            return msg

        # Save JPEG image files
        cv2.imwrite(CAMERA_SNAPSHOT_PATH, frame)
        cv2.imwrite(UI_CAMERA_SNAPSHOT_PATH, frame)

        # Convert frame to Base64 JPEG data URI for instant 100% reliable UI rendering!
        _, buffer = cv2.imencode('.jpg', frame)
        b64_str = base64.b64encode(buffer).decode('utf-8')
        LAST_CAMERA_B64 = f"data:image/jpeg;base64,{b64_str}"

        # Deep Visual Feature & Object Analysis
        description = analyze_deep_visual_features(frame)

        # Launch default photo viewer window
        try:
            os.startfile(CAMERA_SNAPSHOT_PATH)
        except Exception:
            pass

        full_msg = f"Camera analysis complete, Boss! {description}."
        LAST_VISION_RESULT = full_msg
        print(f"[ VISION RESULT ]: {full_msg} (Saved to memory/camera_view.jpg)\n")
        return full_msg

    except Exception as e:
        msg = f"Camera vision error: {e}"
        LAST_VISION_RESULT = msg
        return msg
