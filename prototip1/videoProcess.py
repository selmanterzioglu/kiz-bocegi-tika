from fileProcess import FileProcess
import cv2
from datetime import datetime
import time
import os

class videoProcess():
    
    def __init__(self):
        self.path = ""
        self.createDataFolder()

    def createVideoName(self):
        date = datetime.now()
        year = datetime.strftime(date, '%Y')
        month = datetime.strftime(date, '%m')
        day = datetime.strftime(date, '%d')
        hour = datetime.strftime(date, '%X')
        videoName = "{}-{}-{}-{}".format(year, month, day,hour)
        
        return videoName

    def createDataFolder(self):
        fs = FileProcess()
        mainDirectory = "videoData"
        fs.make_directory(fs.get_current_path_os(), mainDirectory)
        fs.setPath(fs.get_current_path_os() + "/" + mainDirectory)
        self.path = fs.get_current_path_os()

    def captureVideo(self, videoFormat, videoDuration):
        video = cv2.VideoCapture(0)
        frame_width = int(video.get(3))
        frame_height = int(video.get(4))
        size = (frame_width, frame_height)
        
        fileName = self.createVideoName() + videoFormat
        print(type(fileName))
        print(fileName)
        
        result = cv2.VideoWriter("2021-11-12-16:46:24.mp4",
                                cv2.VideoWriter_fourcc(*'MP4V'),
                                20.0,size)
        
        start = time.time()
        while(int(time.time() - start) < videoDuration):
            now = int (time.time() - start)
            ret, frame = video.read()

            if ret == True:     
                result.write(frame)

        video.release()
        result.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    a = videoProcess()
    a.captureVideo(".mp4", 1)

