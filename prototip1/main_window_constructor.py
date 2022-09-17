import glob
import libs
import logging
from specialFunciton import specialFunction
from structure_ui import Structure_UI, Graphics_View
from structure_camera import Camera_Object, CAMERA_FLAGS
from structure_system import System_Object
import cv2
import qt_tools
from tools import list_files

from video_file_process import File_Process
from structure_threading import Thread_Object
import sys
import serial_communication
from specialFunciton import specialFunction

class kiz_UI(Structure_UI):

    def __init__(self, *args, onj = None, logger_level = logging.INFO, **kwargs):
        self.init_QTimers = lambda: None
        super(kiz_UI, self).__init__(*args, **kwargs)

        self.cameras = dict()
        self.q_timers = dict()
        self.gui_widgets = dict()
        self.status_string = dict()
        self.__thread_Dict = dict()

        self.available_cameras = None
        self.max_camera_numbers = 4
        self.is_Camera_Stream_Active = False
        self.logger_level = logger_level
        self.connected_camera_list = list()
        self.available_cameras_counter = 0
        self.video_capture_mod = False
        self.video_directory = "video_data_folder/"
        self.is_Object_Initialized = True
        self.video_thread_quit = None
        self.specialFunction = specialFunction()
        
        self.simulation_mode = False
        
        self.init()
    
    def init(self):
        self.name = "KizUI"
        self.logger = logging.getLogger(self.name)
        
        self.system_o = System_Object()
        self.set_widgets()

        # self.system_o.thread_print_info()
        self.print_system_info_Thread(trigger_pause=None, trigger_quit=None, number_of_snapshot=-1, delay=0.001, trigger_before=None, trigger_after=None)
            
        if (self.simulation_mode == False):
            self.arduino_serial = serial_communication.Arduino_communication()
            if (self.arduino_serial.arduino == None):
                self.set_statusbar_string("Arduino is not found. ! ")
            else: 
                self.arduino_serial_recieve_data = None
                self.arduino_frontend_distance = 0
                self.arduino_backend_distance = 0
                self.arduino_route = 1
                self.arduino_motors_lock = 0
                self.arduino_motors_lock_last = 0

                self.read_arduino_Thread(trigger_pause=None, trigger_quit=None, number_of_snapshot=-1, delay=0.001, trigger_before=None, trigger_after=None)
                self.camera_video_capture()

    def read_arduino_Thread(self, trigger_pause=None, trigger_quit=None, number_of_snapshot=-1, delay=0.001, trigger_before=None, trigger_after=None):

        if self.get_Is_Object_Initialized():
            self.__thread_Dict["read_arduino_Thread"] = Thread_Object(
                name="Camera_Object.read_arduino_Thread",
                delay=0.0001,
                logger_level=self.logger.getEffectiveLevel(),
                run_number=None,
                quit_trigger=None
            )
            self.__thread_Dict["read_arduino_Thread"].init(
                params = [
                    trigger_pause,
                    trigger_quit,
                    number_of_snapshot,
                    delay,
                    trigger_before, 
                    trigger_after
                ],
                task=self.read_arduino
            )
            self.__thread_Dict["read_arduino_Thread"].start()

            return self.__thread_Dict["read_arduino_Thread"]
        else:
            return None

    def read_arduino(self, trigger_pause=None, trigger_quit=None, number_of_snapshot=-1, delay=0.001, trigger_before=None, trigger_after=None):

        if (self.arduino_serial.arduino is not None):
            self.arduino_serial_recieve_data = self.arduino_serial.read_data_from_arduino()

            if (self.arduino_serial_recieve_data.find("frontend_distance: ") != -1):
                self.arduino_frontend_distance = int(self.arduino_serial_recieve_data.strip("frontend_distance: "))
                self.gui_widgets["label_frontend_distance"].setText("Frontend Distance: {} cm".format(self.arduino_frontend_distance))

            elif (self.arduino_serial_recieve_data.find("backend_distance: ") != -1):
                self.arduino_backend_distance = int(self.arduino_serial_recieve_data.strip("backend_distance: "))
                self.gui_widgets["label_backend_distance"].setText("Backend Distance: {} cm".format(self.arduino_backend_distance))
            
            elif (self.arduino_serial_recieve_data.find("lock: ") != -1):
                self.arduino_motors_lock = int(self.arduino_serial_recieve_data.strip("lock: "))
                if (self.arduino_motors_lock == 1):
                    self.gui_widgets["label_motors_lock"].setText("Motors Lock: Locked")
                if (self.arduino_motors_lock == 0):
                    self.gui_widgets["label_motors_lock"].setText("Motors Lock: Unlock")
            
            elif (self.arduino_serial_recieve_data.find("route: ") != -1):
                self.arduino_route = int(self.arduino_serial_recieve_data.strip("route: "))
                
                self.gui_widgets["label_route"].setText("Route: Forward")
                if (self.arduino_route == 0):
                    self.gui_widgets["label_route"].setText("Route: Backward")

            if (self.arduino_motors_lock == 1 and self.arduino_motors_lock_last == 0):
                self.camera_video_capture()
                self.arduino_serial.send_data_to_arduino("motors_unlock")
                self.arduino_motors_lock_last = 1
                
            elif (self.arduino_motors_lock == 0 and self.arduino_motors_lock_last == 1):
                self.camera_video_capture()
                self.arduino_motors_lock_last = 0
        else:
            self.arduino_frontend_distance = -1
            self.arduino_backend_distance = -1
            self.gui_widgets["label_frontend_distance"].setText("Frontend Sensor is not found")
            self.gui_widgets["label_backend_distance"].setText("Backend Sensor is not found")
            self.set_statusbar_string("Sensor error! Sensors are not available.!")
              
    def print_system_info_Thread(self, trigger_pause=None, trigger_quit=None, number_of_snapshot=-1, delay=0.001, trigger_before=None, trigger_after=None):

        if self.get_Is_Object_Initialized():
            self.__thread_Dict["print_system_info_Thread"] = Thread_Object(
                name="Camera_Object.print_system_info_Thread",
                delay=0.001,
                logger_level=self.logger.getEffectiveLevel(),
                run_number=None,
                quit_trigger=None
            )
            self.__thread_Dict["print_system_info_Thread"].init(
                params=[
                    trigger_pause,
                    trigger_quit,
                    number_of_snapshot,
                    delay,
                    trigger_before, 
                    trigger_after
                ],
                task=self.init_gui_thread
            )
            self.__thread_Dict["print_system_info_Thread"].start()

            return self.__thread_Dict["print_system_info_Thread"]
        else:
            return None

    def set_widgets(self):
        self.gui_widgets["cam_1_status_label"] = self.cam_1_status_label
        self.gui_widgets["cam_2_status_label"] = self.cam_2_status_label
        self.gui_widgets["cam_3_status_label"] = self.cam_3_status_label
        self.gui_widgets["cam_4_status_label"] = self.cam_4_status_label

        self.gui_widgets["button_camera_video_capture"] = self.button_camera_video_capture
        self.gui_widgets["button_camera_connect"] = self.button_camera_connect
        self.gui_widgets["button_camera_remove"] = self.button_camera_remove

        self.gui_widgets["label_used_cpu"] = self.label_used_cpu
        self.gui_widgets["label_used_memory"] = self.label_used_memory
        self.gui_widgets["label_frontend_distance"] = self.label_frontend_distance
        self.gui_widgets["label_backend_distance"] = self.label_backend_distance
        self.gui_widgets["label_motors_lock"] = self.label_motors_lock
        self.gui_widgets["label_route"] = self.label_route

    def init_gui_thread(self, trigger_pause=None, trigger_quit=None, number_of_snapshot=-1, delay=0.001, trigger_before=None, trigger_after=None):
        cpu_percent = "Used CPU: {}".format(self.system_o.cpu_percent_Psutil())        
        memory_usage = "Used Memory: {:.2f} MB".format(self.system_o.memory_Usage_Psutil())        

        self.gui_widgets["label_used_cpu"].setText(cpu_percent)
        self.gui_widgets["label_used_memory"].setText(memory_usage)

    def camera_video_capture_button_clicked(self):

        if self.is_video_capture_mod():
            self.stop_video_record()
        else:
            self.available_cameras = self.get_camera_available_port()
            self.available_cameras_counter = len(self.available_cameras)
            self.start_video_record()

    def camera_video_capture(self):
        if self.is_video_capture_mod():
            self.stop_video_record()
        else:
            self.available_cameras = self.get_camera_available_port()
            self.available_cameras_counter = len(self.available_cameras)
            self.start_video_record()

    def camera_connect_button_clicked(self):
        self.available_cameras = self.get_camera_available_port()
        self.available_cameras_counter = len(self.available_cameras)

        self.camera_qtimer_creater_runner()

        self.autonomous_Camera_Instance()
        self.camera_set_resolution(width=1920, height=1080)
        self.autonomous_Camera_Thread_Starter()
        self.stream_Switch(True)
        self.set_camera_status(status="connected")
    
    def camera_remove_button_clicked(self):
        # self.camera_Remove(), # this button is beta version. it is not working
        self.set_statusbar_string("This button is not working.!")

    def stop_video_record(self):
        self.set_video_thread_quit(True)
        qt_tools.qtimer_All_Stop(self.q_timers)

        for i in range(1,self.available_cameras_counter + 1):
            cam_string = "camera_{}".format(i)
            self.cameras[cam_string].quit()

        self.remove_camera_variables()
        
        self.gui_widgets["button_camera_video_capture"].setText("Start Video Record")
        self.garbage_Collector_Cleaner()
        self.set_video_capture_mod(False)
       
    def remove_camera_variables(self):
        
        cameras_keys = list(self.cameras.keys())
        for i in cameras_keys:
            del self.cameras[i]
        del cameras_keys
        
        q_timers_keys = list(self.q_timers.keys())
        for i in q_timers_keys:
            del self.q_timers[i]
        
        Buffer_Dict_keys  = list(self.Buffer_Dict.keys())
        for i in Buffer_Dict_keys:
            del self.Buffer_Dict[i]
        
        
        self.available_cameras = None
        self.available_cameras_counter = 0

    def start_video_record(self):

        self.camera_qtimer_creater_runner()
        self.autonomous_Camera_Instance()
        self.camera_set_resolution(width=1920, height=1080)
        self.set_video_thread_quit(None)
        self.video_record_Thread_Starter()
        self.stream_Switch(True)
        self.set_video_capture_mod(True)
        self.set_camera_status(status="connected") 
        self.gui_widgets["button_camera_video_capture"].setText("Stop Video Record")
        
    def configure_Button_Connections(self):
        self.button_camera_video_capture.clicked.connect(
            self.camera_video_capture_button_clicked
        )
        self.button_camera_connect.clicked.connect(       
            self.camera_connect_button_clicked
        )
        self.button_camera_remove.clicked.connect(
            self.camera_remove_button_clicked
        )
   
    def set_video_capture_mod(self, bool):
        self.video_capture_mod = bool

    def is_video_capture_mod(self):
        return self.video_capture_mod

    def camera_qtimer_creater_runner(self):
        if self.available_cameras_counter == 0:
            print("your camera/s is not available")
        else:    
            if self.available_cameras_counter >= 1:
                self.q_timers["camera_1_renderer"] = qt_tools.qtimer_Create_And_Run(
                    self,
                    connection=self.camera_1_renderer,
                    delay=2,
                    is_needed_start=True,
                    is_single_shot=False
                )   
            if self.available_cameras_counter >= 2:
                self.q_timers["camera_2_renderer"] = qt_tools.qtimer_Create_And_Run(
                    self,
                    connection=self.camera_2_renderer,
                    delay=2,
                    is_needed_start=True,
                    is_single_shot=False
                )
            if self.available_cameras_counter >= 3:
                self.q_timers["camera_3_renderer"] = qt_tools.qtimer_Create_And_Run(
                    self,
                    connection=self.camera_3_renderer,
                    delay=2,
                    is_needed_start=True,
                    is_single_shot=False
                )
            if self.available_cameras_counter >= 4:
                self.q_timers["camera_4_renderer"] = qt_tools.qtimer_Create_And_Run(
                    self,
                    connection=self.camera_4_renderer,
                    delay=2,
                    is_needed_start=True,
                    is_single_shot=False
                )
       
    def camera_Initializes(self, camera_number):
        camera_string = "camera_" + str(camera_number)
        if not self.cameras.get(camera_string):
            self.cameras[camera_string] = Camera_Object(
                camera_flag=CAMERA_FLAGS.CV2,
                logger_level=logging.INFO,
                auto_configure=True,
                extra_params=[],
                # auto_configure=False,
                trigger_quit=None,
                trigger_pause=None,
                lock_until_done=False,
                acquisition_framerate=30,
                max_buffer_limit=10
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
        counter=0
        for i in range(1,self.available_cameras_counter+1):
            cam_string = "camera_{}".format(i)
            self.qt_Priority()
            self.camera_Initializes(camera_number=i)
            # if (self.specialFunction.get_os_platform == "win32"):
            #     self.cameras[cam_string].api_CV2_Camera_Create_Instance(self.available_cameras[counter], extra_params = [cv2.CAP_V4L2])
            if (self.specialFunction.get_os_platform() == "linux" or self.specialFunction.get_os_platform() == "linux2"):
                self.cameras[cam_string].api_CV2_Camera_Create_Instance(self.available_cameras[counter], extra_params = [cv2.CAP_V4L2])
            else:
                self.cameras[cam_string].api_CV2_Camera_Create_Instance(self.available_cameras[counter], extra_params = [cv2.CAP_MSMF])

            counter +=1

    def set_camera_status(self, status):

        if status == "default":
            for i in range(1,5):
                self.qt_Priority()
                label_string = "cam_{}_status_label".format(i)
                message = "Cam {} Status:".format(i)
                self.gui_widgets[label_string].setText(message)
        
        elif status== "connected":
            for i in range(1,self.available_cameras_counter + 1):
                self.qt_Priority()
                label_string = "cam_{}_status_label".format(i)
                message = "Cam {} Status: ENABLED".format(i)
                self.gui_widgets[label_string].setText(message)

    def video_record_Thread_Starter(self):
        
        file_process = File_Process(video_data_directory_name="video_data_folder")
        path = file_process.get_data_folder_path()
        generated_video_name = file_process.get_video_name()
        
        fps = 30
        if self.available_cameras_counter == 1:
            fps = 29
        elif self.available_cameras_counter == 2:
            fps = 22
        elif self.available_cameras_counter == 3:
            fps = 15
        elif self.available_cameras_counter == 4:
            fps = 22

        for i in range(1,self.available_cameras_counter + 1):
            self.qt_Priority()
            cam_string = "camera_{}".format(i)
            video_path = "{}{}".format(path, self.cameras[cam_string].name)
            video_name = "{}{}{}.avi".format(path, generated_video_name, cam_string)
            
            self.cameras[cam_string].stream_And_Save_Start_Thread(
                trigger_pause=self.is_Stream_Active,
                trigger_quit=self.is_video_thread_quit, 
                number_of_snapshot=-1, 
                delay=0.0001, 
                trigger_before=None,
                trigger_after=None,
                save_path=video_name, 
                fps=fps
            )
    
    def is_video_thread_quit(self):
        return self.video_thread_quit

    def set_video_thread_quit(self, video_thread_quit):
        self.video_thread_quit = video_thread_quit

    def autonomous_Camera_Thread_Starter(self):
        """This function start camera thread functions"""
        for i in range(1,self.available_cameras_counter + 1):
            self.qt_Priority()
            cam_string = "camera_{}".format(i)

            self.cameras[cam_string].stream_Start_Thread(
                trigger_pause=self.is_Stream_Active,
                trigger_quit= None,
                number_of_snapshot=-1,
                delay=0.001,
                trigger_before=None, 
                trigger_after=None,
            )
            
    def set_statusbar_string(self, message):
        self.statusBar().showMessage(message)
    
    def camera_set_resolution(self, width, height):
        for i in range(1,self.available_cameras_counter+1):
            self.qt_Priority()
            cam_string = "camera_{}".format(i)
            self.cameras[cam_string].cv2_Set_Camera_Size((width,height))
   
    def closeEvent(self, *args, **kwargs):
        super(kiz_UI, self).closeEvent(*args, **kwargs)

    
    def get_camera_available_port(self):
        """ This function search available camera port on pc """

        source = 10
        available_port = []
        camera = None

        while source >=0:
            try:
                if (self.specialFunction.get_os_platform() == "win32"):
                    camera = cv2.VideoCapture(source, cv2.CAP_MSMF)
                else:
                    camera = cv2.VideoCapture(source)

                is_reading, img = camera.read()
                if camera.isOpened() and is_reading is True:
                    available_port.append(source)  
                
                camera.release()
                cv2.destroyAllWindows()
            except TypeError:
                pass
            source -= 1
        print(available_port)
        return available_port

    def is_Stream_Active(self):
        return self.is_Camera_Stream_Active

    def stream_Switch(self, bool=None):
        self.is_Camera_Stream_Active = \
            not self.is_Camera_Stream_Active \
            if bool is None else bool
        return self.is_Camera_Stream_Active

    def get_Is_Object_Initialized(self):
        return self.is_Object_Initialized
   
