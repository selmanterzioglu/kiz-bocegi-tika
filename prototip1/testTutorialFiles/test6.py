# import required libraries
from vidgear.gears import VideoGear, CamGear, WriteGear
import cv2

# open live video stream on webcam at first index(i.e. 0) device
stream_1 = CamGear(source=0).start()
stream_2 = CamGear(source=2).start()

output_params = {"-input_framerate": stream_1.framerate}

writer_1 = WriteGear(output_filename="video_data_folder\\camera_1.mp4", **output_params)
writer_2 = WriteGear(output_filename="video_data_folder\\camera_2.mp4", **output_params)

while True:

    frame_1 = stream_1.read()
    frame_2 = stream_2.read()

    if frame_1 is None or frame_2 is None:
        break

    writer_1.write(frame_1)
    writer_2.write(frame_2)

    cv2.imshow("camera_1", frame_1)
    cv2.imshow("camera_2", frame_2)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cv2.destroyAllWindows()

stream_1.stop()
stream_2.stop()

writer_1.close()
writer_2.close()


