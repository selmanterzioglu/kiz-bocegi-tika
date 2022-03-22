# import required libraries
from vidgear.gears import VideoGear
from vidgear.gears import WriteGear
import cv2

# define suitable tweak parameters for writer


# open live video stream on webcam at first index(i.e. 0) device
# stream_1 = VideoGear(source=0, logging=True).start()
# stream_2 = VideoGear(source=2, logging=True).start()


stream_1 = cv2.VideoCapture(0)
stream_2 = cv2.VideoCapture(2)

output_params = {
    "-fps": 30,
    "-fourcc": "MJPG",
    "-output_dimensions": (1920,1080)
}

# Define writer with defined parameters and suitable output filename for e.g. `Output.mp4`
writer_1 = WriteGear(
    output_filename="video_data_folder\\camera_1.mp4", compression_mode=False, logging=True, **output_params
)
writer_2 = WriteGear(
    output_filename="video_data_folder\\camera_2.mp4", compression_mode=False, logging=True, **output_params
)



while True:

    # read frames from stream
    (grabbed_1, frame_1) = stream_1.read()
    (grabbed_2, frame_2) = stream_2.read()

    # check for frame if not grabbed
    if not grabbed_1 and not grabbed_2 :
        break

    writer_1.write(frame_1)
    writer_2.write(frame_2)

    # Show output window
    cv2.imshow("camera_1", frame_1)
    cv2.imshow("camera_2", frame_2)

    # check for 'q' key if pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cv2.destroyAllWindows()

stream_1.release()
stream_2.release()

writer_1.close()
writer_2.close()
