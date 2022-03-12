# import required libraries
import time
from vidgear.gears import VideoGear
from vidgear.gears import WriteGear
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


# open live video stream on webcam at first index(i.e. 0) device
# stream_1 = VideoGear(source=0, logging=True).start()
# stream_2 = VideoGear(source=2, logging=True).start()



camera_string = "camera_1"
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

camera_string = "camera_2"
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

time.sleep(1)
input_frame_rate = 25
stream_1.instance_Camera.set(cv2.CAP_PROP_FPS, input_frame_rate)
stream_2.instance_Camera.set(cv2.CAP_PROP_FPS, input_frame_rate)
# cap. set(cv2. cv. CV_CAP_PROP_FPS, 60)


stream_2.api_CV2_Camera_Create_Instance(2, extra_params = [])

stream_1.stream_Start_Thread( 
            trigger_pause=lambda: True, 
            trigger_quit=None, 
            number_of_snapshot=-1, 
            delay=0.001, 
        )
stream_2.stream_Start_Thread( 
            trigger_pause=lambda: True, 
            trigger_quit=None, 
            number_of_snapshot=-1, 
            delay=0.001, 
        )

width  =1920
height =1080
# stream_1.cv2_Set_Camera_Size((width,height))
# stream_2.cv2_Set_Camera_Size((width,height))


output_params = {
    "-fps": 50,
    "-fourcc": "MJPG",
    # "-output_dimensions": (1920,1080),
    # "-input_framerate": 30.0
}

# Define writer with defined parameters and suitable output filename for e.g. `Output.mp4`
writer_1 = WriteGear(
    output_filename="video_data_folder\\camera_1.mp4", compression_mode=False, logging=True, **output_params
)
writer_2 = WriteGear(
    output_filename="video_data_folder\\camera_2.mp4", compression_mode=False, logging=True, **output_params
)

time.sleep(1)

while True:

    # read frames from stream
    frame_1 = stream_1.stream_Returner(auto_pop=False, pass_broken=True)
    frame_2 = stream_2.stream_Returner(auto_pop=False, pass_broken=True)

    if frame_1 is None or frame_2 is None :
        continue

    # print("DEBUG: ", frame_1)
    # print("DEBUG: ", frame_2)
    
    # print("DEBUG: ", frame_1.shape)
    # print("DEBUG: ", frame_2.shape)

    writer_1.write(frame_1)
    writer_2.write(frame_2)

    cv2.imshow("camera_1", frame_1)
    cv2.imshow("camera_2", frame_2)

    # check for 'q' key if pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cv2.destroyAllWindows()

# stream_1.release()
# stream_2.release()

writer_1.close()
writer_2.close()
