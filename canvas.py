import enum
from PyQt5 import QtWidgets, QtGui


class toolMode(enum.Enum):
   pen = 1
   eraser = 2
   fill = 3

class Canvas(QtWidgets.QLabel):
    def __init__(self,W,H,backclr='#ffffff',pencolor='#000000'):
        super().__init__()
        self.canvas_Width = W
        self.canvas_height = H
        pixmap = QtGui.QPixmap(self.canvas_Width, self.canvas_height)
        pixmap.fill(QtGui.QColor(backclr)) #background of paint
        self.setPixmap(pixmap)
        self.last_x, self.last_y = None, None
        self.pen_color = QtGui.QColor(pencolor)
        self.pen_Width = 1
        self.mode = toolMode.pen

    def set_pen_color(self, color):
        self.pen_color = QtGui.QColor(color)
    def set_pen_size(self,size):
        self.pen_Width = size

    def mouseMoveEvent(self, e):

        if self.mode == toolMode.pen:
            if self.last_x is None:
                self.last_x = e.x()
                self.last_y = e.y()
                return
            painter = QtGui.QPainter(self.pixmap())
            p = painter.pen()
            p.setWidth(self.pen_Width)
            p.setColor(self.pen_color)
            painter.setPen(p)
            painter.drawLine(self.last_x, self.last_y, e.x(), e.y())
            painter.end()
            self.update()
            self.last_x = e.x()
            self.last_y = e.y()
        elif self.mode == toolMode.eraser:
            pass  # TODO
        elif self.mode == toolMode.fill:
            pass  # TODO
        else:
            pass

    def mouseReleaseEvent(self, e):
        if self.mode == toolMode.pen:
            self.last_x = None
            self.last_y = None
        elif self.mode == toolMode.eraser:
            pass  # TODO
        elif self.mode == toolMode.fill:
            pass  # TODO
        else:
            pass
