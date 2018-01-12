#!/usr/bin/env python3

import sys, logging, os
from PyQt5 import QtGui, QtWidgets, QtCore

class ExampleWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.widget_close = None
        self.context = None
        self.initUI()
        
    def initUI(self):
        self.resize(720, 300)
        self.setWindowTitle("QT Window")
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        
        label = QtWidgets.QLabel('Label')
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(label)
        self.setLayout(layout)
        
        self.show()
    
    def closeEvent(self, event):
        self.widget_close = True
        self.deleteLater()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Plastique")
    window = ExempleWidget()
    sys.exit(app.exec())
