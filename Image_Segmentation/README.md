Image Segmentation using Watershed (OpenCV)

Overview:

-  This project implements image segmentation using the Watershed algorithm with a simple Tkinter GUI.
-  The user can select an image, and the program segments objects by detecting boundaries.

---

Features: 
-  GUI-based image selection
-  Automatic thresholding (Otsu)
-  Noise removal using morphology
- Foreground & background separation
-  Watershed segmentation
-  Boundary visualization

---

How It Works: 
1. Convert image to grayscale
2. Apply Otsu thresholding
3. Remove noise (morphological opening)
4. Identify:
    - Sure foreground
    - Sure background
5. Compute unknown region
6. Label markers
7. Apply Watershed algorithm
8. Draw boundaries on segmented regions

---

Run:

python main.py

---
