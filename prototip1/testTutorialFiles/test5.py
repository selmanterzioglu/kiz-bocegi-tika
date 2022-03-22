# import required libraries
import time
from vidgear.gears import VideoGear, WriteGear
import cv2
from distutils import extension
import libs
import logging
from structure_ui import Structure_UI, Graphics_View
from structure_camera import Camera_Object, CAMERA_FLAGS
from structure_system import System_Object
import qt_tools
from structure_ui_camera import Structure_Ui_Camera
from video_file_process import File_Process
# define suitable tweak parameters for writer

stream_1 = Camera_Object(
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
stream_1.api_CV2_Camera_Create_Instance(0, extra_params = [])

stream_2 = Camera_Object(
        camera_flag=CAMERA_FLAGS.CV2,
        logger_level=logging.INFO,
        auto_configure=False,
        trigger_quit=None,
        trigger_pause=None,
        lock_until_done=False,
        acquisition_framerate_enable=True,
        acquisition_framerate=30,
        # exposure_time=exposure_time,
        # max_buffer_limit=buffer_size,
        max_buffer_limit=10
        # logger_level=self.logger_level
)
stream_2.api_CV2_Camera_Create_Instance(1, extra_params = [])

stream_3 = Camera_Object(
        camera_flag=CAMERA_FLAGS.CV2,
        logger_level=logging.INFO,
        auto_configure=False,
        trigger_quit=None,
        trigger_pause=None,
        lock_until_done=False,
        acquisition_framerate_enable=True,
        acquisition_framerate=30,
        # exposure_time=exposure_time,
        # max_buffer_limit=buffer_size,
        max_buffer_limit=10
        # logger_level=self.logger_level
)
stream_3.api_CV2_Camera_Create_Instance(2, extra_params = [])



input_frame_rate = 25
stream_1.instance_Camera.set(cv2.CAP_PROP_FPS, input_frame_rate)
stream_2.instance_Camera.set(cv2.CAP_PROP_FPS, input_frame_rate)
stream_3.instance_Camera.set(cv2.CAP_PROP_FPS, input_frame_rate)

stream_1.stream_And_Save_Start_Thread_2( 
    trigger_pause=lambda: True, 
    trigger_quit=None, 
    number_of_snapshot=-1, 
    delay=0.001, 
    save_path="camera_1.avi",
    fps=input_frame_rate
)
stream_2.stream_And_Save_Start_Thread_2( 
    trigger_pause=lambda: True, 
    trigger_quit=None, 
    number_of_snapshot=-1, 
    delay=0.001, 
    save_path="camera_2.avi",
    fps=input_frame_rate
)
stream_3.stream_And_Save_Start_Thread_2( 
    trigger_pause=lambda: True, 
    trigger_quit=None, 
    number_of_snapshot=-1, 
    delay=0.001, 
    save_path="camera_3.avi",
    fps=input_frame_rate
)

width  =1920
height =1080
# stream_1.cv2_Set_Camera_Size((width,height))
# stream_2.cv2_Set_Camera_Size((width,height))

while True:

    frame_1 = stream_1.stream_Returner(auto_pop=False, pass_broken=True)
    frame_2 = stream_2.stream_Returner(auto_pop=False, pass_broken=True)
    frame_3 = stream_3.stream_Returner(auto_pop=False, pass_broken=True)
    
    time.sleep(0.01)

    if frame_1 is None or frame_2 is None or frame_3 is None :
        continue
    
    cv2.imshow("camera_1", frame_1)
    cv2.imshow("camera_2", frame_2)
    cv2.imshow("camera_3", frame_3)

    # check for 'q' key if pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        stream_1.quit()
        stream_2.quit()
        stream_3.quit()
        break

cv2.destroyAllWindows()
