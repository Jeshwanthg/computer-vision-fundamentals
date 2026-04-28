# Line Detection using Hough Transform 

## Overview

This project detects straight lines in an image using:

* Canny Edge Detection
* Hough Line Transform

A simple GUI allows users to adjust thresholds and visualize results.

---

## Features

* Image selection via GUI
* Adjustable Canny edge threshold
* Adjustable Hough transform threshold
* Line detection and visualization

---

## How It Works

1. Load image
2. Convert to grayscale
3. Detect edges using Canny
4. Apply Hough Transform
5. Draw detected lines

---

## Run

```bash id="kcb59k"
python main.py
```

---

## Requirements

```bash id="yd5l9i"
pip install opencv-python numpy
```

---

## Notes

* Works best on images with clear edges
* Threshold tuning is important for accuracy
* Detects infinite straight lines (not segments)
