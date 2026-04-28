import cv2
import numpy as np
from tkinter import filedialog, Tk, Label, Button, Scale, HORIZONTAL


class LineDetectionApp:
    """
    GUI Application for detecting straight lines in an image
    using Canny Edge Detection + Hough Transform.
    """

    def __init__(self, root):
        """
        Initializes the GUI components and layout.

        Components:
        - Label: Instructions / status
        - Button: Image selection
        - Sliders: Threshold tuning
        - Button: Trigger detection
        """
        self.root = root
        self.root.title("Hough Transform for Line Detection")

        # Instruction label
        self.label = Label(root, text="Select an image to detect lines")
        self.label.pack()

        # Button to select image
        self.select_button = Button(root, text="Select Image", command=self.select_image)
        self.select_button.pack()

        # Canny edge threshold slider
        self.canny_scale = Scale(
            root,
            from_=50,
            to=150,
            orient=HORIZONTAL,
            label="Canny Threshold"
        )
        self.canny_scale.set(100)
        self.canny_scale.pack()

        # Hough transform threshold slider
        self.hough_scale = Scale(
            root,
            from_=50,
            to=200,
            orient=HORIZONTAL,
            label="Hough Threshold"
        )
        self.hough_scale.set(100)
        self.hough_scale.pack()

        # Button to detect lines
        self.detect_button = Button(root, text="Detect Lines", command=self.detect_lines)
        self.detect_button.pack()

        # Store selected image path
        self.image_path = None

    def select_image(self):
        """
        Opens file dialog and stores selected image path.
        Updates label with selected file name.
        """
        self.image_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")]
        )

        self.label.config(text=f"Selected image: {self.image_path}")

    def detect_lines(self):
        """
        Performs line detection using Hough Transform.

        Pipeline:
        1. Load image
        2. Convert to grayscale
        3. Detect edges (Canny)
        4. Detect lines (Hough Transform)
        5. Draw detected lines
        6. Display result
        """
        if not self.image_path:
            self.label.config(text="No image selected!")
            return

        # Load image
        image = cv2.imread(self.image_path)

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Edge detection using Canny
        edges = cv2.Canny(
            gray,
            self.canny_scale.get(),
            self.canny_scale.get() * 2
        )

        # Hough Line Transform
        lines = cv2.HoughLines(
            edges,
            1,                  # Distance resolution (pixels)
            np.pi / 180,        # Angle resolution (radians)
            self.hough_scale.get()  # Threshold (votes)
        )

        # Draw detected lines
        if lines is not None:
            for rho, theta in lines[:, 0]:
                a = np.cos(theta)
                b = np.sin(theta)

                # Convert polar to Cartesian
                x0 = a * rho
                y0 = b * rho

                # Create long line for visualization
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * (a))
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * (a))

                cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Display result
        cv2.imshow("Detected Lines", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


# -----------------------------
# Entry Point
# -----------------------------
if __name__ == "__main__":
    root = Tk()
    app = LineDetectionApp(root)
    root.mainloop()