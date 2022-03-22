from multiprocessing import Process, current_process
import time
import cv2

import numpy as np
import cv2 as cv


def video_record(camera_name, cam_src):
    name = current_process().name
    print("name", name)
    cap = cv.VideoCapture(cam_src)
    # Define the codec and create VideoWriter object
    fourcc = cv.VideoWriter_fourcc(*'mp4v')


    out = cv.VideoWriter(camera_name + ".mp4", fourcc, 20.0, (640,  480))

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        # write the flipped frame
        out.write(frame)
        cv.imshow('frame', frame)
        if cv.waitKey(1) == ord('q'):
            break
    # Release everything if job is finished
    cap.release()
    out.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    camera_1 = Process(name="camera_1",target=video_record, args=("camera_1",0,))
    camera_2 = Process(name="camera_2",target=video_record, args=("camera_2",2,))

    camera_1.start()
    camera_2.start()
    time.sleep(5)
    camera_1.join()
    camera_2.join()
    

