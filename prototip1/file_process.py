from fileProcess import FileProcess
import cv2
from datetime import datetime
import time
import os

class File_Process():
    
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


if __name__ == '__main__':
    a = videoProcess()
    a.captureVideo(".mp4", 1)

