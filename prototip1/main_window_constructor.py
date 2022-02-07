import libs

import logging
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QImage, QPixmap
from structure_ui import Structure_UI
from structure_ui_camera import Structure_Ui_Camera
from structure_camera import Camera_Object, CAMERA_FLAGS
import sys
import cv2
from qt_tools import numpy_To_QT_Type_Converter

class Ui_Camera_API_Main(Structure_UI):
    
    logger_level = logging.INFO

    def __init__(self, *args, obj=None, logger_level= logging.INFO, **kwargs):
        super(Ui_Camera_API_Main, self).__init__(*args, **kwargs)

        self.logger_level = logger_level
        self.init()
    

    def init(self):
        self.configure_Other_Settings()
    
    def connect_camera_button_triggered(self):
        print("test")

    
        

class Ui_Camera_API_Developer(Structure_Ui_Camera):
    logger_level = logging.INFO

    def __init__(self, *args, onj = None, logger_level = logging.INFO, **kwargs):
        super(Ui_Camera_API_Developer, self).__init__(*args, **"kwargs")

        self.logger_level = logger_level

        self.init()
    
    def init(self):
        self.configure_Other_Settings()

    def configure_Button_Connections(self):
        self.connect_camera_button.clicked.connect(
            lambda: self.connect_to_Camera(
                camera_flag=CAMERA_FLAGS.CV2
                
            )
        )

    def configure_Other_Settings(self):
        
        self.init_qt_graphicsView_Scene(
            self.frame_1,
        )
        self.init_qt_graphicsView_Scene(
            self.frame_2,
        )
        self.init_qt_graphicsView_Scene(
            self.frame_3,
        )
        self.init_qt_graphicsView_Scene(
            self.frame_4,
        )

    def closeEvent(self, *args, **kwargs):
        super(Ui_Camera_API_Developer, self).closeEvent(*args, **kwargs)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Ui_Camera_API_Main()
    sys.exit(app.exec_())