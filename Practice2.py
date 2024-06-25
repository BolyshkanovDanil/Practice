import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageOps
import cv2
import numpy as np

class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor")

        self.image_label = tk.Label(root)
        self.image_label.pack()

        self.load_image_button = tk.Button(root, text="Загрузить изображение", command=self.load_image)
        self.load_image_button.pack()

        self.capture_image_button = tk.Button(root, text="Загрузить изображение с камеры", command=self.capture_image)
        self.capture_image_button.pack()

        self.channel_var = tk.StringVar()
        self.channel_var.set("red")
        self.channel_menu = tk.OptionMenu(root, self.channel_var, "red", "green", "blue")
        self.channel_menu.pack()

        self.show_channel_button = tk.Button(root, text="Показать канал", command=self.show_channel)
        self.show_channel_button.pack()

        self.show_negative_button = tk.Button(root, text="Показать негативное изображение", command=self.show_negative)
        self.show_negative_button.pack()

        self.rotate_angle_entry = tk.Entry(root)
        self.rotate_angle_entry.pack()
        self.rotate_button = tk.Button(root, text="Вращение изображения", command=self.rotate_image)
        self.rotate_button.pack()

        self.circle_coords_entry = tk.Entry(root)
        self.circle_coords_entry.pack()
        self.circle_diameter_entry = tk.Entry(root)
        self.circle_diameter_entry.pack()
        self.draw_circle_button = tk.Button(root, text="Нарисовать красный круг", command=self.draw_circle)
        self.draw_circle_button.pack()

        self.clear_button = tk.Button(root, text="Clear", command=self.clear_effects)
        self.clear_button.pack()

        self.exit_button = tk.Button(root, text="Exit", command=root.quit)
        self.exit_button.pack()

        self.original_image = None
        self.display_image = None

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png")])
        if file_path:
            try:
                self.original_image = Image.open(file_path)
                self.display_image = self.original_image.copy()
                self.show_image()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить изображение: {e}")

    def capture_image(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Ошибка", "Не удалось подключиться к веб-камере.")
            return

        ret, frame = cap.read()
        cap.release()

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.original_image = Image.fromarray(frame)
            self.display_image = self.original_image.copy()
            self.show_image()
        else:
            messagebox.showerror("Ошибка", "Не удалось сделать снимок.")

    def show_image(self):
        img = ImageTk.PhotoImage(self.display_image)
        self.image_label.config(image=img)
        self.image_label.image = img

    def show_channel(self):
        if self.original_image:
            channel = self.channel_var.get()
            if channel == "red":
                channel_img = np.array(self.original_image)[:, :, 0]
            elif channel == "green":
                channel_img = np.array(self.original_image)[:, :, 1]
            elif channel == "blue":
                channel_img = np.array(self.original_image)[:, :, 2]
            self.display_image = Image.fromarray(channel_img)
            self.show_image()

    def show_negative(self):
        if self.original_image:
            self.display_image = ImageOps.invert(self.original_image)
            self.show_image()

    def rotate_image(self):
        if self.original_image:
            try:
                angle = float(self.rotate_angle_entry.get())
                self.display_image = self.original_image.rotate(angle)
                self.show_image()
            except ValueError:
                messagebox.showerror("Ошибка", "Пожалуйста, введите корректное значение угла.")

    def draw_circle(self):
        if self.original_image:
            try:
                coords = [int(x) for x in self.circle_coords_entry.get().split(",")]
                diameter = int(self.circle_diameter_entry.get())
                draw = ImageDraw.Draw(self.display_image)
                draw.ellipse((coords[0], coords[1], coords[0] + diameter, coords[1] + diameter), outline="red", width=2)
                self.show_image()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось нарисовать круг: {e}")

    def clear_effects(self):
        if self.original_image:
            self.display_image = self.original_image.copy()
            self.show_image()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()
