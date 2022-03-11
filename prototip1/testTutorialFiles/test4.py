import cv2
import device
  
# define a video capture object
vid = cv2.VideoCapture(0)
vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while(True):
      
    # Capture the video frame
    # by frame
    ret, frame = vid.read()
  
    # Display the resulting frame
    cv2.imshow('frame', frame)


    # vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    # vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    # print(cv2.CAP_PROP_XI_DEVICE_MODEL_ID)

    # print(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    # print(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
      
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



