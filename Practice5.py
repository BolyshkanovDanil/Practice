import sys
import cv2
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QLabel, QFileDialog, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

class ImageEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.image = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Image Editor')
        self.setGeometry(100, 100, 800, 600)

        # Метка для отображения изображения
        self.image_label = QLabel(self)
        self.image_label.resize(640, 480)
        self.image_label.move(80, 20)

        # Кнопки
        self.btn_load = QPushButton('Load Image', self)
        self.btn_load.move(50, 520)
        self.btn_load.clicked.connect(self.loadImage)

        self.btn_negative = QPushButton('Show Negative', self)
        self.btn_negative.move(160, 520)
        self.btn_negative.clicked.connect(self.showNegative)

        self.btn_rotate = QPushButton('Rotate Image', self)
        self.btn_rotate.move(290, 520)
        self.btn_rotate.clicked.connect(self.rotateImage)

        self.angle_input = QLineEdit(self)
        self.angle_input.setPlaceholderText('Enter rotation angle')
        self.angle_input.move(290, 550)

        self.btn_draw_circle = QPushButton('Draw Circle', self)
        self.btn_draw_circle.move(420, 520)
        self.btn_draw_circle.clicked.connect(self.drawCircle)

        self.circle_x_input = QLineEdit(self)
        self.circle_x_input.setPlaceholderText('X-coordinate')
        self.circle_x_input.move(420, 550)

        self.circle_y_input = QLineEdit(self)
        self.circle_y_input.setPlaceholderText('Y-coordinate')
        self.circle_y_input.move(520, 550)

        self.circle_radius_input = QLineEdit(self)
        self.circle_radius_input.setPlaceholderText('Radius')
        self.circle_radius_input.move(620, 550)

        self.show()

    def loadImage(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', '/home', "Image files (*.jpg *.png)")
        if fname:
            self.image = cv2.imread(fname)
            self.displayImage(self.image)

    def displayImage(self, img):
        qformat = QImage.Format_Indexed8 if len(img.shape) == 2 else QImage.Format_RGB888
        outImage = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
        outImage = outImage.rgbSwapped()
        self.image_label.setPixmap(QPixmap.fromImage(outImage))
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)

    def showNegative(self):
        if self.image is not None:
            negative = cv2.bitwise_not(self.image)
            self.displayImage(negative)

    def rotateImage(self):
        if self.image is not None:
            angle = float(self.angle_input.text())
            height, width = self.image.shape[:2]
            rotation_matrix = cv2.getRotationMatrix2D((width/2, height/2), angle, 1)
            rotated_image = cv2.warpAffine(self.image, rotation_matrix, (width, height))
            self.displayImage(rotated_image)

    def drawCircle(self):
        if self.image is not None:
            x = int(self.circle_x_input.text())
            y = int(self.circle_y_input.text())
            radius = int(self.circle_radius_input.text())
            circled_image = self.image.copy()
            cv2.circle(circled_image, (x, y), radius, (0, 0, 255), 2)
            self.displayImage(circled_image)

def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = ImageEditor()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
