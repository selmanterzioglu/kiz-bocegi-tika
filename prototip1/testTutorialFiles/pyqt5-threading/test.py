from PyQt5.QtWidgets import *
from numpy import uint
from main_window import Ui_MainWindow
import sys

class Window(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


    def test(self):
        self.ui.label2.setText("test")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    app.exec_()