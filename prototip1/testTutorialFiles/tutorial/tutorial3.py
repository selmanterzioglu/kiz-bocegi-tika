from curses import window
from PyQt5.QtWidgets import *
import sys

class Test(QMainWindow):

    scene  = QGraphicsScene()
    scene.addText("merhaba")

    view = QGraphicsView()
    view.setScene(scene)
    view.show()

if  __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Test()
    sys.exit(app.exec_())