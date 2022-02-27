# -*- coding: utf-8 -*-

"""
@ Author: github.com/recklight
@ main.py
"""

import sys
import argparse
from imgplat import ImgPlatform, QApplication


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--reset', action='store_true', help="Reset GUI settings.")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    # args = parse()
    app = QApplication(sys.argv)
    window = ImgPlatform()
    # window.read_settings(reset=args.reset)
    window.show()
    app.exec_()
    # window.write_settings()
    sys.exit()
