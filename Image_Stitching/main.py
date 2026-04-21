import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


def open_files():
    """
    Opens file dialog → stores selected image paths
    """
    files = filedialog.askopenfilenames(title="Select Images")

    if len(files) < 2:
        messagebox.showerror("Error", "Please select at least two images")
        return

    image_paths.clear()  # clear old selections
    for file in files:
        image_paths.append(file)


def stitch_images():
    """
    Reads images → stitches using OpenCV → displays result
    """
    paths = image_paths

    if len(paths) < 2:
        messagebox.showerror("Error", "Please select at least two images")
        return

    images = []
    for path in paths:
        img = cv2.imread(path)
        if img is None:
            messagebox.showerror("Error", f"Could not read image: {path}")
            return
        images.append(img)

    # FIX: typo corrected
    stitcher = cv2.Stitcher_create()

    status, pano = stitcher.stitch(images)

    if status != cv2.Stitcher_OK:
        messagebox.showerror("Error", f"Stitching failed with status code: {status}")
        return

    display_image(pano)
    messagebox.showinfo("Success", "Images stitched successfully!")


def display_image(image):
    """
    Displays stitched image in Tkinter panel
    """
    cv_image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(cv_image_rgb)

    img_tk = ImageTk.PhotoImage(pil_image)

    panel.config(image=img_tk)
    panel.image = img_tk  # IMPORTANT: keep reference


# ---------------- GUI ----------------

root = tk.Tk()
root.title("Image Stitching with OpenCV")

# UI Variables
image_paths = []

# UI Elements
open_button = tk.Button(root, text="Open Images", command=open_files)
stitch_button = tk.Button(root, text="Stitch Images", command=stitch_images)
panel = tk.Label(root)

open_button.pack(pady=10)
stitch_button.pack(pady=10)
panel.pack(padx=10, pady=10)

root.mainloop()