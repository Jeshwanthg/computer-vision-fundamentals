# Image Stitching (Panorama) using OpenCV

## Overview

This project creates a **panorama image** by stitching multiple overlapping images using OpenCV's built-in Stitcher.

A simple Tkinter GUI allows users to select images and generate the stitched output.

---

## Features

* Select multiple images via GUI
* Automatic feature detection & matching
* Image alignment and blending
* Panorama generation
* Result displayed in-app

---

## How It Works

1. Select multiple overlapping images
2. Images are read using OpenCV
3. OpenCV Stitcher:

   * detects features
   * matches them
   * aligns images
   * blends into panorama
4. Final stitched image is displayed

---

## Run

```bash
python main.py
```

---

## Folder Structure

```
image_stitching/
├── main.py
├── test1.jpg
├── test2.jpg
├── result.png
└── README.md
```

---

## Notes

* Images must have overlapping regions
* Works best with similar lighting and perspective
