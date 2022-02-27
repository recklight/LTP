import sys
import argparse
from DFM import UiDFM, QApplication


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--reset', action='store_true', help="Reset GUI settings.")
    args = parser.parse_args()
    return args


class main(UiDFM):
    def __init__(self):
        super(main, self).__init__()
        self.actionSettings.triggered.connect(lambda: self.cameraConnectDialog.exec())


if __name__ == '__main__':
    args = parse()
    app = QApplication(sys.argv)
    window = main()
    window.read_settings(reset=args.reset)
    window.show()
    app.exec_()
    window.write_settings()
    sys.exit()
