import sys
import argparse
from yolov5_train import YoloV5Train, QApplication


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--reset', action='store_true', help="Reset GUI settings.")
    args = parser.parse_args()
    return args


class main(YoloV5Train):
    def __init__(self):
        super(main, self).__init__()
        self.actionModelSize.triggered.connect(self.set_model_size)
        self.actionParameter.triggered.connect(lambda: self.parameterDialog.exec())

    def set_model_size(self):
        if self.modelDialog.exec():
            self.modelSize.setText(self.modelDialog.get_modelSize())


if __name__ == '__main__':
    # args = parse()
    app = QApplication(sys.argv)
    window = main()
    # window.read_settings(reset=args.reset)
    window.show()
    app.exec_()
    # window.write_settings()
    sys.exit()
