from distutils import extension
import libs
import logging
from structure_ui import Structure_UI, Graphics_View
from structure_camera import Camera_Object, CAMERA_FLAGS
from structure_system import System_Object
import cv2
import qt_tools
from structure_ui_camera import Structure_Ui_Camera
from video_file_process import File_Process

class kiz_UI(Structure_Ui_Camera):
    def __init__(self, *args, onj = None, logger_level = logging.INFO, **kwargs):
        self.init_QTimers = lambda: None
        
        super(kiz_UI, self).__init__(*args, **kwargs)

        self.cameras = dict()
        self.q_timers = dict()
        self.available_cameras = None
        self.max_camera_numbers = 4
        self.is_Camera_Stream_Active = False
        self.logger_level = logger_level
        self.connected_camera_list = list()
        
        self.video_capture_mod = False
        self.video_directory = "video_data_folder/"

        self.system_o = System_Object()
        self.system_o.thread_print_info()
        
    def camera_qtimer_creater_runer(self):
        self.available_cameras = self.get_camera_available_port()
        available_cameras_counter = len(self.available_cameras)
        if available_cameras_counter == 0:
            print("your camera/s is not available")
        else:    
            if available_cameras_counter >= 1:
                self.q_timers["camera_1_renderer"] = qt_tools.qtimer_Create_And_Run(
                    self,
                    connection=self.camera_1_renderer,
                    delay=10,
                    is_needed_start=True,
                    is_single_shot=False
                )   
            if available_cameras_counter >= 2:
                self.q_timers["camera_2_renderer"] = qt_tools.qtimer_Create_And_Run(
                    self,
                    connection=self.camera_2_renderer,
                    delay=10,
                    is_needed_start=True,
                    is_single_shot=False
                )
            if available_cameras_counter >= 3:
                self.q_timers["camera_3_renderer"] = qt_tools.qtimer_Create_And_Run(
                    self,
                    connection=self.camera_3_renderer,
                    delay=10,
                    is_needed_start=True,
                    is_single_shot=False
                )
            if available_cameras_counter >= 4:
                self.q_timers["camera_4_renderer"] = qt_tools.qtimer_Create_And_Run(
                    self,
                    connection=self.camera_4_renderer,
                    delay=10,
                    is_needed_start=True,
                    is_single_shot=False
                )
       
    def camera_Initializes(self, camera_number):
        camera_string = "camera_" + str(camera_number)
        if not self.cameras.get(camera_string):
            self.cameras[camera_string] = Camera_Object(
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
    
    def camera_3_renderer(self):
        if self.cameras.get("camera_3"):
            self.frame_3.set_Background_Image(self.cameras["camera_3"].stream_Returner(auto_pop=True, pass_broken=True))
    
    def camera_4_renderer(self):
        if self.cameras.get("camera_4"):
            self.frame_4.set_Background_Image(self.cameras["camera_4"].stream_Returner(auto_pop=True, pass_broken=True))
    
    def camera_Remove(self):
        # if self.is_Camera_Instance_Exist():
        self.stream_Switch(False)

        for camera in self.cameras.values():
            camera.quit()

        for key in self.cameras.keys():
            self.cameras.pop(key)
    
    def autonomous_Camera_Instance(self):
        available_cameras_counter = len(self.available_cameras)
        counter=0
        for i in range(1,available_cameras_counter+1):
            cam_string = "camera_{}".format(i)
            self.camera_Initializes(camera_number=i)
            self.cameras[cam_string].api_CV2_Camera_Create_Instance(self.available_cameras[counter], extra_params = []),
            counter +=1

    def camera_status_clear(self, counter):
        if counter >= 1:
            self.cam_1_status_label.setText("")
        if counter >= 2:
            self.cam_2_status_label.setText("")
        if counter >= 3:
            self.cam_3_status_label.setText("")
        if counter >= 4:
            self.cam_4_status_label.setText("")

    def camera_status_remove(self):
        available_cameras_counter = len(self.available_cameras)
        self.camera_status_clear(available_cameras_counter)

        if available_cameras_counter >= 1:
            self.cam_1_status_label.setText("Cam 1 Status:" + " camera is removed")
        if available_cameras_counter >= 2:
            self.cam_2_status_label.setText("Cam 2 Status:" + " camera is removed")
        if available_cameras_counter >= 3:
            self.cam_3_status_label.setText("Cam 3 Status:" + " camera is removed")
        if available_cameras_counter >= 4:
            self.cam_4_status_label.setText("Cam 4 Status:" + " camera is removed")

    def camera_status_default(self):
        self.camera_status_clear(self.max_camera_numbers)
        self.cam_1_status_label.setText("Cam 1 Status:")
        self.cam_2_status_label.setText("Cam 2 Status:")
        self.cam_3_status_label.setText("Cam 3 Status:")
        self.cam_4_status_label.setText("Cam 4 Status:")

    def camera_status_connected(self):
        available_cameras_counter = len(self.available_cameras)
        self.camera_status_clear(available_cameras_counter)

        if available_cameras_counter >= 1:
            self.cam_1_status_label.setText("Cam 1 Status:" + " ENABLED")
        if available_cameras_counter >= 2:
            self.cam_2_status_label.setText("Cam 2 Status:" + " ENABLED")
        if available_cameras_counter >= 3:
            self.cam_3_status_label.setText("Cam 3 Status:" + " ENABLED")
        if available_cameras_counter >= 4:
            self.cam_4_status_label.setText("Cam 4 Status:" + " ENABLED")

    def autonomous_Camera_Thread_Starter(self):
        """This function start camera thread functions"""

        available_cameras_counter = len(self.available_cameras)
        for i in range(1,available_cameras_counter+1):
            cam_string = "camera_{}".format(i)
            self.cameras[cam_string].stream_Start_Thread(
                    number_of_snapshot=-1,
                    delay=0.001,
                    trigger_pause=self.is_Stream_Active,
                    trigger_quit=self.is_Quit_App
            )
            
    def set_statusbar_string(self, message):
        self.statusBar().showMessage(message)
    
    def camera_set_resolution(self, width, height):
        self.available_cameras = self.get_camera_available_port()
        available_cameras_counter = len(self.available_cameras)
        
        for i in range(1,available_cameras_counter+1):
                cam_string = "camera_{}".format(i)
                self.cameras[cam_string].cv2_Set_Camera_Size((width,height))

                print(self.cameras[cam_string].get_Camera_Size()[0],
                      self.cameras[cam_string].get_Camera_Size()[1]
                      )

    def video_capture(self):
        self.connect_camera_button_clicked()
        available_cameras_counter = len(self.available_cameras)
        
        file_process = File_Process(video_data_directory_name="video_data_folder")
        file_process.set_video_extension("avi")
        path = file_process.get_data_folder_path()
        extension = file_process.get_video_extension()

        if self.video_capture_mod == False:
            for i in range(1,available_cameras_counter+1):
                cam_string = "camera_{}".format(i)
                video_name = file_process.get_video_name() + cam_string
                # self.cameras[cam_string].buffer_Clear()

                self.cameras[cam_string].save_Video_From_Buffer_Thread(
                    path=path, 
                    name=video_name, 
                    extension=extension, 
                    fps=30,
                    trigger_pause=self.is_Stream_Active, 
                    trigger_quit=self.is_Quit_App, 
                    number_of_snapshot=-1, 
                    delay=0.0001
                )

            self.camera_video_capture_button.setText("Stop Video Record")
            self.video_capture_mod = True
        else:
            for i in range(1,available_cameras_counter+1):
                cam_string = "camera_{}".format(i)
                self.cameras[cam_string].camera_Releaser()

                self.video_capture_mod = False
                self.camera_video_capture_button.setText("Start Video Record")
    
    def connect_camera_button_clicked(self):
        self.camera_qtimer_creater_runer()
        self.camera_status_clear(self.max_camera_numbers)
        self.autonomous_Camera_Instance()
        # self.camera_set_resolution(width=1920, height=1080)
        self.autonomous_Camera_Thread_Starter()
        self.stream_Switch(True)
        self.camera_status_connected()
    
    def remove_camera_button_clicked(self):
        # self.camera_Remove(), # this button is beta version. it is not working
        self.camera_status_remove()
        self.set_statusbar_string("This button is not working.!")

    def configure_Button_Connections(self):
        self.connect_camera_button.clicked.connect(       
            self.connect_camera_button_clicked
        )
        self.remove_camera_button.clicked.connect(
            self.remove_camera_button_clicked
        )
        self.camera_video_capture_button.clicked.connect(
            self.video_capture
            # buraya video kaydetme fonksiyonu eklenecek
        )
   
    def closeEvent(self, *args, **kwargs):
        super(kiz_UI, self).closeEvent(*args, **kwargs)

    @staticmethod
    def get_camera_available_port():
        """ This function search available camera port on pc """

        source = 10
        available_port = []
        
        while source >=0:
            try:
                camera = cv2.VideoCapture(source, cv2.CAP_DSHOW)
                is_reading, img = camera.read()
                if camera.isOpened() and is_reading is True:
                    available_port.append(source)  
                
                camera.release()
                cv2.destroyAllWindows()
            except TypeError:
                pass
            source -= 1
        return available_port

    def is_Stream_Active(self):
        return self.is_Camera_Stream_Active

    def stream_Switch(self, bool=None):
        self.is_Camera_Stream_Active = \
            not self.is_Camera_Stream_Active \
            if bool is None else bool
        return self.is_Camera_Stream_Active
