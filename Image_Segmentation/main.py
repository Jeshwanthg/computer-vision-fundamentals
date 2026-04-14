import cv2 
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import Button, Label


def select_image():
    """
    Opens file dialog → loads image → converts to grayscale → calls segmentation
    """
    file_path = filedialog.askopenfilename()
    if not file_path:
        return

    image = cv2.imread(file_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    segment_image(image)


def segment_image(image):
    """
    Performs watershed-based image segmentation
    """

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Otsu thresholding (binary inverse)
    _, thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    # Noise removal using morphological opening
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

    # Sure background (dilation)
    sure_bg = cv2.dilate(opening, kernel, iterations=3)

    # Distance transform → helps find object centers
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)

    # Threshold to get sure foreground
    _, sure_fg = cv2.threshold(
        dist_transform, 0.7 * dist_transform.max(), 255, 0
    )
    sure_fg = np.uint8(sure_fg)

    # Unknown region (boundary)
    unknown = cv2.subtract(sure_bg, sure_fg)

    # Marker labeling
    ret, markers = cv2.connectedComponents(sure_fg)

    # Increment markers so background is not 0
    markers = markers + 1

    # Mark unknown regions as 0
    markers[unknown == 255] = 0

    # Apply watershed algorithm
    markers = cv2.watershed(image, markers)

    # Mark boundaries in red
    image[markers == -1] = [255, 0, 0]

    dsiplay_segmented_image(image)


def dsiplay_segmented_image(segmented_image):
    """
    Displays the segmented image
    """
    cv2.imshow(
        "Segmented Image",
        cv2.cvtColor(segmented_image, cv2.COLOR_RGB2BGR)
    )
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# ---------------- GUI ----------------

app = tk.Tk()
app.title("Image Segmentation Tool")

label = Label(app, text="Select an image to segment:")
label.pack(pady=10)

select_button = Button(app, text="Select Image", command=select_image)
select_button.pack(pady=10)

app.geometry("300x150")
app.mainloop()