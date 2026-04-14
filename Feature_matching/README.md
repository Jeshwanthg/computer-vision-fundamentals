🔍 Feature Matching using ORB (OpenCV + Tkinter)

A simple GUI-based Python application that performs feature detection and matching between two images using ORB (Oriented FAST and Rotated BRIEF) and Brute Force matching.

This project demonstrates fundamental computer vision concepts such as:

- Keypoint detection
- Feature descriptors
- Feature matching
- GUI integration with OpenCV

'''

🛠️ Requirements:

Install dependencies:
pip install -r requirements.py

'''

🖥️ How It Works
1️⃣ Select Images

- Click Select Image 1
- Click Select Image 2
- Images are loaded in grayscale for feature extraction

2️⃣ Feature Detection

ORB detects keypoints and computes descriptors for both images

3️⃣ Feature Matching

- Brute Force Matcher with Hamming distance
- Matches are sorted by distance (best matches first)

4️⃣ Visualization

- Top 50 matches are drawn and displayed using OpenCV
