import enum
from PyQt5 import QtWidgets, QtGui


class ToolMode(enum.Enum):
    pen = 1
    eraser = 2
    fill = 3


class Canvas(QtWidgets.QLabel):
    def __init__(self, w, h, back_clr='#ffffff', pen_color='#000000'):
        super().__init__()
        self.canvas_width = w
        self.canvas_height = h
        pixmap = QtGui.QPixmap(self.canvas_width, self.canvas_height)
        pixmap.fill(QtGui.QColor(back_clr))  # background of paint
        self.setPixmap(pixmap)
        self.last_x, self.last_y = None, None
        self.pen_color = QtGui.QColor(pen_color)
        self.pen_width = 2
        self.mode = ToolMode.pen

    def set_pen_color(self, color):
        self.pen_color = QtGui.QColor(color)

    def set_pen_size(self, size):
        self.pen_width = size

    def mouseMoveEvent(self, e):
        if self.mode == ToolMode.pen:
            if self.last_x is None:
                self.last_x = e.x()
                self.last_y = e.y()
                return
            painter = QtGui.QPainter(self.pixmap())
            p = painter.pen()
            p.setWidth(self.pen_width)
            p.setColor(self.pen_color)
            painter.setPen(p)
            painter.drawLine(self.last_x, self.last_y, e.x(), e.y())
            painter.end()
            self.update()
            self.last_x = e.x()
            self.last_y = e.y()

    def mouseReleaseEvent(self, e):
        if self.mode == ToolMode.pen:
            self.last_x = None
            self.last_y = None
