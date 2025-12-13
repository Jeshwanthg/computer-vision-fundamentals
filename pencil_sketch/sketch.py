"""
Pencil Sketch Image Converter
-----------------------------
This script converts an input image into a pencil sketch using
classical image processing techniques and provides a simple GUI
using Tkinter to open, preview, and save images.

Technologies used:
- OpenCV (image processing)
- NumPy (array operations)
- Tkinter (GUI)
- PIL (image conversion for Tkinter)
"""

import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


# Dictionary to store PIL images so they are not garbage-collected
# and can later be saved to disk
images = {
    "original": None,
    "sketch": None
}


def open_file():
    """
    Opens a file dialog to select an image, converts it to a
    pencil sketch, and displays both original and sketch images.
    """
    filepath = filedialog.askopenfilename()
    if not filepath:
        return

    # Read image using OpenCV (BGR format)
    img = cv2.imread(filepath)

    # Display original image
    display_image(img, original=True)

    # Convert image to sketch
    sketch_image = convert_to_sketch(img)

    # Display sketch image
    display_image(sketch_image, original=False)


def convert_to_sketch(img):
    """
    Converts an image to a pencil sketch using the following steps:
    1. Convert to grayscale
    2. Invert grayscale image
    3. Apply Gaussian blur
    4. Invert blurred image
    5. Divide grayscale image by inverted blur

    Parameters:
        img (numpy.ndarray): Input BGR image

    Returns:
        numpy.ndarray: Pencil sketch image
    """

    # Step 1: Convert to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Step 2: Invert grayscale image
    inverted_img = cv2.bitwise_not(gray_img)

    # Step 3: Apply Gaussian blur to smooth the image
    blurred_img = cv2.GaussianBlur(inverted_img, (21, 21), 0)

    # Step 4: Invert the blurred image
    inverted_blur_img = cv2.bitwise_not(blurred_img)

    # Step 5: Divide grayscale image by inverted blur to get sketch
    sketch_img = cv2.divide(gray_img, inverted_blur_img, scale=256.0)

    return sketch_img


def display_image(img, original):
    """
    Displays an image in the Tkinter GUI.

    Parameters:
        img (numpy.ndarray): Image to display
        original (bool): True if original image, False if sketch
    """

    # Convert OpenCV image to RGB only if it's the original image
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) if original else img

    # Convert NumPy array to PIL Image
    img_pil = Image.fromarray(img_rgb)

    # Convert PIL Image to ImageTk for Tkinter
    img_tk = ImageTk.PhotoImage(image=img_pil)

    # Store image reference to prevent garbage collection
    if original:
        images["original"] = img_pil
        label = original_image_label
    else:
        images["sketch"] = img_pil
        label = sketch_image_label

    # Update the label with new image
    label.config(image=img_tk)
    label.image = img_tk


def save_sketch():
    """
    Saves the generated pencil sketch image to disk.
    """
    if images["sketch"] is None:
        messagebox.showerror("Error", "No sketch to save.")
        return

    filepath = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png")]
    )

    if not filepath:
        return

    images["sketch"].save(filepath, "PNG")
    messagebox.showinfo("Saved", f"Sketch saved to:\n{filepath}")


# ------------------- GUI SETUP -------------------

app = tk.Tk()
app.title("Pencil Sketch Converter")

# Frame for displaying images
frame = tk.Frame(app)
frame.pack(pady=10, padx=10)

original_image_label = tk.Label(frame)
original_image_label.grid(row=0, column=0, padx=5, pady=5)

sketch_image_label = tk.Label(frame)
sketch_image_label.grid(row=0, column=1, padx=5, pady=5)

# Frame for buttons
btn_frame = tk.Frame(app)
btn_frame.pack(pady=10)

open_button = tk.Button(btn_frame, text="Open Image", command=open_file)
open_button.grid(row=0, column=0, padx=5)

save_button = tk.Button(btn_frame, text="Save Sketch", command=save_sketch)
save_button.grid(row=0, column=1, padx=5)

# Start GUI loop
app.mainloop()
