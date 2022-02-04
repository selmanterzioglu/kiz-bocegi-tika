# import module 
import sys
from threading import Thread
from PyQt5.QtWidgets import *
import time 
 

class ListBox(QWidget):

    def __init__(self):
        super().__init__()

        self.Button()

    def Button(self):

        #  add push butotn
        clear_btn = QPushButton("Click  me", self)  
        clear_btn.clicked.connect(self.thread)

        #set geometry
        self.setGeometry(200, 200, 200, 200)

        #display qlistwidet
        self.show()

    def thread(self):
        t1 = Thread(target=self.Operation)
        t1.start()

    def Operation(self):
        print("time start")
        time.sleep(10)
        print("time stop")

    

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # call listbox class
    ex = ListBox()

    #close the window
    sys.exit(app.exec_())



