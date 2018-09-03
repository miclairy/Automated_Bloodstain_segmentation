import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
import main_window
import features_dialog
import batch_dialog
from photo_viewer import PhotoViewer
import stain_segmentation as Seg
import cv2
from PIL import Image
import os
import progressbar
import batch_process

class BPA_App(QtGui.QMainWindow, main_window.Ui_MainWindow):
    def __init__(self, parent=None):
        super(BPA_App, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Automated Blood Stain Pattern Analysis - ABPA")
        self.viewer = PhotoViewer(self.centralwidget)
        self.viewer.setMinimumSize(500, 500)
        self.horizontalLayout.addWidget(self.viewer)
        self.actionLoad.triggered.connect(self.load_image)
        self.actionExport.triggered.connect(self.export)
        self.actionSegment_Image.triggered.connect(self.show_metrics)
        self.actionBatch_process.triggered.connect(self.show_batch_dialog)
        self.file_name = ""
        self.folder_name = ''
        self.progressBar.hide()
        self.pixmap = None
        # self.populate_table()
        self.result = None

    def load_image(self):
        self.file_name = QtGui.QFileDialog.getOpenFileName(self, 'Open file', 
         'c:\\',"Image files (*.jpg *.gif *.png *.tif)")
        if self.file_name:
            self.viewer.setPhoto(pixmap=QtGui.QPixmap(self.file_name))
            self.setWindowTitle("ABPA - " + self.file_name)

    def export(self):
        save_path = QtGui.QFileDialog.getSaveFileName(self, 'Open file', 
         'c:\\')
        if save_path:
            save_path = os.path.splitext(save_path)[0]
            self.progressBar.show()
            self.progressBar.setValue(0)
            Seg.export_stain_data(save_path, self.progressBar)
            Seg.pattern.export(save_path)
            self.progressBar.setValue(100)
            cv2.cvtColor(self.result, cv2.COLOR_BGR2RGB, self.result)
            cv2.drawContours(self.result, Seg.pattern.contours, -1, (255,0,255), 3)
            for stain in Seg.pattern.stains:
                stain.annotate(self.result)
            cv2.imwrite(save_path + "-result.jpg", self.result)
            self.progressBar.hide()

    def show_metrics(self):
        Dialog = self.show_dialog(features_dialog.Ui_SegmenationMetrics(), self.segment_image)
        Dialog.exec_()

    def show_dialog(self, dialog, accept):
        Dialog = QtGui.QDialog()
        self.dialog = dialog
        self.dialog.setupUi(Dialog)
        self.dialog.scale_spin.setMinimum(1)
        self.dialog.scale_spin.setValue(Seg.pattern.scale)
        self.dialog.scale_spin.valueChanged.connect(self.update_scale)
        self.dialog.buttonBox.accepted.connect(accept)
        return Dialog

    def update_scale(self, value):
        Seg.pattern.scale = value

    def segment_image(self):
        if self.file_name != "":
            self.progressBar.show()
            self.progressBar.setValue(0)
            image = cv2.imread(str(self.file_name))
            orginal = cv2.imread(str(self.file_name))
            annotations = {'id': self.dialog.id.isChecked(), 
                        'ellipse': self.dialog.ellipse.isChecked(), 
                        'outline': self.dialog.outline.isChecked(), 
                        'center': self.dialog.center.isChecked(),
                        'directionality': self.dialog.directionality.isChecked(),  
                        'direction_line': self.dialog.direction_line.isChecked(), 
                        'gamma': self.dialog.gamma.isChecked()}
            self.result = Seg.stain_segmentation(image, orginal)
            result = self.result.copy()
            # cv2.cvtColor(image, cv2.COLOR_BGR2RGB, image)
            Seg.pattern.image = result
            Seg.pattern.name = self.file_name
            self.set_image()
            self.populate_tables()
            self.viewer.add_annotations(annotations, Seg.pattern)

    def set_image(self):
            height, width, byteValue = self.result.shape
            bytesPerLine = 3 * width
            cv2.cvtColor(self.result, cv2.COLOR_BGR2RGB, self.result)
            qImg = QtGui.QImage(self.result.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
            self.pixmap = QtGui.QPixmap.fromImage(qImg)
            self.viewer.setPhoto(pixmap=self.pixmap)
            
    def populate_tables(self):
        self.clear_tables()
        self.populate_stain_table()
        self.populate_pattern_table()
        self.progressBar.setValue(100)
        self.progressBar.hide()

    def populate_stain_table(self):
        self.tableWidget.setColumnCount(13)
        self.tableWidget.setRowCount(len(Seg.pattern.stains))
        self.tableWidget.itemClicked.connect(self.show_stain)
        headers = "position x;position y;area px;area_mm;width ellipse;height ellipse;angle;gamma;direction;solidity;circularity;intensity"
        self.tableWidget.setHorizontalHeaderLabels(headers.split(";"))
        ids = [str(i) for i in range(0, len(Seg.pattern.stains))]
        self.tableWidget.setVerticalHeaderLabels(ids)
        j = 0
        for stain in progressbar.progressbar(Seg.pattern.stains):
            percent = (j / len(Seg.pattern.stains)) * 50
            self.progressBar.setValue(percent)
            stain_data = stain.get_summary_data()            
            for i in range(1,13):
                if stain_data[i] != None:
                    self.tableWidget.setItem(j,i-1, QtGui.QTableWidgetItem(str(stain_data[i])))
            j += 1
        self.tableWidget.show()

    def show_stain(self, item):
        position = (int(self.tableWidget.item(item.row(), 0).text()),
                    int(self.tableWidget.item(item.row(), 1).text()))
        self.viewer.add_rectangle(position[0] - 50, position[1] - 50, 100, 100)

    def populate_pattern_table(self):
        metrics = ["Linearity - Polyline fit", "R^2", "Distribution - ratio stain number to convex hull area", 
                                "ratio stain area to convex hull area", "Convergence - point of highest density", "box of %60 of intersections"]
        self.pattern_table_widget.setColumnCount(2)
        self.pattern_table_widget.setRowCount(len(metrics))
        self.pattern_table_widget.setHorizontalHeaderLabels(["Metric", "Value"])
        pattern_data = Seg.pattern.get_summary_data()

        for i in range(len(pattern_data)):
            self.pattern_table_widget.setItem(i, 0, QtGui.QTableWidgetItem(str(metrics[i])))
            self.pattern_table_widget.setItem(i, 1, QtGui.QTableWidgetItem(str(pattern_data[i])))

    def clear_tables(self):
        self.tableWidget.setRowCount(0)
        self.tableWidget.clear()
        self.pattern_table_widget.setRowCount(0)
        self.pattern_table_widget.clear()

    def show_batch_dialog(self):   
        self.batch_dialog = batch_dialog.Ui_BatchProcessing()
        Dialog = self.show_dialog(self.batch_dialog, self.batch_process)
        self.batch_dialog.folder_path.clicked.connect(self.open_folder)
        self.batch_dialog.output_path.clicked.connect(self.output_folder)
        Dialog.exec_()
        
    def open_folder(self):
        folder_name = QtGui.QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\', QtGui.QFileDialog.ShowDirsOnly)
        self.batch_dialog.folder_path_edit.setText(folder_name)

    def output_folder(self):
        out_folder = QtGui.QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\', QtGui.QFileDialog.ShowDirsOnly)
        self.batch_dialog.output_path_edit.setText(out_folder)

    def batch_process(self):
        self.progressBar.show()
        self.progressBar.setValue(0)
        folder_name = self.batch_dialog.folder_path_edit.text()
        output_folder = self.batch_dialog.output_path_edit.text()
        scale = self.batch_dialog.scale_spin.value()
        if folder_name:
            Dialog = QtGui.QDialog()
            self.dialog.setupUi(Dialog)
            self.setWindowTitle("ABPA - " + folder_name)
            if folder_name[-1] != '/' and folder_name[-1] != '\\':
                folder_name += "/"
            batch_process.segment_images(folder_name, output_folder, scale, self.progressBar)     
                  


def main():
    app = QtGui.QApplication(sys.argv)
    gui = BPA_App()
    gui.show()
    app.exec_()

if __name__ == '__main__':
   main()
