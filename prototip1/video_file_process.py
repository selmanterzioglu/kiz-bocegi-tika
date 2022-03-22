from datetime import datetime
import glob
from http.server import executable
import os

"""
Usage Guide:
    test_object = File_Process(video_data_directory_name="video_data_folder")
"""
class File_Process():

    def __init__(self, video_data_directory_name):
        self.video_data_directory_name = video_data_directory_name
        self.video_name = self.generate_video_name()
        self.video_extension = None
        self.data_folder_path = None

        self.create_data_folder()
        self.update_data_folder_path()

    def delete_files(self, file_path,  extension):
        glob_string = "{}/*.{}".format(file_path, extension)

        files = glob.glob(glob_string)

        for f in files:
            try:
                os.remove(f)
            except OSError as e:
                print("Error: %s : %s" % (f, e.strerror))


    def update_data_folder_path(self):
        self.data_folder_path = self.get_path_os() + "\\" +  self.video_data_directory_name + "\\" 
    
    def create_data_folder(self):
        self.make_directory(self.video_data_directory_name)

    def make_directory(self, new_directory_name):
        try: 
            os.makedirs(new_directory_name)
        except FileExistsError:
            pass

    def generate_video_name(self):
        date = datetime.now()
        year = date.year
        month = date.month
        day = date.day
        hour = date.hour
        minute = date.minute
        second = date.second
        
        videoName = "{}-{}-{}_{}-{}-{}_".format(day, month, year, hour, minute, second)
        
        return videoName
    
    def get_video_name(self):
        return self.video_name

    def get_video_extension(self):
        return self.video_extension
    
    def get_data_folder_path(self):
        return self.data_folder_path
    
    def get_path_os(self):
        return os.getcwd()
        
    def set_video_extension(self, video_extension):
        self.video_extension = video_extension

    def set_video_name(self, video_name):
        self.video_name = video_name

if __name__ == "__main__":
    a = File_Process(video_data_directory_name="video_data_folder")
    print(a.get_video_name())