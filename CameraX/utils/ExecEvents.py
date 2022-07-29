from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QMenu, QAction
from utils.CamFrameLabels import CameraFrameLabel
from utils.ImgProcessListWidgets import UsedListWidget


class CameraFrameLabelWithExec(CameraFrameLabel):
    def mouseReleaseEvent(self, ev):
        self.setMouseCursorPos(ev.pos())
        if ev.button() == Qt.LeftButton:
            self.mouseData.leftButtonRelease = True
            if self.drawBox:
                self.drawBox = False
                self.mouseData.selectionBox.setX(self.box.left())
                self.mouseData.selectionBox.setY(self.box.top())
                self.mouseData.selectionBox.setWidth(self.box.width())
                self.mouseData.selectionBox.setHeight(self.box.height())
                self.mouseData.leftButtonRelease = True
                self.newMouseData.emit(self.mouseData)
            self.mouseData.leftButtonRelease = False
        elif ev.button() == Qt.RightButton:
            if self.drawBox:
                self.drawBox = False
            else:
                self.menu.exec(ev.globalPos())

class UsedListWidgetWithExec(UsedListWidget):
    def contextMenuEvent(self, e):
        item = self.itemAt(self.mapFromGlobal(QCursor.pos()))
        if item:
            menu = QMenu(self)
            delete_action = QAction('刪除', self)
            delete_action.triggered.connect(lambda: self.delete_item(item))
            menu.addAction(delete_action)
            menu.exec(e.globalPos())
        else:
            self.menuProcess.exec(e.globalPos())