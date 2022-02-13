from cgi import print_directory
import cv2 

# def returnCameraIndexes():
#     # checks the first 10 indexes.
#     index = 0
#     arr = []
#     i = 10
#     while i > 0:
#         cap = cv2.VideoCapture(index)
#         if cap.read()[0]:
#             arr.append(index)
#             cap.release()
#         index += 1
#         i -= 1
#     return arr

# def list_ports():


#     is_working = True
#     dev_port = 10
#     working_ports = []
#     available_ports = []
#     while dev_port >= 0:
#         camera = cv2.VideoCapture(dev_port)
#         if camera.isOpened():
#             is_reading, img = camera.read()
#             if is_reading:
#                 print(is_reading)
#                 working_ports.append(dev_port)
#             else:
#                 available_ports.append(dev_port)
#         dev_port -=1

#     return available_ports,working_ports



# arr1,arr2 = list_ports()

# print("\n\n\n")
# for i in arr2:
#     print(i)


# arr = []
# def testDevice(source):
#     cap, frame= cv2.VideoCapture(source) 
#     if cap is None or not cap.isOpened():
#         print('Warning: unable to open video source: ', source)
        
#     else: 
#         arr.append(source)

# for i in range(1,10):
#     testDevice(i) # no printout


# for i in arr:
#     print(i)


# import cv2, glob

# for camera in glob.glob("/dev/video?"):
#     c = cv2.VideoCapture(camera)


# import cv2 as cv
# import PySpin

# print (cv.__version__)

# # provided by Patrick Artner as solution to be working for other cameras than
# #                                                  those of Point Grey (FLIR).

# def testDevice(source):
#    cap = cv.VideoCapture(source) 
#    if cap is None or not cap.isOpened():
#        print('Warning: unable to open video source: ', source)

# # ... PySpin / Spinnaker (wrapper/SDK libary) ...

# system   = PySpin.System.GetInstance()
# cam_list = system.GetCameras()

# cam = ''
# cam_num = 0

# for ID, cam in enumerate(cam_list):
#     # Retrieve TL device nodemap
#     if ID == cam_num:
#         print ('Got cam')
#         cam = cam

#         cam.Init()

#         # ... CV2 again ...

#         for i in range(10):
#             testDevice(i) # no printout

import numpy as np
import cv2 as cv

cap = cv.VideoCapture(6)

# cap.set(3,1920)
# cap.set(4,1080)
# print(cap.get(cv2.CAP_PROP_FPS))
# print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

codec = 0x47504A4D # MJPG

cap.set(cv2.CAP_PROP_FPS, 30.0)

cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M','J','P','G'))

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)

cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    # gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Display the resulting frame
    cv.imshow('frame', frame)
    # print(frame.shape)
    if cv.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()



# source = 10
# arr = []
# while source >0:
#     import pdb
#     pdb.set_trace()
#     cap, frame= cv2.VideoCapture(source)
#     if cap is None or not cap.isOpened():
#         print('Warning: unable to open video source: ', source)
#     else: 
#         arr.append(source)
#     source -= 1

# temp_text = ""
# for i in arr:
#     temp_text += "," + i

# print(temp_text)


# arr = []
# def testDevice(source):
#     cap = cv2.VideoCapture(source) 
#     if cap is None or not cap.isOpened():
#         print('Warning: unable to open video source: ', source)
        
#     else: 
#         arr.append(source)


# for i in range(0,10):
#     testDevice(i) # no printout

# for i in arr:
#     print(i)