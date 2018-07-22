import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
import main_window

class BPA_App(QtGui.QMainWindow, main_window.Ui_MainWindow):
    def __init__(self, parent=None):
        super(BPA_App, self).__init__(parent)
        self.setupUi(self)
        self.actionLoad.triggered.connect(self.load_image)

    def load_image(self):
        file_name = QtGui.QFileDialog.getOpenFileName(self, 'Open file', 
         'c:\\',"Image files (*.jpg *.gif *.png *.tif)")
        if file_name:
            scene = QtGui.QGraphicsScene()
            scene.addPixmap(QtGui.QPixmap(file_name))
            self.graphicsView.setScene(scene)

def main():
    app = QtGui.QApplication(sys.argv)
    gui = BPA_App()
    gui.show()
    app.exec_()

if __name__ == '__main__':
   main()