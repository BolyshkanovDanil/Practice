import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps
import cv2
from cv2 import VideoCapture

# Функция для загрузки изображения
def load_image():
    global img, imgtk, original
    file_path = filedialog.askopenfilename()
    if file_path:
        img = Image.open(file_path)
        original = img.copy()
        imgtk = ImageTk.PhotoImage(img)
        canvas.create_image(20, 20, anchor="nw", image=imgtk)
        canvas.config(width=img.width, height=img.height)

# Функция для захвата изображения с камеры
def capture_image():
    global img, imgtk, original
    cap = VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite("capture.jpg", frame)
        img = Image.open("capture.jpg")
        original = img.copy()
        imgtk = ImageTk.PhotoImage(img)
        canvas.create_image(20, 20, anchor="nw", image=imgtk)
        canvas.config(width=img.width, height=img.height)
    cap.release()

# Показ негатива изображения
def show_negative():
    global img, imgtk
    img = ImageOps.invert(img)
    imgtk = ImageTk.PhotoImage(img)
    canvas.create_image(20, 20, anchor="nw", image=imgtk)

# Вращение изображения
def rotate_image():
    global img, imgtk
    img = img.rotate(90, expand=True)
    imgtk = ImageTk.PhotoImage(img)
    canvas.create_image(20, 20, anchor="nw", image=imgtk)

# Рисование круга
def draw_circle():
    global img, imgtk
    x, y, r = 50, 50, 30  # Примерные координаты и радиус
    img_draw = ImageDraw.Draw(img)
    img_draw.ellipse((x-r, y-r, x+r, y+r), outline='red', width=5)
    imgtk = ImageTk.PhotoImage(img)
    canvas.create_image(20, 20, anchor="nw", image=imgtk)

# Очистка эффектов
def clear_effects():
    global img, imgtk, original
    img = original.copy()
    imgtk = ImageTk.PhotoImage(img)
    canvas.create_image(20, 20, anchor="nw", image=imgtk)

# Выход из программы
def exit_app():
    root.destroy()

# Основное окно приложения
root = tk.Tk()
root.title("Image Editor")

# Создаем холст для изображения
canvas = tk.Canvas(root, width=300, height=300)
canvas.pack()

# Кнопки для функций
btn_load = tk.Button(root, text="Загрузить изображение", command=load_image)
btn_load.pack(fill='x')

btn_capture = tk.Button(root, text="Загрузить изображение с камеры", command=capture_image)
btn_capture.pack(fill='x')

btn_negative = tk.Button(root, text="Показать негативное изображение", command=show_negative)
btn_negative.pack(fill='x')

btn_rotate = tk.Button(root, text="Вращение изображения", command=rotate_image)
btn_rotate.pack(fill='x')

btn_circle = tk.Button(root, text="Нарисовать красный круг", command=draw_circle)
btn_circle.pack(fill='x')

btn_clear = tk.Button(root, text="Clear", command=clear_effects)
btn_clear.pack(fill='x')

btn_exit = tk.Button(root, text="Exit", command=exit_app)
btn_exit.pack(fill='x')

root.mainloop()
