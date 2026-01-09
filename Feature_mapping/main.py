"""
Feature Matching GUI using ORB (OpenCV)

This script provides a simple Tkinter-based GUI to:
1. Select two images from disk
2. Detect ORB features in both images
3. Match features using Brute Force Matcher
4. Visualize the best feature matches

Author: Jeshwanth Ganesh
"""

import cv2 as cv
import numpy as np
from tkinter import Tk, filedialog, Button, Label


# -----------------------------
# Global Variables
# -----------------------------
img1 = None
img2 = None
file_path1 = None
file_path2 = None


# -----------------------------
# Image Selection Functions
# -----------------------------
def select_image():
    """
    Opens a file dialog to select the first image.
    The image is loaded in grayscale for feature extraction.
    """
    global img1, file_path1

    file_path1 = filedialog.askopenfilename()
    if file_path1:
        img1 = cv.imread(file_path1, cv.IMREAD_GRAYSCALE)
        label_img1.config(text=f"Image 1: {file_path1.split('/')[-1]}")


def select_image2():
    """
    Opens a file dialog to select the second image.
    The image is loaded in grayscale for feature extraction.
    """
    global img2, file_path2

    file_path2 = filedialog.askopenfilename()
    if file_path2:
        img2 = cv.imread(file_path2, cv.IMREAD_GRAYSCALE)
        label_img2.config(text=f"Image 2: {file_path2.split('/')[-1]}")


# -----------------------------
# Feature Matching Logic
# -----------------------------
def feature_matching():
    """
    Detects ORB features in both selected images,
    matches them using Brute Force matcher,
    and displays the best matches.
    """
    if img1 is None or img2 is None:
        print("Please select both images first.")
        return

    # Initialize ORB detector
    orb = cv.ORB_create()

    # Detect keypoints and compute descriptors
    keypoints1, descriptor1 = orb.detectAndCompute(img1, None)
    keypoints2, descriptor2 = orb.detectAndCompute(img2, None)

    # Create Brute Force Matcher using Hamming distance
    bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)

    # Match descriptors
    matches = bf.match(descriptor1, descriptor2)

    # Sort matches by distance (lower = better)
    matches = sorted(matches, key=lambda x: x.distance)

    # Draw top 50 matches
    matched_image = cv.drawMatches(
        img1, keypoints1,
        img2, keypoints2,
        matches[:50],
        None,
        flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
    )

    # Display result
    cv.imshow("ORB Feature Matching", matched_image)
    cv.waitKey(0)
    cv.destroyAllWindows()


# -----------------------------
# Tkinter GUI Setup
# -----------------------------
root = Tk()
root.title("Feature Matching using ORB")

# Button: Select Image 1
btn_select_image1 = Button(root, text="Select Image 1", command=select_image)
btn_select_image1.pack(pady=5)

label_img1 = Label(root, text="Image 1: Not selected")
label_img1.pack()

# Button: Select Image 2
btn_select_image2 = Button(root, text="Select Image 2", command=select_image2)
btn_select_image2.pack(pady=5)

label_img2 = Label(root, text="Image 2: Not selected")
label_img2.pack()

# Button: Match Features
btn_match_features = Button(root, text="Match Features", command=feature_matching)
btn_match_features.pack(pady=10)

# Start GUI loop
root.mainloop()
