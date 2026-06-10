import os
import random
import cv2
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# Create Output Folder
# ==========================================

os.makedirs("output", exist_ok=True)

# ==========================================
# Helper Function
# ==========================================

def save_histogram(image, filename, title):

    hist, bins = np.histogram(
        image.flatten(),
        256,
        [0, 256]
    )

    cdf = hist.cumsum()

    cdf_normalized = (
        cdf * float(hist.max()) / cdf.max()
    )

    plt.figure(figsize=(8, 5))

    plt.plot(
        cdf_normalized,
        color="b",
        label="CDF"
    )

    plt.hist(
        image.flatten(),
        256,
        [0, 256],
        color="r",
        alpha=0.7,
        label="Histogram"
    )

    plt.title(title)
    plt.xlim([0, 256])
    plt.legend()

    plt.savefig(filename)
    plt.close()


# ==========================================
# Noise Addition Function
# ==========================================

def add_white_noise(image):

    noisy = image.copy()

    prob = 0.01

    rnd = np.random.rand(
        noisy.shape[0],
        noisy.shape[1]
    )

    noisy[rnd < prob] = np.random.randint(
        50,
        230
    )

    return noisy


# ==========================================
# PART 1
# Noise Addition and Removal
# ==========================================

print("Running Noise Removal...")

image = cv2.imread(
    "images/londonxmas.png"
)

if image is None:
    raise FileNotFoundError(
        "images/londonxmas.png not found"
    )

# Add Noise
noisy_image = add_white_noise(
    image
)

# Remove Noise
denoised_image = cv2.fastNlMeansDenoisingColored(
    noisy_image,
    None,
    20,
    20,
    7,
    21
)

# Save Results
cv2.imwrite(
    "output/noisy_image.jpg",
    noisy_image
)

cv2.imwrite(
    "output/denoised_image.jpg",
    denoised_image
)

# ==========================================
# PART 2
# Histogram Equalization
# ==========================================

print("Running Histogram Equalization...")

img = cv2.imread(
    "images/soaps.png"
)

if img is None:
    raise FileNotFoundError(
        "images/soaps.png not found"
    )

gray = cv2.cvtColor(
    img,
    cv2.COLOR_BGR2GRAY
)

# Save histogram before
save_histogram(
    gray,
    "output/histogram_before.png",
    "Histogram Before Equalization"
)

# Equalize Histogram
equalized = cv2.equalizeHist(
    gray
)

# Save histogram after
save_histogram(
    equalized,
    "output/histogram_after.png",
    "Histogram After Equalization"
)

# Save equalized image
cv2.imwrite(
    "output/equalized_image.jpg",
    equalized
)

# ==========================================
# Create GitHub Summary Image
# ==========================================

# Resize images
w = 600
h = 400

original_noise = cv2.resize(
    image,
    (w, h)
)

noisy_image = cv2.resize(
    noisy_image,
    (w, h)
)

denoised_image = cv2.resize(
    denoised_image,
    (w, h)
)

equalized_bgr = cv2.cvtColor(
    equalized,
    cv2.COLOR_GRAY2BGR
)

equalized_bgr = cv2.resize(
    equalized_bgr,
    (w, h)
)

# Add labels

cv2.putText(
    original_noise,
    "Original",
    (20, 40),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    (0, 255, 0),
    2
)

cv2.putText(
    noisy_image,
    "Noise Added",
    (20, 40),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    (0, 255, 0),
    2
)

cv2.putText(
    denoised_image,
    "Noise Removed",
    (20, 40),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    (0, 255, 0),
    2
)

cv2.putText(
    equalized_bgr,
    "Histogram Equalized",
    (20, 40),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    (0, 255, 0),
    2
)

# Build summary grid

top_row = np.hstack([
    original_noise,
    noisy_image
])

bottom_row = np.hstack([
    denoised_image,
    equalized_bgr
])

summary = np.vstack([
    top_row,
    bottom_row
])

cv2.imwrite(
    "output/project_summary.png",
    summary
)

print("\nResults saved to output/")
print("project_summary.png")