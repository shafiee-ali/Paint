import enum

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtWidgets import QFileDialog


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
    """
    this is a special widget that has drawing functions
    """
    def __init__(self, w, h, back_clr='#ffffff', pen_color='#000000',pensize=1):
        """

        :param w: width of canvas
        :param h: height of canvas
        :param back_clr: background color of canvas
        :param pen_color: pen color of canvas
        :param pensize: pen size of canvas
        """
        super().__init__()
        self.setCursor(QCursor(QtCore.Qt.CrossCursor))
        self.canvas_width = w
        self.canvas_height = h
        pixmap = QtGui.QPixmap(self.canvas_width, self.canvas_height)

        self.background_color = back_clr
        pixmap.fill(QtGui.QColor(self.background_color))  # background of paint
        self.setPixmap(pixmap)
        self.last_x, self.last_y = None, None
        self.pen_color = QtGui.QColor(pen_color)
        self.pen_width = pensize
        self.mode = ToolMode.pen
        self.shape_mode = None
        self.begin_shape_point = None
        self.end_shape_point = None
        self.before_drawing_shape_pixmap = None

        self.undo_stack = list()
        self.redo_stack = list()

    def set_pen_color(self, color):
        """
        set pen color

        :param color: (string) hex color (like:"#FFFFFF")
        :return: nothing
        """
        self.pen_color = QtGui.QColor(color)

    def set_pen_size(self, size):
        """
        set pen size

        :param size: width of pen
        :return: nothing
        """
        self.pen_width = size

    def save_pixmap_as_image(self):
        """
        this function will save canvas as image
        :return: noting
        """
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()",  "", "Image Files (*.png *.jpg *.bmp)")
        if file_name:
            if file_name[-4:] != '.png' and file_name[-4:] != '.jpg' and file_name[-4:] != '.bmp':
                file_name += '.png'
            self.pixmap().save(file_name)

    def open_image_as_pixmap(self):
        """
        this function will open an image in canvas
        :return: noting
        """
        file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "Image Files (*.png *.jpg *.bmp)")
        if file_name:
            new_pixmap = QPixmap(file_name)
            new_pixmap = new_pixmap.scaled(self.canvas_width, self.canvas_height, QtCore.Qt.KeepAspectRatio)
            self.setPixmap(new_pixmap)

    def set_mode(self, new_mode):
        """
        set mode of tool (which tool we are using ex: pen, eraser & etc)
        :param new_mode: (type:ToolMode)name of the tool we want to use
        :return: noting
        """
        if new_mode == ToolMode.pen.name:
            self.mode = ToolMode.pen
        if new_mode == ToolMode.eraser.name:
            self.mode = ToolMode.eraser
        if new_mode == ToolMode.fill.name:
            self.mode = ToolMode.fill
        if new_mode == ToolMode.shape.name:
            self.mode = ToolMode.shape

    def set_shape_mode(self, new_shape_mode):
        """
        if we select shape tool this function will select what shape we want to draw
        :param new_shape_mode: (type:ShapeMode) name of the shape we want to use
        :return: noting
        """
        if new_shape_mode == ShapeMode.line.name:
            self.shape_mode = ShapeMode.line
        if new_shape_mode == ShapeMode.circle.name:
            self.shape_mode = ShapeMode.circle
        if new_shape_mode == ShapeMode.rect.name:
            self.shape_mode = ShapeMode.rect
        if new_shape_mode == ShapeMode.rounded_rect.name:
            self.shape_mode = ShapeMode.rounded_rect

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

    def pen_mode_mouse_press_event(self, e):
        self.last_x = e.x()
        self.last_y = e.y()
        self.painter = QtGui.QPainter(self.pixmap())
        self.p = self.painter.pen()
        self.p.setWidth(self.pen_width)
        self.p.setColor(self.pen_color)
        self.painter.setPen(self.p)
        self.painter.drawPoint(e.x(), e.y())
        self.painter.end()
        self.update()
        self.last_x = e.x()
        self.last_y = e.y()

    def eraser_mode_mouse_press_event(self, e):
        self.last_x = e.x()
        self.last_y = e.y()
        self.painter = QtGui.QPainter(self.pixmap())
        self.p = self.painter.pen()
        self.p.setWidth(self.pen_width)
        eraser_color = QtGui.QColor(self.background_color)
        self.p.setColor(eraser_color)
        self.painter.setPen(self.p)
        self.painter.drawPoint(e.x(), e.y())
        self.painter.end()
        self.update()
        self.last_x = e.x()
        self.last_y = e.y()

    def fill_mode_mouse_press_event(self, e):

        image = self.pixmap().toImage()
        clicked_pixel_color = image.pixelColor(e.x(), e.y()).name()
        self.points_queue = []
        self.points_queue.append((e.x(), e.y()))
        self.have_seen = set()
        self.bfs(clicked_pixel_color)

    def shape_mode_mouse_press_event(self, e):
        self.before_drawing_shape_pixmap = self.pixmap().copy()
        self.begin_shape_point = e.pos()
        self.end_shape_point = e.pos()
        self.drawing_shape()
        self.update()


    def mouseMoveEvent(self, e):
        if self.mode == ToolMode.pen:
            self.pen_mode_mouse_move_event(e)
        elif self.mode == ToolMode.eraser:
            self.eraser_mode_mouse_move_event(e)
        elif self.mode == ToolMode.fill:
            self.fill_mode_mouse_move_event(e)
        elif self.mode == ToolMode.shape:
            self.shape_mode_mouse_move_event(e)

    def pen_mode_mouse_move_event(self, e):
        """

        :param e: (type:mouseEvent)
        :return: noting
        """
        self.painter = QtGui.QPainter(self.pixmap())
        self.p = self.painter.pen()
        self.p.setWidth(self.pen_width)
        self.p.setColor(self.pen_color)
        self.painter.setPen(self.p)
        self.painter.drawLine(self.last_x, self.last_y, e.x(), e.y())
        self.painter.end()
        self.update()
        self.last_x = e.x()
        self.last_y = e.y()

    def eraser_mode_mouse_move_event(self, e):
        self.painter = QtGui.QPainter(self.pixmap())
        self.p = self.painter.pen()
        self.p.setWidth(self.pen_width)
        eraser_color = QtGui.QColor(self.background_color)
        self.p.setColor(eraser_color)
        self.painter.setPen(self.p)
        self.painter.drawLine(self.last_x, self.last_y, e.x(), e.y())
        self.painter.end()
        self.update()
        self.last_x = e.x()
        self.last_y = e.y()

    def shape_mode_mouse_move_event(self, e):
        self.end_shape_point = e.pos()
        self.drawing_shape()
        self.update()

    def fill_mode_mouse_move_event(self, e):
        pass

    def drawing_shape(self):
        self.setPixmap(self.before_drawing_shape_pixmap)
        self.painter = QtGui.QPainter(self.pixmap())
        self.p = self.painter.pen()
        self.p.setWidth(self.pen_width)
        self.p.setColor(self.pen_color)
        self.painter.setPen(self.p)
        if self.shape_mode == ShapeMode.line:
            self.painter.drawLine(self.begin_shape_point.x(), self.begin_shape_point.y(), self.end_shape_point.x(), self.end_shape_point.y())
        elif self.shape_mode == ShapeMode.circle:
            self.painter.drawEllipse(self.begin_shape_point.x(), self.begin_shape_point.y(),
                                self.end_shape_point.x() - self.begin_shape_point.x(),
                                self.end_shape_point.y() - self.begin_shape_point.y())
        elif self.shape_mode == ShapeMode.rect:
            self.painter.drawRect(QtCore.QRect(self.begin_shape_point, self.end_shape_point))
        elif self.shape_mode == ShapeMode.rounded_rect:
            if self.begin_shape_point.x() < self.end_shape_point.x() and self.begin_shape_point.y() < self.end_shape_point.y():
                self.painter.drawRoundedRect(QtCore.QRect(self.begin_shape_point, self.end_shape_point), 10, 10)
            elif self.begin_shape_point.x() < self.end_shape_point.x() and self.begin_shape_point.y() > self.end_shape_point.y():
                correct_begin_shape_point = QtCore.QPoint(self.begin_shape_point.x(), self.end_shape_point.y())
                correct_end_shape_point = QtCore.QPoint(self.end_shape_point.x(), self.begin_shape_point.y())
                self.painter.drawRoundedRect(QtCore.QRect(correct_begin_shape_point, correct_end_shape_point), 10, 10)
            elif self.begin_shape_point.x() > self.end_shape_point.x() and self.begin_shape_point.y() > self.end_shape_point.y():
                correct_begin_shape_point = self.end_shape_point
                correct_end_shape_point = self.begin_shape_point
                self.painter.drawRoundedRect(QtCore.QRect(correct_begin_shape_point, correct_end_shape_point), 10, 10)
            else:
                correct_begin_shape_point = QtCore.QPoint(self.end_shape_point.x(), self.begin_shape_point.y())
                correct_end_shape_point = QtCore.QPoint(self.begin_shape_point.x(), self.end_shape_point.y())
                self.painter.drawRoundedRect(QtCore.QRect(correct_begin_shape_point, correct_end_shape_point), 10, 10)
        self.painter.end()



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

    def get_cardinal_points(self, have_seen, center_pos, initial_color):
        cx, cy = center_pos
        for x, y in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            xx, yy = cx + x, cy + y
            if xx >= 0 and xx < self.canvas_width and yy >= 0 and yy < self.canvas_height and (xx, yy) not in have_seen:
                self.points_queue.append((xx, yy))
                self.have_seen.add((xx, yy))

    def bfs(self, initial_color):
        while self.points_queue:
            x, y = self.points_queue.pop(0)
            curr_color = self.pixmap().toImage().pixelColor(x, y).name()
            if curr_color == initial_color and curr_color != self.pen_color.name():
                self.painter = QtGui.QPainter(self.pixmap())
                self.p = self.painter.pen()
                self.p.setWidth(1)
                self.p.setColor(self.pen_color)
                self.painter.setPen(self.p)
                self.painter.drawPoint(x, y)
                self.update()
                self.painter.end()
                self.get_cardinal_points(have_seen=self.have_seen, center_pos=(x, y), initial_color=initial_color)


    def mouseReleaseEvent(self, e):
        # if self.mode == ToolMode.pen: #TODO:WHY???
        #     self.last_x = None
        #     self.last_y = None
        self.before_drawing_shape_pixmap = None
        self.begin_shape_point = None
        self.end_shape_point = None
        self.redo_stack = list()