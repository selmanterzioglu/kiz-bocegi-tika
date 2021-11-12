from fileProcess import FileProcess
import cv2
from datetime import datetime
import time


class videoProcess():
    
    def __init__(self):
        self.path = ""
        self.createDataFolder()


    def createVideoName():
        date = datetime.now()
        year = datetime.strftime(date, '%Y')
        month = datetime.strftime(date, '%m')
        day = datetime.strftime(date, '%d')
        hour = datetime.strftime(date, '%X')

        videoName = year, month, day,hour
        videoName = "-".join(videoName)

        return videoName

    def createDataFolder(self):
        fs = FileProcess()
        mainDirectory = "videoData"
        fs.make_directory(fs.get_current_path_os(), mainDirectory)
        fs.setPath(fs.get_current_path_os() + "/" + mainDirectory)
        self.path = fs.get_current_path_os()

    def captureVideo(self, videoName, videoFormat, videoDuration):
        video = cv2.VideoCapture(0)
        frame_width = int(video.get(3))
        frame_height = int(video.get(4))
        size = (frame_width, frame_height)

        result = cv2.VideoWriter(videoName + videoFormat, 
                                cv2.VideoWriter_fourcc(*'MJPG'),
                                10, size)
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
    a.save_video_file()
