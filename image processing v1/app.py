import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
import main_window
from photo_viewer import PhotoViewer
import stain_segmentation as Seg

class BPA_App(QtGui.QMainWindow, main_window.Ui_MainWindow):
    def __init__(self, parent=None):
        super(BPA_App, self).__init__(parent)
        self.setupUi(self)
        self.viewer = PhotoViewer(self.centralwidget)
        self.viewer.setMinimumSize(500, 500)
        self.horizontalLayout.addWidget(self.viewer)
        self.actionLoad.triggered.connect(self.load_image)
        self.actionSegment_Image.triggered.connect(self.segment_image)
        self.file_name = ""

    def load_image(self):
        self.file_name = QtGui.QFileDialog.getOpenFileName(self, 'Open file', 
         'c:\\',"Image files (*.jpg *.gif *.png *.tif)")
        if self.file_name:
            self.viewer.setPhoto(pixmap=QtGui.QPixmap(self.file_name))

    def segment_image(self):
        Seg.bloodstain_segmentation(self.file_name)

def main():
    app = QtGui.QApplication(sys.argv)
    gui = BPA_App()
    gui.show()
    app.exec_()

if __name__ == '__main__':
   main()