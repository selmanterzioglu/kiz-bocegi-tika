from PyQt5.QtWidgets import *
from numpy import uint
from main_window import Ui_MainWindow
import sys
import threading
import time


class Window(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    
    def timer(self):
        timer = 10
        while timer>0:
            
            print("{}".format(timer))

            time.sleep(1)
            timer -=1

    def clicked_function(self):
        # self.ui.label2.setText("test")
        thread1 = threading.Thread(target=self.set_text, daemon=True)
        thread2 = threading.Thread(target=self.timer, daemon=True)    

        thread1.start()
        thread2.start()


    def set_text(self):
        print("clicked! this is a test function!")
        self.ui.label.setText("test")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    app.exec_()