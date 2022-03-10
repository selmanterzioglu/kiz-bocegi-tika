from datetime import datetime

class File_Process():
    
    def __init__(self,
                 video_file_path,
                 video_name,
                 video_extension,
                ):


        self.video_file_path = video_file_path
        self.video_name = video_name
        self.video_extension = video_extension
        self.create_data_folder()


    def create_video_name(self):
        date = datetime.now()
        year = datetime.strftime(date, '%Y')
        month = datetime.strftime(date, '%m')
        day = datetime.strftime(date, '%d')
        hour = datetime.strftime(date, '%X')
        videoName = "{}-{}-{}-{}".format(year, month, day,hour)
        
        return videoName

    def create_data_folder(self):
        fs = FileProcess()
        fs.make_directory(fs.get_current_path_os(), self.video_file_path)
        fs.setPath(fs.get_current_path_os() + "/" + self.video_file_path)
        self.path = fs.get_current_path_os()

    def get_video_file_path(self):
        return self.video_file_path
    
    def get_video_name(self):
        return self.video_name
    
    def get_video_extension(self):
        return self.video_name

    def set_video_file_path(self, video_file_path ):
        self.video_file_path = video_file_path  
    
    def set_video_name(self, set_video_name):
        self.video_name = set_video_name
    
    def set_video_extension(self, video_extension):
        self.video_extension = video_extension

if __name__ == '__main__':
    a = File_Process("video_data_folder", video_name="video_name", video_extension="video_extension")
    print(a.createVideoName())

