

# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 16:00:52 2019

@author: ebruk
"""
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from code1 import MainWindow

def main():
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
