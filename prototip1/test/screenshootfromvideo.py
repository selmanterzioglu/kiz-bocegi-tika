import cv2
import time

# Opens the Video file
fileName = "test.mp4"
cap= cv2.VideoCapture(fileName)
i=0
while(cap.isOpened()):
    ret, frame = cap.read()    
    if ret == False:
        break
    cv2.imwrite(fileName +str(i)+'.jpg',frame)
    i+=1

cap.release()
cv2.destroyAllWindows()