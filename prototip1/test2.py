from pickle import FALSE
from sys import implementation
import libs
import cv2
from structure_camera import Camera_Object, CAMERA_FLAGS
from time import sleep
import logging 

# cam = cv2.VideoCapture(0)


def trigger_p():

    return True


camera_Instance =  Camera_Object(
            camera_flag=CAMERA_FLAGS.CV2,
            auto_configure=False,
            trigger_quit=None,
            trigger_pause=None,
            lock_until_done=False,
            acquisition_framerate=30,
            # exposure_time=exposure_time,
            # max_buffer_limit=buffer_size,
            max_buffer_limit=20,
            logger_level=logging.DEBUG
        )

camera_Instance.api_CV2_Camera_Create_Instance(0, extra_params = [])
print(camera_Instance.get_Is_Camera_Initialized())
cv2.namedWindow("test")

temp = camera_Instance.stream_Start_Thread(
        trigger_p,
        number_of_snapshot=1000,
        delay=0.001
)


while True:

    sleep(0.001)
    frame = camera_Instance.stream_Returner(auto_pop=True, pass_broken=True)
    # print(frame)
    
    cv2.imshow("test", frame) if frame is not None else None 

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break

camera_Instance.camera_Releaser()
cv2.destroyAllWindows()
