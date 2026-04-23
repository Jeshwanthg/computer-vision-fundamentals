import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import Scale, HORIZONTAL, Button


# -----------------------------
# Global Variables
# -----------------------------
img = None            # Original loaded image
img_display = None    # Transformed image to display


# -----------------------------
# Load Image Function
# -----------------------------
def load_image():
    """
    Opens a file dialog to select an image from disk.

    Steps:
    1. Opens file explorer
    2. Reads image using OpenCV
    3. Triggers transformation pipeline

    Notes:
    - Image is loaded in color (BGR format)
    - If no file is selected, function exits safely
    """
    global img, img_display

    filepath = filedialog.askopenfilename()
    if not filepath:
        return  # User cancelled file selection

    img = cv2.imread(filepath, cv2.IMREAD_COLOR)

    if img is not None:
        apply_transformations()


# -----------------------------
# Morphological Transformation
# -----------------------------
def apply_transformations(*args):
    """
    Applies selected morphological operation on the image.

    Pipeline:
    1. Get kernel size from UI slider
    2. Create kernel matrix
    3. Apply selected operation
    4. Display result

    Parameters:
    - *args: Required for Tkinter callbacks (ignored)

    Notes:
    - Uses real-time UI updates
    - Uses non-blocking display (waitKey(1))
    """
    global img, img_display

    if img is None:
        return  # No image loaded

    # Get kernel size from slider
    kernel_size = kernel_scale.get()

    # Get selected operation from dropdown
    operation = var.get()

    # Create square kernel
    kernel = np.ones((kernel_size, kernel_size), np.uint8)

    # Apply morphological operation
    if operation == "Erosion":
        transformed_img = cv2.erode(img, kernel, iterations=1)

    elif operation == "Dilation":
        transformed_img = cv2.dilate(img, kernel, iterations=1)

    elif operation == "Opening":
        transformed_img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

    elif operation == "Closing":
        transformed_img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

    elif operation == "Gradient":
        transformed_img = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)

    elif operation == "Top Hat":
        transformed_img = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)

    elif operation == "Black Hat":
        transformed_img = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernel)

    # Store result
    img_display = transformed_img

    # Display result (non-blocking)
    cv2.imshow("Morphological Transformation", img_display)
    cv2.waitKey(1)


# -----------------------------
# GUI Setup
# -----------------------------
root = tk.Tk()
root.title("Morphological Transformations")

# Dropdown options
OPTIONS = [
    "Erosion",
    "Dilation",
    "Opening",
    "Closing",
    "Gradient",
    "Top Hat",
    "Black Hat"
]

# Dropdown menu variable
var = tk.StringVar(root)
var.set(OPTIONS[0])

# Dropdown menu UI
operation_menu = tk.OptionMenu(root, var, *OPTIONS)
operation_menu.pack(pady=5)

# Kernel size slider
kernel_scale = Scale(
    root,
    from_=1,
    to=20,
    orient=HORIZONTAL,
    label="Kernel Size"
)
kernel_scale.set(5)
kernel_scale.pack()

# Load image button
load_button = Button(root, text="Load Image", command=load_image)
load_button.pack(pady=10)

# -----------------------------
# Event Bindings
# -----------------------------

# Update transformation when slider is released
kernel_scale.bind("<ButtonRelease-1>", apply_transformations)

# Update transformation when operation changes
var.trace("w", apply_transformations)

# -----------------------------
# Start Application
# -----------------------------
root.mainloop()

# Cleanup OpenCV windows
cv2.destroyAllWindows()