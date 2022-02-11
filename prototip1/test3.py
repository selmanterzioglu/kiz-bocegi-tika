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


import cv2 as cv
import PySpin

print (cv.__version__)

# provided by Patrick Artner as solution to be working for other cameras than
#                                                  those of Point Grey (FLIR).

def testDevice(source):
   cap = cv.VideoCapture(source) 
   if cap is None or not cap.isOpened():
       print('Warning: unable to open video source: ', source)

# ... PySpin / Spinnaker (wrapper/SDK libary) ...

system   = PySpin.System.GetInstance()
cam_list = system.GetCameras()

cam = ''
cam_num = 0

for ID, cam in enumerate(cam_list):
    # Retrieve TL device nodemap
    if ID == cam_num:
        print ('Got cam')
        cam = cam

        cam.Init()

        # ... CV2 again ...

        for i in range(10):
            testDevice(i) # no printout