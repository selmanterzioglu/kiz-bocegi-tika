import libs

import logging
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QImage, QPixmap
from structure_ui import Structure_UI, Graphics_View
from structure_ui_camera import Structure_Ui_Camera
from structure_camera import Camera_Object, CAMERA_FLAGS
import sys
import cv2

# from qt_tools import numpy_To_QT_Type_Converter

class Ui_Camera_API_Main(Structure_UI):
    
    logger_level = logging.INFO

    def __init__(self, *args, obj=None, logger_level= logging.INFO, **kwargs):
        super(Ui_Camera_API_Main, self).__init__(*args, **kwargs)

        self.logger_level = logger_level

class Ui_Camera_API_Developer(Structure_Ui_Camera):
    logger_level = logging.INFO

    def __init__(self, *args, onj = None, logger_level = logging.INFO, **kwargs):
        super(Ui_Camera_API_Developer, self).__init__(*args, **kwargs)

        self.logger_level = logger_level
        self.camera_Instance = None


        self.q_timer_1 = self._qtimer_Create_And_Run(
            self,
            connection=self.qtimer_function_1,
            delay=10,
            is_needed_start=True,
            is_single_shot=False
        )

    def qtimer_function_1(self):
        if self.camera_Instance is not None:
            self.frame_1.set_Background_Image(self.camera_Instance.stream_Returner(auto_pop=True, pass_broken=True))
    
    
    def configure_Button_Connections(self):
        self.connect_camera_button.clicked.connect(            
            lambda: [
            self.connect_to_Camera(
                CAMERA_FLAGS.CV2,
                buffer_size=1000,
                exposure_time=40000,
                auto_configure = False
            ),
            self.camera_Instance.api_CV2_Camera_Create_Instance(4, extra_params = [])
            ]
        )
        self.remove_camera_button.clicked.connect(
            self.camera_Remove
        )

    def closeEvent(self, *args, **kwargs):
        super(Ui_Camera_API_Developer, self).closeEvent(*args, **kwargs)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Ui_Camera_API_Main()
    sys.exit(app.exec_())