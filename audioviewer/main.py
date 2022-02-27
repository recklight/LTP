# -*- coding: utf-8 -*-

"""
@ Author: github.com/recklight
@ main.py
"""
import sys
from PyQt5.QtWidgets import QApplication
from audioviewer import AudioViewer

app = QApplication(sys.argv)
window = AudioViewer()
window.show()
app.exec_()
sys.exit()
