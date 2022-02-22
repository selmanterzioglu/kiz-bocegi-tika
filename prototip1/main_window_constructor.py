import libs

import logging
from structure_ui import Structure_UI, Graphics_View
from structure_camera import Camera_Object, CAMERA_FLAGS
from structure_system import System_Object
import cv2
import qt_tools


class kiz_UI(Structure_UI):
    def __init__(self, *args, onj = None, logger_level = logging.INFO, **kwargs):
        super(kiz_UI, self).__init__(*args, **kwargs)

        self.cameras = dict()
        self.q_timers = dict()
        self.system_o = System_Object()

        self.logger_level = logger_level
        self.system_o.thread_print_info()
        
        self.is_Camera_Stream_Active = False
        self.q_timers["camera_1_renderer"] = qt_tools.qtimer_Create_And_Run(
            self,
            connection=self.camera_1_renderer,
            delay=10,
            is_needed_start=True,
            is_single_shot=False
        )

        self.q_timers["camera_2_renderer"] = qt_tools.qtimer_Create_And_Run(
            self,
            connection=self.camera_2_renderer,
            delay=10,
            is_needed_start=True,
            is_single_shot=False
        )

    def camera_Initializes(self):
        if not self.cameras.get("camera_1"):
            self.cameras["camera_1"] = Camera_Object(
                camera_flag=CAMERA_FLAGS.CV2,
                logger_level=logging.INFO,
                auto_configure=False,
                trigger_quit=None,
                trigger_pause=None,
                lock_until_done=False,
                acquisition_framerate=30,
                # exposure_time=exposure_time,
                # max_buffer_limit=buffer_size,
                max_buffer_limit=10
                # logger_level=self.logger_level
            ) 
        if not self.cameras.get("camera_2"):
            self.cameras["camera_2"] = Camera_Object(
                camera_flag=CAMERA_FLAGS.CV2,
                logger_level=logging.INFO,
                auto_configure=False,
                trigger_quit=None,
                trigger_pause=None,
                lock_until_done=False,
                acquisition_framerate=30,
                # exposure_time=exposure_time,
                # max_buffer_limit=buffer_size,
                max_buffer_limit=10
                # logger_level=self.logger_level
            )

    def camera_1_renderer(self):
        if self.cameras.get("camera_1"):
            self.frame_1.set_Background_Image(self.cameras["camera_1"].stream_Returner(auto_pop=True, pass_broken=True))
    
    def camera_2_renderer(self):
        if self.cameras.get("camera_2"):
            self.frame_2.set_Background_Image(self.cameras["camera_2"].stream_Returner(auto_pop=True, pass_broken=True))
    
    def camera_Remove(self):
        if self.is_Camera_Instance_Exist():
            self.stream_Switch(False)

            self.cameras["camera_1"].quit()
            self.cameras["camera_2"].quit()
            
            self.cameras.pop("camera_1")
            self.cameras.pop("camera_2")
    
    def configure_Button_Connections(self):
        self.connect_camera_button.clicked.connect(            
            lambda: [
                self.camera_Initializes(),

                self.cameras["camera_1"].api_CV2_Camera_Create_Instance(1, extra_params = []),
                self.cameras["camera_2"].api_CV2_Camera_Create_Instance(2, extra_params = []),
                
                self.cameras["camera_1"].stream_Start_Thread(
                    number_of_snapshot=-1,
                    delay = 0.001,
                    trigger_pause=self.is_Stream_Active,
                    trigger_quit=self.is_Quit_App
                ),
                self.cameras["camera_2"].stream_Start_Thread(
                        number_of_snapshot=-1,
                        delay=0.001,
                        trigger_pause=self.is_Stream_Active,
                        trigger_quit=self.is_Quit_App
                ),
                
                self.cam_1_status_label.setText(self.cam_1_status_label.text() + " ENABLED"),
                self.cam_2_status_label.setText(self.cam_2_status_label.text() + " ENABLED"),
                self.stream_Switch(True)
            ]
        )
        self.remove_camera_button.clicked.connect(
            lambda:[
                self.camera_Remove,
                self.cam_1_status_label.setText("Cam 1 Status:"),
                self.cam_2_status_label.setText("Cam 2 Status:")
            ]
        )

    def closeEvent(self, *args, **kwargs):
        super(kiz_UI, self).closeEvent(*args, **kwargs)

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

    def is_Stream_Active(self):
        return self.is_Camera_Stream_Active

    def stream_Switch(self, bool=None):
        self.is_Camera_Stream_Active = \
            not self.is_Camera_Stream_Active \
            if bool is None else bool
        return self.is_Camera_Stream_Active
