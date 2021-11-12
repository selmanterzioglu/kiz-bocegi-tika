import os
import os.path

class FileProcess():

    def __init__(self):
        self.path = ""
        self.FileName = ""

    def setPath(self, filePath):
        os.chdir(filePath)
        self.path = filePath
        

    def setFileName (self, fileName):
        self.FileName = fileName

    def get_current_path_os(self,):
        return os.getcwd()

    def getFilePath(self):
        return self.get_current_path_os() + self.FileName
        
    def file_exist(self):
        if os.path.exists(self.getFilePath):
            return True
        
    def make_directory(self, directoryPath, directoryName):
        self.setPath(directoryPath)
        try: 
            os.makedirs(directoryName)
        except FileExistsError:
            pass
    
    def make_file(self, filePath, fileName):
        self.setPath(filePath)
        try: 
            os.makedirs(fileName)
        except FileExistsError:
            pass


