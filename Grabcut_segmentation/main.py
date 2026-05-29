"""
GrabCut Foreground Extraction using OpenCV

This project demonstrates foreground segmentation using the GrabCut algorithm.

Pipeline:
1. Load image
2. Define Region of Interest (ROI) using a rectangle
3. Initialize GrabCut
4. Estimate foreground and background
5. Generate segmentation mask
6. Extract foreground object

"""

import cv2
import numpy as np
from matplotlib import pyplot as plt


# --------------------------------------------------
# Display Function
# --------------------------------------------------
def imshow(title="Image", image=None, size=8):
    """
    Displays an image using Matplotlib.

    Parameters:
    ----------
    title : str
        Window title

    image : ndarray
        Image to display

    size : int
        Figure size scaling factor
    """
    h, w = image.shape[:2]
    aspect_ratio = h / w

    plt.figure(figsize=(size, size * aspect_ratio))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis("off")
    plt.show()


# --------------------------------------------------
# Load Image
# --------------------------------------------------
image = cv2.imread("woman.jpeg")

if image is None:
    raise FileNotFoundError("Could not load image.")

copy = image.copy()


# --------------------------------------------------
# Create GrabCut Data Structures
# --------------------------------------------------

# Mask stores pixel labels used by GrabCut
mask = np.zeros(image.shape[:2], np.uint8)

# Internal background model used by GrabCut
bgdModel = np.zeros((1, 65), np.float64)

# Internal foreground model used by GrabCut
fgdModel = np.zeros((1, 65), np.float64)


# --------------------------------------------------
# Define ROI (Region of Interest)
# --------------------------------------------------
# Rectangle should contain the object to extract

x1, y1 = 190, 70
x2, y2 = 350, 310

start = (x1, y1)
end = (x2, y2)

# Format: (x, y, width, height)
rect = (x1, y1, x2 - x1, y2 - y1)

# Visualize selected region
cv2.rectangle(copy, start, end, (0, 0, 255), 3)

imshow("Input Image with ROI", copy)


# --------------------------------------------------
# Run GrabCut
# --------------------------------------------------
cv2.grabCut(
    image,
    mask,
    rect,
    bgdModel,
    fgdModel,
    5,
    cv2.GC_INIT_WITH_RECT
)


# --------------------------------------------------
# Convert GrabCut Mask
# --------------------------------------------------
"""
Mask Labels:

0 = Definite Background
1 = Definite Foreground
2 = Probable Background
3 = Probable Foreground

Keep:
    1 and 3

Remove:
    0 and 2
"""

mask2 = np.where(
    (mask == 0) | (mask == 2),
    0,
    1
).astype("uint8")


# --------------------------------------------------
# Extract Foreground
# --------------------------------------------------
segmented_image = image * mask2[:, :, np.newaxis]


# --------------------------------------------------
# Display Results Together
# --------------------------------------------------

fig, ax = plt.subplots(1, 3, figsize=(15, 5))

# GrabCut mask (4 classes)
ax[0].imshow(mask * 80, cmap="gray")
ax[0].set_title("GrabCut Mask")
ax[0].axis("off")

# Binary foreground mask
ax[1].imshow(mask2 * 255, cmap="gray")
ax[1].set_title("Binary Mask")
ax[1].axis("off")

# Final segmented image
ax[2].imshow(cv2.cvtColor(segmented_image, cv2.COLOR_BGR2RGB))
ax[2].set_title("Segmented Output")
ax[2].axis("off")

plt.tight_layout()
plt.savefig("grabcut_results.png", bbox_inches="tight")