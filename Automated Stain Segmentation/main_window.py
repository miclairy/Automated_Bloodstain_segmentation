# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1075, 837)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralwidget.setAutoFillBackground(True)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.horizontalLayout.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.StainData = QtGui.QWidget()
        self.StainData.setObjectName(_fromUtf8("StainData"))
        self.gridLayout_3 = QtGui.QGridLayout(self.StainData)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.tableWidget = QtGui.QTableWidget(self.StainData)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.horizontalLayout_3.addWidget(self.tableWidget)
        self.gridLayout_3.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
        self.tabWidget.addTab(self.StainData, _fromUtf8(""))
        self.PatternData = QtGui.QWidget()
        self.PatternData.setObjectName(_fromUtf8("PatternData"))
        self.gridLayout_2 = QtGui.QGridLayout(self.PatternData)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pattern_table_widget = QtGui.QTableWidget(self.PatternData)
        self.pattern_table_widget.setMinimumSize(QtCore.QSize(361, 0))
        self.pattern_table_widget.setAutoFillBackground(False)
        self.pattern_table_widget.setObjectName(_fromUtf8("pattern_table_widget"))
        self.pattern_table_widget.setColumnCount(0)
        self.pattern_table_widget.setRowCount(0)
        self.horizontalLayout_2.addWidget(self.pattern_table_widget)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.tabWidget.addTab(self.PatternData, _fromUtf8(""))
        self.horizontalLayout.addWidget(self.tabWidget)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1075, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuChoose_Image = QtGui.QMenu(self.menubar)
        self.menuChoose_Image.setObjectName(_fromUtf8("menuChoose_Image"))
        self.menuProcess = QtGui.QMenu(self.menubar)
        self.menuProcess.setObjectName(_fromUtf8("menuProcess"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionLoad = QtGui.QAction(MainWindow)
        self.actionLoad.setObjectName(_fromUtf8("actionLoad"))
        self.actionExport = QtGui.QAction(MainWindow)
        self.actionExport.setObjectName(_fromUtf8("actionExport"))
        self.actionSegment_Image = QtGui.QAction(MainWindow)
        self.actionSegment_Image.setObjectName(_fromUtf8("actionSegment_Image"))
        self.actionBatch_process = QtGui.QAction(MainWindow)
        self.actionBatch_process.setObjectName(_fromUtf8("actionBatch_process"))
        self.menuChoose_Image.addAction(self.actionLoad)
        self.menuChoose_Image.addAction(self.actionExport)
        self.menuProcess.addAction(self.actionSegment_Image)
        self.menuProcess.addAction(self.actionBatch_process)
        self.menubar.addAction(self.menuChoose_Image.menuAction())
        self.menubar.addAction(self.menuProcess.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.StainData), _translate("MainWindow", "Stain Data", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.PatternData), _translate("MainWindow", "Pattern Data", None))
        self.menuChoose_Image.setTitle(_translate("MainWindow", "File", None))
        self.menuProcess.setTitle(_translate("MainWindow", "Process", None))
        self.actionLoad.setText(_translate("MainWindow", "Load", None))
        self.actionExport.setText(_translate("MainWindow", "Export", None))
        self.actionSegment_Image.setText(_translate("MainWindow", "Segment Image", None))
        self.actionBatch_process.setText(_translate("MainWindow", "Batch Process", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

