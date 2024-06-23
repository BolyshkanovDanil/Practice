import cv2
import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog, Tk, Button, Label, Entry

def show_image(img, title="Image"):
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def negative_image(img):
    return cv2.bitwise_not(img)

def rotate_image(img, angle):
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(img, M, (w, h))

def draw_circle(img, x, y, radius):
    return cv2.circle(img.copy(), (x, y), radius, (0, 0, 255), 2)

def load_image():
    Tk().withdraw()
    file_path = filedialog.askopenfilename()
    if file_path:
        img = cv2.imread(file_path)
        if img is None:
            print("Error loading image")
        else:
            show_image(img)
            return img
    else:
        print("No file selected")

def capture_image():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot access webcam")
        return None

    ret, frame = cap.read()
    cap.release()
    if not ret:
        print("Failed to capture image")
        return None

    show_image(frame)
    return frame

def show_channel(img, channel):
    channels = cv2.split(img)
    channel_img = np.zeros_like(img)
    channel_img[:, :, channel] = channels[channel]
    show_image(channel_img, f"Channel {channel}")

def main():
    root = Tk()
    root.title("Image Processing App")

    Button(root, text="Load Image", command=load_image).pack()
    Button(root, text="Capture Image", command=capture_image).pack()

    Label(root, text="Enter rotation angle:").pack()
    angle_entry = Entry(root)
    angle_entry.pack()

    Button(root, text="Rotate Image", command=lambda: show_image(rotate_image(load_image(), float(angle_entry.get())))).pack()

    Label(root, text="Enter circle parameters (x, y, radius):").pack()
    x_entry = Entry(root)
    x_entry.pack()
    y_entry = Entry(root)
    y_entry.pack()
    radius_entry = Entry(root)
    radius_entry.pack()

    Button(root, text="Draw Circle", command=lambda: show_image(draw_circle(load_image(), int(x_entry.get()), int(y_entry.get()), int(radius_entry.get())))).pack()

    root.mainloop()

if __name__ == "__main__":
    main()
