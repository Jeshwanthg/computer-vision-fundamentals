# Image Enhancement using OpenCV

## Overview

This project demonstrates two fundamental image enhancement techniques:

1. Noise Addition and Noise Removal
2. Histogram Equalization

The project explores how image quality can be improved through denoising and contrast enhancement.

---

## Features

* Artificial Noise Generation
* Non-Local Means Denoising
* Histogram Visualization
* Cumulative Distribution Function (CDF)
* Histogram Equalization
* Contrast Enhancement

---

## Technologies Used

* Python
* OpenCV
* NumPy
* Matplotlib

---

## Project Structure

```text
image_enhancement/
│
├── images/
│   ├── londonxmas.jpeg
│   └── soaps.jpeg
│
├── output/
│   ├── noisy_image.jpg
│   ├── denoised_image.jpg
│   ├── histogram_before.png
│   ├── histogram_after.png
│   └── equalized_image.jpg
│
├── main.py
└── README.md
```

---

## Installation

```bash
pip install opencv-python numpy matplotlib
```

---

## Run

```bash
python main.py
```

---

## Part 1: Noise Removal

### Workflow

```text
Original Image
      ↓
Add Random Noise
      ↓
Non-Local Means Denoising
      ↓
Clean Image
```

### OpenCV Function

```python
cv2.fastNlMeansDenoisingColored()
```

---

## Part 2: Histogram Equalization

### Workflow

```text
Original Image
      ↓
Convert to Grayscale
      ↓
Compute Histogram
      ↓
Apply Histogram Equalization
      ↓
Enhanced Contrast
```

### OpenCV Function

```python
cv2.equalizeHist()
```
### Histogram Before Equalization

![Before](Image_enhancement/output/histogram_before.png)

### Histogram After Equalization

![After](Image_enhancement/output/histogram_after.png)
---

## Results

![Summary](Image_enhancement/output/project_summary.png)

---

## Applications

* OCR Preprocessing
* Medical Imaging
* Satellite Image Processing
* Face Recognition
* Autonomous Driving
* Surveillance Systems

---

## Concepts Demonstrated

* Image Noise
* Denoising Algorithms
* Histogram Analysis
* Contrast Enhancement
* Cumulative Distribution Function (CDF)
* Image Preprocessing

---

## Future Improvements

* CLAHE (Adaptive Histogram Equalization)
* Gaussian Noise Removal
* Median Filtering
* Bilateral Filtering
* Real-Time Image Enhancement

---
