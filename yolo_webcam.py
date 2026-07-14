#############################################
# YOLO Object Detection using Webcam + VOICE
# Windows SAPI Voice (Guaranteed)
#############################################

import cv2
import numpy as np
import os
import time
import win32com.client

# ================= VOICE (WINDOWS SAPI) =================
speaker = win32com.client.Dispatch("SAPI.SpVoice")

def speak(text):
    print("VOICE:", text)
    speaker.Speak(text)

# object_name : last_spoken_time
spoken_objects = {}
VOICE_DELAY = 4   # seconds between voice alerts

# ================= BASE DIRECTORY =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ================= YOLO FILE PATHS =================
config_path = os.path.join(BASE_DIR, "yolo-coco", "yolov3.cfg")
weights_path = os.path.join(BASE_DIR, "yolo-coco", "yolov3.weights")
classes_path = os.path.join(BASE_DIR, "yolo-coco", "coco.names")

# ================= HELPER FUNCTIONS =================
def get_output_layers(net):
    layer_names = net.getLayerNames()
    try:
        return [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    except:
        return [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
    label = f"{classes[class_id]} {confidence:.2f}"
    color = COLORS[class_id]
    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
    cv2.putText(
        img, label, (x, y - 10),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2
    )

# ================= LOAD CLASSES =================
with open(classes_path, "r") as f:
    classes = [line.strip() for line in f.readlines()]

COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

# ================= LOAD YOLO =================
print("🔹 Loading YOLO model...")
net = cv2.dnn.readNet(weights_path, config_path)
print("✅ YOLO loaded")

# ================= OPEN WEBCAM =================
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
if not cap.isOpened():
    print("❌ Cannot open webcam")
    exit()

speak("Blind assistance system started")
print("🎥 Webcam started (Press Q to quit)")

# ================= LIVE DETECTION LOOP =================
while True:
    ret, frame = cap.read()
    if not ret:
        break

    Height, Width = frame.shape[:2]

    blob = cv2.dnn.blobFromImage(
        frame, 1 / 255.0, (416, 416),
        swapRB=True, crop=False
    )

    net.setInput(blob)
    outs = net.forward(get_output_layers(net))

    boxes = []
    confidences = []
    class_ids = []
    detected_objects = set()

    conf_threshold = 0.6
    nms_threshold = 0.5

    # ---------- DETECTION ----------
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > conf_threshold:
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
                detected_objects.add(classes[class_id])

    indices = cv2.dnn.NMSBoxes(
        boxes, confidences,
        conf_threshold, nms_threshold
    )

    for i in indices:
        i = i[0] if isinstance(i, (list, tuple, np.ndarray)) else i
        x, y, w, h = boxes[i]
        draw_prediction(
            frame, class_ids[i], confidences[i],
            x, y, x + w, y + h
        )

    # ---------- VOICE (CONTINUOUS WITH DELAY) ----------
    current_time = time.time()
    for obj in detected_objects:
        last_time = spoken_objects.get(obj, 0)
        if current_time - last_time > VOICE_DELAY:
            speak(obj)          # 🔊 SAYS OBJECT NAME
            spoken_objects[obj] = current_time

    cv2.imshow("YOLO Webcam Detection with Voice", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ================= CLEANUP =================
cap.release()
cv2.destroyAllWindows()
speak("Camera stopped")
print("✅ Webcam closed")
