import cv2
import time
import glob
import os 


# Opens the Video file
class screenShootFromVideo():
    videoFileName = ""

    def __init__(self):
        self.welcomeScreen()
    
    def get_video_property(self):
        print("Secilen video: {}".format(self.videoFileName))
        video = cv2.VideoCapture(self.videoFileName)

        if (video.isOpened()):
            fps = video.get(cv2.CAP_PROP_FPS)
            width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
            height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
            frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = (frame_count / fps)

            print("fps: {}".format(fps))
            print("video width: {}".format(width))
            print("video height: {}".format(height))
            print("video duration: {}".format(duration/60))

            video.release()

            return ([fps, width, height, frame_count, duration])

    def welcomeScreen(self):
        self.getVideoFileName()
        video_property = self.get_video_property()


        a = input("Saniyede parcalanmasini istediginiz frame adedini  girin: ")
        total_frame = int(video_property[4]) * int(a)
        fps = int(video_property[3] / total_frame)

        self.getFrameVideo(self.videoFileName, fps)

    def  getVideoFileName(self):
        fileList = []
        for file in os.listdir():
            fileList.append(file)
        
        for i in range(len(fileList)):
            print("[{}] {}".format(str(i), fileList[i]))

        videoNumber = input("lutfen islem yapmak istediginiz video dosyasinin numarasini giriniz: ")

        if (int(videoNumber) >= len(fileList) or  int(videoNumber) < 0):
            print("Lutfen belirtilen secenekler arasinda islem yapiniz..!!")
            self.getVideoFileName()

        self.videoFileName = fileList[int(videoNumber)]
        return 0
        
    def getFrameVideo(self, videoFileName, fps):
        start = time.time()
        cap= cv2.VideoCapture(videoFileName)
        i=0
        a=0
        self.videoFileName = self.videoFileName[:self.videoFileName.rfind(".")]

        while(cap.isOpened()):

            ret, frame = cap.read()    
            if ret == False:
                break
            
            if (i % fps == 0):
                print(self.videoFileName + str(a)+'.jpg')
                cv2.imwrite(self.videoFileName +str(a)+'.jpg',frame)
                a+=1
            i+=1

        cap.release()
        cv2.destroyAllWindows()
        end =  time.time()
        print("gecen sure (saniye): {} \ntoplam {} adet dosya kaydedildi..!".format(str(end-start), a))

    def getVideoProperty(self):
        pass

if __name__ == "__main__":
    a = screenShootFromVideo()
