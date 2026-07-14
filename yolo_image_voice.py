#############################################
# YOLO Object Detection using OpenCV
# IMAGE + VOICE NOTIFICATION (ONCE)
#############################################

import cv2
import numpy as np
import sys
import os
from tkinter import Tk, filedialog
import pyttsx3

# ================= VOICE ENGINE =================
engine = pyttsx3.init('sapi5')
engine.setProperty('rate', 160)

def speak(text):
    engine.say(text)
    engine.runAndWait()

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
    cv2.putText(img, label, (x, y -10),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

# ================= SELECT IMAGE =================
Tk().withdraw()
image_path = filedialog.askopenfilename(
    title="Select Image",
    filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
)

if not image_path:
    print("❌ No image selected")
    sys.exit()

print("✅ Image selected:", image_path)

# ================= LOAD IMAGE =================
image = cv2.imread(image_path)
if image is None:
    print("❌ Failed to load image")
    sys.exit()

Height, Width = image.shape[:2]

# ================= LOAD CLASSES =================
with open(classes_path, "r") as f:
    classes = [line.strip() for line in f.readlines()]

print(f"✅ {len(classes)} classes loaded")

COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

# ================= LOAD YOLO =================
print("🔹 Loading YOLO model...")
net = cv2.dnn.readNet(weights_path, config_path)
print("✅ YOLO loaded")

# ================= CREATE BLOB =================
blob = cv2.dnn.blobFromImage(
    image, 1 / 255.0, (416, 416),
    swapRB=True, crop=False
)

net.setInput(blob)

# ================= FORWARD PASS =================
outs = net.forward(get_output_layers(net))

# ================= DETECTION =================
class_ids = []
confidences = []
boxes = []

conf_threshold = 0.3
nms_threshold = 0.4

detected_objects = set()   # <-- IMPORTANT

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

# ================= NMS =================
indices = cv2.dnn.NMSBoxes(
    boxes, confidences,
    conf_threshold, nms_threshold
)

if len(indices) == 0:
    print("⚠ No objects detected")
    speak("No objects detected")

for i in indices:
    i = i[0] if isinstance(i, (list, tuple, np.ndarray)) else i
    x, y, w, h = boxes[i]
    draw_prediction(image, class_ids[i], confidences[i],
                    x, y, x + w, y + h)

# ================= VOICE NOTIFICATION (ONCE) =================
if detected_objects:
    objects_text = ", ".join(detected_objects)
    speak(f"Detected objects are {objects_text}")

# ================= SHOW OUTPUT =================
image=cv2.resize(image,(500,300))
cv2.imshow("YOLO Object Detection with Voice", image)
cv2.imwrite("object-detection.jpg", image)

cv2.waitKey(0)
cv2.destroyAllWindows()

print("✅ Detection completed successfully")
