# -*- coding: utf-8 -*-
import argparse
import sys

from PyQt5.QtWidgets import QApplication

from AudioMax import AudioMax


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--reset', action='store_true', help="Reset GUI settings.")
    args = parser.parse_args()
    return args


class main(AudioMax):
    def __init__(self):
        super(main, self).__init__()
        self.actionConnectDevice.triggered.connect(self.connect_devices.exec)
        self.actionConnectPLC.triggered.connect(self.connect_plc.exec)
        self.actionConnectDetector.triggered.connect(self.connect_detector.exec)


if __name__ == '__main__':
    args = parse()
    app = QApplication(sys.argv)
    window = main()
    window.read_settings(reset=args.reset)
    window.show()
    app.exec_()
    window.write_settings()
    sys.exit()
