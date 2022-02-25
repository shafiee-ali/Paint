import enum
from PyQt5 import QtWidgets, QtGui


class ToolMode(enum.Enum):
    pen = 1
    eraser = 2
    fill = 3
    shape = 4


class ShapeMode(enum.Enum):
    line = 1
    circle = 2
    rect = 3
    rounded_rect = 4


class Canvas(QtWidgets.QLabel):
    def __init__(self, w, h, back_clr='#ffffff', pen_color='#000000'):
        super().__init__()
        self.canvas_width = w
        self.canvas_height = h
        pixmap = QtGui.QPixmap(self.canvas_width, self.canvas_height)
        self.background_color = back_clr
        pixmap.fill(QtGui.QColor(self.background_color))  # background of paint
        self.setPixmap(pixmap)
        self.last_x, self.last_y = None, None
        self.pen_color = QtGui.QColor(pen_color)
        self.pen_width = 2
        self.mode = ToolMode.pen
        self.shape_mode = None

    def set_pen_color(self, color):
        self.pen_color = QtGui.QColor(color)

    def set_pen_size(self, size):
        self.pen_width = size

    def set_mode(self, new_mode):
        if new_mode == "pen":
            self.mode = ToolMode.pen
        if new_mode == "eraser":
            self.mode = ToolMode.eraser
        if new_mode == "fill":
            self.mode = ToolMode.fill
        if new_mode == "shape":
            self.mode = ToolMode.shape

    def pen_mode_mouse_move_event(self, e):
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

    def eraser_mode_mouse_move_event(self, e):
        if self.last_x is None:
            self.last_x = e.x()
            self.last_y = e.y()
            return
        painter = QtGui.QPainter(self.pixmap())
        p = painter.pen()
        p.setWidth(self.pen_width)
        eraser_color = QtGui.QColor(self.background_color)
        p.setColor(eraser_color)
        painter.setPen(p)
        painter.drawLine(self.last_x, self.last_y, e.x(), e.y())
        painter.end()
        self.update()
        self.last_x = e.x()
        self.last_y = e.y()

    def shape_mode_mouse_move_event(self, e):
        if self.shape_mode == ShapeMode.line:
            pass
        if self.shape_mode == ShapeMode.circle:
            pass
        if self.shape_mode == ShapeMode.rect:
            pass
        if self.shape_mode == ShapeMode.rounded_rect:
            pass


    def mouseMoveEvent(self, e):
        if self.mode == ToolMode.pen:
            self.pen_mode_mouse_move_event(e)
        elif self.mode == ToolMode.eraser:
            self.eraser_mode_mouse_move_event(e)
        elif self.mode == ToolMode.fill:
            pass
        elif self.mode == ToolMode.shape:
            self.shape_mode_mouse_move_event()





    def mouseReleaseEvent(self, e):
        if self.mode == ToolMode.pen:
            self.last_x = None
            self.last_y = None
