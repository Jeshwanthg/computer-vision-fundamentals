# Pencil Sketch Image Converter 🎨✏️

A simple Computer Vision project that converts a normal image into
a pencil sketch using classical image processing techniques.
The application includes a GUI built with Tkinter to open, preview,
and save images.

---

## 📌 Project Objective

The goal of this project is to demonstrate:
- Fundamental image processing techniques
- Pixel-wise image operations
- Integration of OpenCV with a GUI
- Non-photorealistic rendering (pencil sketch effect)

---

## 🧠 How the Pencil Sketch Effect Works

The sketch effect is created using the following pipeline:

1. Convert the image to grayscale  
2. Invert the grayscale image  
3. Apply Gaussian blur to smooth details  
4. Invert the blurred image  
5. Divide the grayscale image by the inverted blur  

This process enhances edges and produces a hand-drawn pencil effect.

---

## 🛠️ Technologies Used

- **Python**
- **OpenCV** – Image processing
- **NumPy** – Numerical operations
- **Tkinter** – GUI interface
- **Pillow (PIL)** – Image handling for Tkinter

---

## 📂 Project Structure

---

<img width="835" height="174" alt="image" src="https://github.com/user-attachments/assets/8a020c52-970a-4541-8015-bfc654f4940a" />

---

## ▶️ How to Run

1. Install dependencies:
```bash
pip install opencv-python numpy pillow
```
2. Run the script:

python sketch.py

3.Use the GUI to:

- Open an image
- View original and sketch side-by-side
- Save the sketch output

---
  

---
