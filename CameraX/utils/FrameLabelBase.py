from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from Structures import MouseData, QRect


class FrameLabelBase(QLabel):
    def __init__(self, parent=None):
        super(FrameLabelBase, self).__init__(parent)
        self.menu = None
        self.mouseData = MouseData()
        self.drawBox = False
        self.box = QRect()
        self.mouseData.leftButtonRelease = False
        self.mouseData.rightButtonRelease = False

    def mouseReleaseEvent(self, ev):
        # Update cursor position
        self.setMouseCursorPos(ev.pos())
        # On left mouse button release
        if ev.button() == Qt.LeftButton:
            # Set leftButtonRelease flag to True
            self.mouseData.leftButtonRelease = True
            if self.drawBox:
                # Stop drawing box
                self.drawBox = False
                # Save box dimensions
                self.mouseData.selectionBox.setX(self.box.left())
                self.mouseData.selectionBox.setY(self.box.top())
                self.mouseData.selectionBox.setWidth(self.box.width())
                self.mouseData.selectionBox.setHeight(self.box.height())
                # Set leftButtonRelease flag to True
                self.mouseData.leftButtonRelease = True
                # Inform main window of event
                self.newMouseData.emit(self.mouseData)
            # Set leftButtonRelease flag to False
            self.mouseData.leftButtonRelease = False
        # On right mouse button release
        elif ev.button() == Qt.RightButton:
            # If user presses (and then releases) the right mouse button while drawing box, stop drawing box
            if self.drawBox:
                self.drawBox = False
            else:
                # Show context menu
                self.menu.exec(ev.globalPos())
