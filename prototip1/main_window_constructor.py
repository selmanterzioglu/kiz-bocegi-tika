import libs

import logging
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QImage, QPixmap
from structure_ui import Structure_UI, Graphics_View
from structure_ui_camera import Structure_Ui_Camera
from structure_camera import Camera_Object, CAMERA_FLAGS
from structure_system import System_Object
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
        system_o = System_Object()
        print(system_o.thread_print_info())
        # system_o.thread_print_info()

        self.cam_2 = Camera_Object(
            camera_flag=CAMERA_FLAGS.CV2,
            auto_configure=False,
            trigger_quit=None,
            trigger_pause=None,
            lock_until_done=False,
            acquisition_framerate=30,
            # exposure_time=exposure_time,
            # max_buffer_limit=buffer_size,
            max_buffer_limit=20
            # logger_level=self.logger_level
        )

        
        self.q_timer_1 = self._qtimer_Create_And_Run(
            self,
            connection=self.qtimer_function_1,
            delay=10,
            is_needed_start=True,
            is_single_shot=False
        )

        self.q_timer_2 = self._qtimer_Create_And_Run(
            self,
            connection=self.qtimer_function_2,
            delay=10,
            is_needed_start=True,
            is_single_shot=False
        )

        self.init()
    
    def init(self):
        self.configure_Other_Settings()


    def configure_Other_Settings(self):
        # self.label.setText(self.get_camera_available_port())
        pass

    def qtimer_function_1(self):
        if self.camera_Instance is not None:
            self.frame_1.set_Background_Image(self.camera_Instance.stream_Returner(auto_pop=True, pass_broken=True))
    
    def qtimer_function_2(self):
        if self.cam_2 is not None:
            self.frame_2.set_Background_Image(self.cam_2.stream_Returner(auto_pop=True, pass_broken=True))
    
    
    def configure_Button_Connections(self):
        self.connect_camera_button.clicked.connect(            
            lambda: [
                self.connect_to_Camera(
                    CAMERA_FLAGS.CV2,
                    buffer_size=1000,
                    exposure_time=40000,
                    auto_configure = False
                ),
                self.camera_Instance.api_CV2_Camera_Create_Instance(
                    # self.spinBox_Camera_Selector.value(), 
                    6,
                    extra_params=[]
                ),
                
                self.cam_2.api_CV2_Camera_Create_Instance(4, extra_params = []),
                
                self.cam_2.stream_Start_Thread(
                        number_of_snapshot=1000,
                        delay=0.001,
                        trigger_pause=self.is_Stream_Active,
                        trigger_quit=self.is_Quit_App
                ),
                self.cam_1_status_label.setText(self.cam_1_status_label.text() + " ENABLED"),
                self.cam_2_status_label.setText(self.cam_2_status_label.text() + " ENABLED"),
                
            ]
        )
        self.remove_camera_button.clicked.connect(
            self.camera_Remove
        )

    def closeEvent(self, *args, **kwargs):
        super(Ui_Camera_API_Developer, self).closeEvent(*args, **kwargs)

    def get_camera_available_port(self):
        source = 10
        arr = []
        while source >0:
            cap, frame= cv2.VideoCapture(source) 
            if cap is None or not cap.isOpened():
                print('Warning: unable to open video source: ', source)
            else: 
                arr.append(source)
            source -= 1
        
        temp_text = ""
        for i in arr:
            temp_text += "," + i
        return temp_text

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Ui_Camera_API_Main()
    sys.exit(app.exec_())