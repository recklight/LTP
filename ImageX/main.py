# -*- coding: utf-8 -*-

"""
@ Author: github.com/recklight
@ main.py
"""

import sys
import argparse

from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QMenu, QAction

from listWidgets import UsedListWidget
from imgplat import ImgPlatform, QApplication


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--reset', action='store_true', help="Reset GUI settings.")
    args = parser.parse_args()
    return args


class main(ImgPlatform):
    def __init__(self):
        super(main, self).__init__()
        self.useListWidget = uListWidget(self)
        self.DW_fcns_used_verticalLayout.deleteLater()
        self.DW_fcns_used_verticalLayout.addWidget(self.useListWidget)


class uListWidget(UsedListWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def contextMenuEvent(self, e):
        item = self.itemAt(self.mapFromGlobal(QCursor.pos()))
        if not item: return
        menu = QMenu()
        delete_action = QAction('删除', self)
        delete_action.triggered.connect(lambda: self.delete_item(item))
        menu.addAction(delete_action)
        menu.exec(QCursor.pos())


if __name__ == '__main__':
    # args = parse()
    app = QApplication(sys.argv)
    window = main()
    # window.read_settings(reset=args.reset)
    window.show()
    app.exec_()
    # window.write_settings()
    sys.exit()
