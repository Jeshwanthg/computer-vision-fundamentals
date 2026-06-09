import os
import cv2
import numpy as np
from easyocr import Reader

# ==========================================
# Create Output Folder
# ==========================================

os.makedirs("output", exist_ok=True)

# ==========================================
# Load Image
# ==========================================

image = cv2.imread(
    os.path.join("images", "test.png")
)

if image is None:
    raise FileNotFoundError(
        "Could not load images/test.png"
    )

original = image.copy()

# ==========================================
# Initialize EasyOCR
# ==========================================

reader = Reader(
    ["en"],
    gpu=False
)

# ==========================================
# OCR Detection
# ==========================================

results = reader.readtext(image)

all_text = []

# Copy for visualization
ocr_boxes = image.copy()

for (bbox, text, prob) in results:

    all_text.append(text)

    (tl, tr, br, bl) = bbox

    tl = (int(tl[0]), int(tl[1]))
    br = (int(br[0]), int(br[1]))

    cv2.rectangle(
        ocr_boxes,
        tl,
        br,
        (0, 255, 0),
        2
    )

    cv2.putText(
        ocr_boxes,
        text,
        (tl[0], tl[1] - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )

# ==========================================
# Save Extracted Text
# ==========================================

output_text = "\n".join(all_text)

with open(
    "output/easyocr_text.txt",
    "w",
    encoding="utf-8"
) as f:
    f.write(output_text)

# ==========================================
# Create Text Panel
# ==========================================

text_panel = np.ones(
    (
        original.shape[0],
        original.shape[1],
        3
    ),
    dtype=np.uint8
) * 255

y = 40

for line in all_text:

    cv2.putText(
        text_panel,
        line,
        (20, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 0),
        2
    )

    y += 40

# ==========================================
# Create Detection Mask
# ==========================================

detection_view = np.zeros_like(original)

for (bbox, text, prob) in results:

    pts = np.array(
        bbox,
        dtype=np.int32
    )

    cv2.polylines(
        detection_view,
        [pts],
        True,
        (0, 255, 0),
        2
    )

# ==========================================
# Resize All Images
# ==========================================

w = 600
h = 400

original = cv2.resize(original, (w, h))
detection_view = cv2.resize(detection_view, (w, h))
ocr_boxes = cv2.resize(ocr_boxes, (w, h))
text_panel = cv2.resize(text_panel, (w, h))

# ==========================================
# Titles
# ==========================================

cv2.putText(original,
            "Original",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,255,0),
            2)

cv2.putText(detection_view,
            "Text Detection",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,255,0),
            2)

cv2.putText(ocr_boxes,
            "OCR Boxes",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,255,0),
            2)

cv2.putText(text_panel,
            "Extracted Text",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,255,0),
            2)

# ==========================================
# Create Summary
# ==========================================

top = np.hstack(
    [original, detection_view]
)

bottom = np.hstack(
    [ocr_boxes, text_panel]
)

summary = np.vstack(
    [top, bottom]
)

# ==========================================
# Save Results
# ==========================================

cv2.imwrite(
    "output/easyocr_summary.png",
    summary
)

cv2.imshow(
    "EasyOCR Summary",
    summary
)

cv2.waitKey(0)
cv2.destroyAllWindows()