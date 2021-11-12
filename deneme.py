import time
import cv2

video = cv2.VideoCapture(0)
frame_width = int(video.get(3))
frame_height = int(video.get(4))
size = (frame_width, frame_height)

result = cv2.VideoWriter('filename.mp4', 
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         10, size)
start = time.time()
video_duration = 4

while(int(time.time() - start) < video_duration):

    now = int (time.time() - start)
    ret, frame = video.read()

    if ret == True:     
        result.write(frame)

video.release()
result.release()
cv2.destroyAllWindows()
