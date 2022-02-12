from pickle import FALSE
import libs
import cv2
from structure_camera import Camera_Object, CAMERA_FLAGS


# cam = cv2.VideoCapture(0)

cam =  Camera_Object(
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

cam.api_CV2_Camera_Create_Instance(2, extra_params = [])

cv2.namedWindow("test")

img_counter = 0

while True:
    # ret, frame = cam.read()
    ret, frame = cam.snapshot()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("test", frame)
    print(frame.shape)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1



cv2.destroyAllWindows()


