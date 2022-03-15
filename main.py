# -*- coding: utf-8 -*-

"""
@ author: recklight
@ contact:recognizer.light@gmail.com
@ version: n
@ license: n
@ file: main.py
"""

import sys
import argparse
from ssRobotApp import ssRobotApp, QApplication


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--reset', action='store_true', help="Reset GUI settings.")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    # args = parse()
    app = QApplication(sys.argv)
    window = ssRobotApp()
    # window.read_settings(reset=args.reset)
    window.show()
    app.exec_()
    # window.write_settings()
    sys.exit()
