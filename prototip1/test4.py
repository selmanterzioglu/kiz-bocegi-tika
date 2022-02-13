import cv2


arr = []
cap = cv2.VideoCapture(4)

for width in range(1, 2000):
    for height in range(1, 2000):

        cap.set(3,width)
        cap.set(4,height)
        w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        
        if w == width and h ==height:
            temp = w + "x" + h
            arr.append(temp)



        