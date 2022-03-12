import enum
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QKeySequence, QPixmap
from PyQt5.QtWidgets import QShortcut, QAction, QMenu, QFileDialog, QColorDialog


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
        self.begin_shape_point = None
        self.end_shape_point = None
        self.before_drawing_shape_pixmap = None

        self.undo_stack = list()
        self.redo_stack = list()



    def set_pen_color(self, color):
        self.pen_color = QtGui.QColor(color)

    def set_pen_size(self, size):
        self.pen_width = size

    def save_pixmap_as_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()",  "", "Image Files (*.png *.jpg *.bmp)")
        if file_name:
            if file_name[-4:] != '.png' and file_name[-4:] != '.jpg' and file_name[-4:] != '.bmp':
                file_name += '.png'
            self.pixmap().save(file_name)

    def open_image_as_pixmap(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "Image Files (*.png *.jpg *.bmp)")
        if file_name:
            new_pixmap = QPixmap(file_name)
            new_pixmap = new_pixmap.scaled(self.canvas_width, self.canvas_height, QtCore.Qt.KeepAspectRatio)
            self.setPixmap(new_pixmap)

    def set_mode(self, new_mode):
        if new_mode == "pen":
            self.mode = ToolMode.pen
        if new_mode == "eraser":
            self.mode = ToolMode.eraser
        if new_mode == "fill":
            self.mode = ToolMode.fill
        if new_mode == "shape":
            self.mode = ToolMode.shape

    def set_shape_mode(self, new_shape_mode):
        if new_shape_mode == "line":
            self.shape_mode = ShapeMode.line
        if new_shape_mode == "circle":
            self.shape_mode = ShapeMode.circle
        if new_shape_mode == "rect":
            self.shape_mode = ShapeMode.rect
        if new_shape_mode == "rounded rect":
            self.shape_mode = ShapeMode.rounded_rect

    def pen_mode_mouse_move_event(self, e):
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
        self.end_shape_point = e.pos()
        self.drawing_shape()
        self.update()

    def fill_mode_mouse_move_event(self, e):
        pass

    def mousePressEvent(self, e):
        self.undo_stack.append(self.pixmap().copy())
        if self.mode == ToolMode.pen:
            self.pen_mode_mouse_press_event(e)
        elif self.mode == ToolMode.eraser:
            self.eraser_mode_mouse_press_event(e)
        elif self.mode == ToolMode.fill:
            self.fill_mode_mouse_press_event(e)
        elif self.mode == ToolMode.shape:
            self.shape_mode_mouse_press_event(e)

    def shape_mode_mouse_press_event(self, e):
        self.before_drawing_shape_pixmap = self.pixmap().copy()
        self.begin_shape_point = e.pos()
        self.end_shape_point = e.pos()
        self.drawing_shape()
        self.update()

    def drawing_shape(self):
        self.setPixmap(self.before_drawing_shape_pixmap)
        painter = QtGui.QPainter(self.pixmap())
        p = painter.pen()
        p.setWidth(self.pen_width)
        p.setColor(self.pen_color)
        painter.setPen(p)
        if self.shape_mode == ShapeMode.line:
            painter.drawLine(self.begin_shape_point.x(), self.begin_shape_point.y(), self.end_shape_point.x(), self.end_shape_point.y())
        elif self.shape_mode == ShapeMode.circle:
            painter.drawEllipse(self.begin_shape_point.x(), self.begin_shape_point.y(),
                                self.end_shape_point.x() - self.begin_shape_point.x(),
                                self.end_shape_point.y() - self.begin_shape_point.y())
        elif self.shape_mode == ShapeMode.rect:
            painter.drawRect(QtCore.QRect(self.begin_shape_point, self.end_shape_point))
        elif self.shape_mode == ShapeMode.rounded_rect:
            if self.begin_shape_point.x() < self.end_shape_point.x() and self.begin_shape_point.y() < self.end_shape_point.y():
                painter.drawRoundedRect(QtCore.QRect(self.begin_shape_point, self.end_shape_point), 10, 10)
            elif self.begin_shape_point.x() < self.end_shape_point.x() and self.begin_shape_point.y() > self.end_shape_point.y():
                correct_begin_shape_point = QtCore.QPoint(self.begin_shape_point.x(), self.end_shape_point.y())
                correct_end_shape_point = QtCore.QPoint(self.end_shape_point.x(), self.begin_shape_point.y())
                painter.drawRoundedRect(QtCore.QRect(correct_begin_shape_point, correct_end_shape_point), 10, 10)
            elif self.begin_shape_point.x() > self.end_shape_point.x() and self.begin_shape_point.y() > self.end_shape_point.y():
                correct_begin_shape_point = self.end_shape_point
                correct_end_shape_point = self.begin_shape_point
                painter.drawRoundedRect(QtCore.QRect(correct_begin_shape_point, correct_end_shape_point), 10, 10)
            else:
                correct_begin_shape_point = QtCore.QPoint(self.end_shape_point.x(), self.begin_shape_point.y())
                correct_end_shape_point = QtCore.QPoint(self.begin_shape_point.x(), self.end_shape_point.y())
                painter.drawRoundedRect(QtCore.QRect(correct_begin_shape_point, correct_end_shape_point), 10, 10)

    def mouseMoveEvent(self, e):
        if self.mode == ToolMode.pen:
            self.pen_mode_mouse_move_event(e)
        elif self.mode == ToolMode.eraser:
            self.eraser_mode_mouse_move_event(e)
        elif self.mode == ToolMode.fill:
            self.fill_mode_mouse_move_event(e)
        elif self.mode == ToolMode.shape:
            self.shape_mode_mouse_move_event(e)

    def pen_mode_mouse_press_event(self, e):
        self.last_x = e.x()
        self.last_y = e.y()
        painter = QtGui.QPainter(self.pixmap())
        p = painter.pen()
        p.setWidth(self.pen_width)
        p.setColor(self.pen_color)
        painter.setPen(p)
        painter.drawPoint(e.x(), e.y())
        painter.end()
        self.update()
        self.last_x = e.x()
        self.last_y = e.y()

    def undo_action(self):
        if self.undo_stack:
            last_pixmap = self.undo_stack.pop()
            self.redo_stack.append(self.pixmap().copy())
            self.setPixmap(last_pixmap)
            # self.update()

    def redo_action(self):
        if self.redo_stack:
            last_pixmap = self.redo_stack.pop()
            self.undo_stack.append(self.pixmap().copy())
            self.setPixmap(last_pixmap)

    def eraser_mode_mouse_press_event(self, e):
        self.last_x = e.x()
        self.last_y = e.y()
        painter = QtGui.QPainter(self.pixmap())
        p = painter.pen()
        p.setWidth(self.pen_width)
        eraser_color = QtGui.QColor(self.background_color)
        p.setColor(eraser_color)
        painter.setPen(p)
        painter.drawPoint(e.x(), e.y())
        painter.end()
        self.update()
        self.last_x = e.x()
        self.last_y = e.y()

    def fill_mode_mouse_press_event(self, e):
        pass

    def mouseReleaseEvent(self, e):
        if self.mode == ToolMode.pen:
            self.last_x = None
            self.last_y = None
        self.redo_stack = list()