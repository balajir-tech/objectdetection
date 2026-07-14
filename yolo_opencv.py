#############################################
# YOLO Object Detection using OpenCV
# Auto-path safe version (NO path errors)
#############################################

import cv2
import numpy as np
import sys
import os
from tkinter import Tk, filedialog

# ================= BASE DIRECTORY =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ================= YOLO FILE PATHS =================
config_path = os.path.join(BASE_DIR, "yolo-coco", "yolov3.cfg")
weights_path = os.path.join(BASE_DIR, "yolo-coco", "yolov3.weights")
classes_path = os.path.join(BASE_DIR, "yolo-coco", "coco.names")
# ==================================================


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
    cv2.putText(img, label, (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


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
if not os.path.exists(classes_path):
    print("❌ coco.names NOT FOUND at:", classes_path)
    sys.exit()

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

# ================= NMS =================
indices = cv2.dnn.NMSBoxes(
    boxes, confidences,
    conf_threshold, nms_threshold
)

if len(indices) == 0:
    print("⚠ No objects detected")

for i in indices:
    i = i[0] if isinstance(i, (list, tuple, np.ndarray)) else i
    x, y, w, h = boxes[i]
    draw_prediction(image, class_ids[i], confidences[i],
                    x, y, x + w, y + h)

# ================= SHOW OUTPUT =================
cv2.imshow("YOLO Object Detection", image)
cv2.imwrite("object-detection.jpg", image)

cv2.waitKey(0)
cv2.destroyAllWindows()

print("✅ Detection completed successfully")
