"""
YOLOv3 Object Detection using OpenCV


Description:
------------
This script performs object detection on all images inside a specified folder
using the YOLOv3 deep learning model and OpenCV's DNN module.

Workflow:
1. Load COCO class labels
2. Load YOLOv3 configuration and weights
3. Read images from the images directory
4. Create image blobs
5. Run forward pass through the network
6. Extract detections
7. Apply Non-Maximum Suppression (NMS)
8. Draw bounding boxes and class labels
9. Display detection results
"""

# ==========================
# Import Required Libraries
# ==========================

import os

import numpy as np
import cv2
from os import listdir
from os.path import isfile, join
from matplotlib import pyplot as plt
import urllib.request


# ==========================
# Display Image Function
# ==========================

def imshow(title="Image", image=None, size=10):
    """
    Displays an image using Matplotlib.

    Parameters:
    -----------
    title : str
        Window title

    image : ndarray
        Image to display

    size : int
        Figure size
    """
    w, h = image.shape[:2]
    aspect_ratio = w / h

    plt.figure(figsize=(size * aspect_ratio, size))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis("off")
    plt.show()


# ==========================
# Load COCO Class Labels
# ==========================

labelsPath = "coco.names"
LABELS = open(labelsPath).read().strip().split("\n")

# Generate a random color for each class
COLORS = np.random.randint(
    0,
    255,
    size=(len(LABELS), 3),
    dtype="uint8"
)

# ==========================
# Load YOLO Model
# ==========================

weights_path = "yolov3.weights"

# if not os.path.exists(weights_path):
#     print("Downloading YOLOv3 weights...")
#     urllib.request.urlretrieve(
#         "https://pjreddie.com/media/files/yolov3.weights",
#         weights_path
#     )
#     print("Download complete!")
    
cfg_path = "yolov3.cfg"

# Load YOLO network
net = cv2.dnn.readNetFromDarknet(
    cfg_path,
    weights_path
)

# Use OpenCV backend
net.setPreferableBackend(
    cv2.dnn.DNN_BACKEND_OPENCV
)

# ==========================
# Display Network Information
# ==========================

print("YOLO Network Loaded")

layer_names = net.getLayerNames()

print(f"Total Layers: {len(layer_names)}")

# ==========================
# Load Input Images
# ==========================

print("Starting Detections...")

image_folder = "images"

file_names = [
    f for f in listdir(image_folder)
    if isfile(join(image_folder, f))
]

# ==========================
# Process Each Image
# ==========================

for file in file_names:

    print(f"Processing: {file}")

    # Load image
    image = cv2.imread(os.path.join(image_folder, file))

    # Get image dimensions
    (H, W) = image.shape[:2]

    # =====================================
    # Get YOLO Output Layer Names
    # =====================================

    output_layers = net.getUnconnectedOutLayersNames()

    # =====================================
    # Create Input Blob
    # =====================================

    blob = cv2.dnn.blobFromImage(
        image,
        scalefactor=1 / 255.0,
        size=(416, 416),
        swapRB=True,
        crop=False
    )

    # Set blob as network input
    net.setInput(blob)

    # Run forward pass
    layer_outputs = net.forward(output_layers)

    # =====================================
    # Store Detection Results
    # =====================================

    boxes = []
    confidences = []
    class_ids = []

    # =====================================
    # Process Network Outputs
    # =====================================

    for output in layer_outputs:

        for detection in output:

            # Extract class scores
            scores = detection[5:]

            # Get class with highest score
            class_id = np.argmax(scores)

            confidence = scores[class_id]

            # Keep strong detections only
            if confidence > 0.75:

                # Scale bounding box
                box = detection[0:4] * np.array(
                    [W, H, W, H]
                )

                (
                    centerX,
                    centerY,
                    width,
                    height
                ) = box.astype("int")

                # Convert center coordinates
                # to top-left corner
                x = int(centerX - width / 2)
                y = int(centerY - height / 2)

                boxes.append([
                    x,
                    y,
                    int(width),
                    int(height)
                ])

                confidences.append(
                    float(confidence)
                )

                class_ids.append(
                    class_id
                )

    # =====================================
    # Apply Non-Maximum Suppression
    # =====================================

    idxs = cv2.dnn.NMSBoxes(
        boxes,
        confidences,
        score_threshold=0.5,
        nms_threshold=0.3
    )

    # =====================================
    # Draw Bounding Boxes
    # =====================================

    if len(idxs) > 0:

        for i in idxs.flatten():

            (x, y) = (
                boxes[i][0],
                boxes[i][1]
            )

            (w, h) = (
                boxes[i][2],
                boxes[i][3]
            )

            color = [
                int(c)
                for c in COLORS[class_ids[i]]
            ]

            # Draw rectangle
            cv2.rectangle(
                image,
                (x, y),
                (x + w, y + h),
                color,
                3
            )

            # Create label text
            text = (
                f"{LABELS[class_ids[i]]}: "
                f"{confidences[i]:.4f}"
            )

            # Draw label
            cv2.putText(
                image,
                text,
                (x, y - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
                2
            )
    # =====================================
    # Save Result
    # =====================================
    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)

    # Save result image
    output_path = os.path.join(
    "output",
    f"detected_{file}"
    )

    cv2.imwrite(output_path, image)
    # =====================================
    # Display Result
    # =====================================

    imshow(
        "YOLO Detections",
        image,
        size=12
    )

print("Detection Completed!")