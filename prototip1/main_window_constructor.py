from PyQt5.QtWidgets import *
import libs

from PyQt5 import uic
from PyQt5.QtGui import QImage, QPixmap
import sys
import cv2
from cv2 import imread
import numpy as np
from qt_tools import numpy_To_QT_Type_Converter

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('main_window.ui', self)
        self.show()

        self.frame_1.setScene(QGraphicsScene())

    def clicked_function(self):
        
        self.label1.setText("said")
        img = imread("test.png", 0)
        # img = QPixmap("test.png")
        img = numpy_To_QT_Type_Converter(img)
        self.frame_1.scene().addPixmap(img)


# class Graphics_View(QGraphicsView): 
#     def __init__(self, *args, parent=None, obj=None, **kwargs):
#         super(Graphics_View, self).__init__(*args, **kwargs)
#         self.current_Frame = None
#         self.setScene(QGraphicsScene(parent=parent))
        
#     def set_Scene(self, parent=None, scene=None):
#         self.setScene(QGraphicsScene(parent=parent) if scene is None else scene)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())