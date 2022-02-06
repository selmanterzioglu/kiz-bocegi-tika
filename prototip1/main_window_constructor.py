from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys
import cv2
import numpy as np

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        
        uic.loadUi('main_window.ui', self)
        self.show()


    def clicked_function(self):
        print("test")

        img = cv2.imread("test.png", 0)
        # a = Graphics_View(self.frame_1)
        
        # cv2.imshow(img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
      
class Graphics_View(QGraphicsView): 
    def __init__(self, *args, parent=None, obj=None, **kwargs):
        super(Graphics_View, self).__init__(*args, **kwargs)
        self.current_Frame = None
        self.setScene(QGraphicsScene(parent=parent))
        
    def set_Scene(self, parent=None, scene=None):
        self.setScene(QGraphicsScene(parent=parent) if scene is None else scene)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())