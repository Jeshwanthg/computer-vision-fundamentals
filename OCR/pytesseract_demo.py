import os
import cv2
import numpy as np
import pytesseract
from pytesseract import Output
from skimage.filters import threshold_local

# ==========================================
# Tesseract Path
# ==========================================

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# ==========================================
# Create Output Folder
# ==========================================

os.makedirs("output", exist_ok=True)

# ==========================================
# Load Image
# ==========================================

image = cv2.imread("images/test.png")

if image is None:
    raise FileNotFoundError(
        "Could not load images/test.png"
    )

original = image.copy()

# ==========================================
# Preprocessing
# ==========================================

# Convert to HSV
hsv = cv2.cvtColor(
    image,
    cv2.COLOR_BGR2HSV
)

# Extract Value channel
V = cv2.split(hsv)[2]

# Adaptive Threshold
T = threshold_local(
    V,
    25,
    offset=15,
    method="gaussian"
)

thresh = (V > T).astype("uint8") * 255

# Save threshold image
# cv2.imwrite(
#     "output/threshold.png",
#     thresh
# )

# ==========================================
# OCR Text Extraction
# ==========================================

output_txt = pytesseract.image_to_string(
    thresh
)

print("\nExtracted Text:\n")
print(output_txt)

# Save extracted text
with open(
    "output/pytesseract_text.txt",
    "w",
    encoding="utf-8"
) as f:
    f.write(output_txt)

# ==========================================
# OCR Bounding Boxes
# ==========================================

data = pytesseract.image_to_data(
    thresh,
    output_type=Output.DICT
)

n_boxes = len(data["text"])

for i in range(n_boxes):

    try:
        conf = float(
            data["conf"][i]
        )
    except:
        continue

    if conf > 60:

        x = data["left"][i]
        y = data["top"][i]
        w = data["width"][i]
        h = data["height"][i]

        cv2.rectangle(
            image,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

# Save OCR boxes image
# cv2.imwrite(
#     "output/ocr_boxes.png",
#     image
# )

# ==========================================
# Create GitHub Summary Image
# ==========================================

# Convert threshold image to color
thresh_bgr = cv2.cvtColor(
    thresh,
    cv2.COLOR_GRAY2BGR
)

# White canvas for extracted text
text_panel = np.ones(
    (
        original.shape[0],
        original.shape[1],
        3
    ),
    dtype=np.uint8
) * 255

# Write extracted text
y = 40

for line in output_txt.split("\n"):

    if line.strip():

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

# Resize all images
w = 600
h = 400

original = cv2.resize(
    original,
    (w, h)
)

thresh_bgr = cv2.resize(
    thresh_bgr,
    (w, h)
)

ocr_boxes = cv2.resize(
    image,
    (w, h)
)

text_panel = cv2.resize(
    text_panel,
    (w, h)
)

# Add titles

cv2.putText(
    original,
    "Original",
    (20, 40),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    (0, 255, 0),
    2
)

cv2.putText(
    thresh_bgr,
    "Threshold",
    (20, 40),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    (0, 255, 0),
    2
)

cv2.putText(
    ocr_boxes,
    "OCR Boxes",
    (20, 40),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    (0, 255, 0),
    2
)

cv2.putText(
    text_panel,
    "Extracted Text",
    (20, 40),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    (0, 255, 0),
    2
)

# Create 2x2 grid

top_row = np.hstack(
    [original, thresh_bgr]
)

bottom_row = np.hstack(
    [ocr_boxes, text_panel]
)

summary = np.vstack(
    [top_row, bottom_row]
)

# Save summary image
cv2.imwrite(
    "output/pytesseract_summary.png",
    summary
)

# ==========================================
# Display Results
# ==========================================

cv2.imshow(
    "Pytesseract Summary",
    summary
)

cv2.waitKey(0)
cv2.destroyAllWindows()

print("\nResults saved to output/")