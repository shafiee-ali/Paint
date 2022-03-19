import enum

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QCursor, QMovie
from PyQt5.QtWidgets import QFileDialog, QWidget, QLabel

import time, threading

class Coordinates():
    """this class is useed for saving 2D Coordinates"""
    def __init__(self, x, y):
        self.X = x
        self.Y = y

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

class loadingScreen(QWidget):
    """ this class is widget that opens a popup with loading animation"""
    def __init__(self):
        super().__init__()
        self.setFixedSize(100,100)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)

        self.label_animation = QLabel(self)
        self.movie = QMovie("UI/load-icon.gif")
        self.label_animation.setMovie(self.movie)
        self.movie.start()

    def show_loadingScreen(self):
        """ open loading screen popup"""
        self.show()

    def close_loadingScreen(self):
        """ open loading screen popup"""
        self.close()

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
        self.setCursor(QCursor(QtCore.Qt.CrossCursor))  # change cursor when mouse hover on Canvas
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

        self.canvas_image = None  # this variable saves convertion of canvas.pixmap to image

        self.loadingScreen = loadingScreen()

        self._lock = threading.Lock()  # this variable solve race conditions

        self.is_fill = False  # this bool uses for controlling fill in filling daemon
        self.fill_Coordinates = Coordinates(0,0)  # this variable saves Coordination of where filling will start

        self.fill_daemon_thread = threading.Thread(target=self.fill_deamon,daemon=True,name="fill_daemon_thread")
        self.fill_daemon_thread.start()

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


    def fill_deamon(self):
        """
        because filling is heavy task , it wouldn't be done in main thread to prevent app freezing
        so this function will run an background in other thread and cals fill function when it needed
        :return: noting
        """
        while(True):
            if self.is_fill == True:
                self.setEnabled(False)
                self.fill_mode_mouse_press_event(self.fill_Coordinates.X,self.fill_Coordinates.Y)
                self.setEnabled(True)
                self.is_fill = False


    def mousePressEvent(self, e):
        """
        this functions will handles what happends after clicking on canvas based on what tool selected
        :param e: (type:mouseEvent)
        :return: noting
        """
        self.undo_stack.append(self.pixmap().copy())  # make copy of canvas for undo
        if self.mode == ToolMode.fill:
            self.loadingScreen.show_loadingScreen()
            self.fill_Coordinates.X = e.x()
            self.fill_Coordinates.Y = e.y()
            self.is_fill = True  # by setting is_fill = True the fill daemon will do the rest of the work
        elif self.mode == ToolMode.pen:
            self.pen_mode_mouse_press_event(e.x(),e.y())
        elif self.mode == ToolMode.eraser:
            self.eraser_mode_mouse_press_event(e.x(),e.y())
        elif self.mode == ToolMode.shape:
            self.shape_mode_mouse_press_event(e)

    def fill_mode_mouse_press_event(self, x, y):
        """
        this functions will handles what happends after clicking on canvas when fill btn selected
        :param x: (int) Coordinates x
        :param y: (int) Coordinates Y
        :return: noting
        """
        with self._lock:
            start_time = time.time()  # to show how much time needed for filling
            time.sleep(0.05)   # to prevent UI crash because of fast UI refreshing
            self.canvas_image = self.pixmap().toImage() #TODO:
            clicked_pixel_color = self.canvas_image.pixelColor(x, y)
            self.points_queue = []
            self.points_queue.append((x, y))
            self.have_seen = set()
            self.bfs(clicked_pixel_color)  # use Breadth First Search algorithm
            self.setPixmap(QPixmap.fromImage(self.canvas_image))
            print(" filling time :",time.time() - start_time,"sec")  # to show how much time needed for filling
            self.loadingScreen.close_loadingScreen()
            # freeing memory
            self.canvas_image = None
            self.points_queue = []


    def bfs(self, initial_color):
        """
        use Breadth First Search algorithm to find what pixels should change color
        :param initial_color: the color of selected pixel that should change (ex: "#ffffff")
        :return: noting
        """
        pen_color = self.pen_color  # new color that will replace the old color
        while self.points_queue:
            x, y = self.points_queue.pop(0)
            curr_color = self.canvas_image.pixelColor(x, y)
            if curr_color == initial_color and curr_color != pen_color:
                self.canvas_image.setPixelColor(x, y, pen_color)
                self.get_cardinal_points(have_seen=self.have_seen, center_pos=(x, y), initial_color=initial_color)

    def get_cardinal_points(self, have_seen, center_pos, initial_color):
        """
        #TODO: ali shafie complete this
        :param have_seen:
        :param center_pos:
        :param initial_color:
        :return:
        """
        cx, cy = center_pos
        for x, y in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            xx, yy = cx + x, cy + y
            if xx >= 0 and xx < self.canvas_width and yy >= 0 and yy < self.canvas_height and (xx, yy) not in have_seen:
                self.points_queue.append((xx, yy))
                self.have_seen.add((xx, yy))

    def pen_mode_mouse_press_event(self, x, y):
        """
        this functions will handles what happens after clicking on canvas when pen btn selected
        :param x: (int) Coordinates x
        :param y: (int) Coordinates Y
        :return: noting
        """
        self.last_x = x
        self.last_y = y
        self.painter = QtGui.QPainter(self.pixmap())
        self.p = self.painter.pen()
        self.p.setWidth(self.pen_width)
        self.p.setColor(self.pen_color)
        self.painter.setPen(self.p)
        self.painter.drawPoint(x, y)
        self.painter.end()
        self.update()
        self.last_x = x
        self.last_y = y

    def eraser_mode_mouse_press_event(self, x,y):
        """
        this functions will handles what happens after clicking on canvas when eraser btn selected
        :param x: (int) Coordinates x
        :param y: (int) Coordinates Y
        :return: noting
        """
        self.last_x = x
        self.last_y = y
        self.painter = QtGui.QPainter(self.pixmap())
        self.p = self.painter.pen()
        self.p.setWidth(self.pen_width)
        eraser_color = QtGui.QColor(self.background_color)
        self.p.setColor(eraser_color)
        self.painter.setPen(self.p)
        self.painter.drawPoint(x, y)
        self.painter.end()
        self.update()
        self.last_x = x
        self.last_y = y

    def shape_mode_mouse_press_event(self, e):
        """
        this functions will handles what happens after clicking on canvas when a shape btn selected
        :param e: (type:mouseEvent)
        :return: noting
        """
        self.before_drawing_shape_pixmap = self.pixmap().copy()
        self.begin_shape_point = e.pos()
        self.end_shape_point = e.pos()
        self.drawing_shape()
        self.update()

    def mouseMoveEvent(self, e):
        """
            this functions will handles what happens while moving mouse on canvas based on what tool selected
            :param e: (type:mouseEvent)
            :return: noting
        """
        if self.mode == ToolMode.fill:
            pass
        elif self.mode == ToolMode.pen:
            self.pen_mode_mouse_move_event(e)
        elif self.mode == ToolMode.eraser:
            self.eraser_mode_mouse_move_event(e)
        elif self.mode == ToolMode.shape:
            self.shape_mode_mouse_move_event(e)

    def pen_mode_mouse_move_event(self, e):
        """
        this functions will handles what happens while moving mouse on canvas when pen btn selected
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
        """
        this functions will handles what happens while moving mouse on canvas when eraser btn selected
        :param e: (type:mouseEvent)
        :return: noting
        """
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
        """
        this functions will handles what happens while moving mouse on canvas when a shape btn selected
        :param e: (type:mouseEvent)
        :return: noting
        """
        self.end_shape_point = e.pos()
        self.drawing_shape()
        self.update()

    def fill_mode_mouse_move_event(self, e):
        """
        this functions will handles what happens while moving mouse on canvas when fill btn selected
        :param e: (type:mouseEvent)
        :return: noting
        """
        pass

    def drawing_shape(self):
        """
        this function will draw shape on canvas based on shape_mode
        :return: noting
        """
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
        """
        undo's a action on canvas
        :return:
        """
        if self.undo_stack:
            last_pixmap = self.undo_stack.pop()
            self.redo_stack.append(self.pixmap().copy())
            self.setPixmap(last_pixmap)

    def redo_action(self):
        """
        redo's a action on canvas
        :return:
        """
        if self.redo_stack:
            last_pixmap = self.redo_stack.pop()
            self.undo_stack.append(self.pixmap().copy())
            self.setPixmap(last_pixmap)



    def mouseReleaseEvent(self, e):
        """
            this functions will handles what happens after releasing mouse on canvas
            :param e: (type:mouseEvent)
            :return: noting
        """
        # if self.mode == ToolMode.pen: #TODO:WHY???
        #     self.last_x = None
        #     self.last_y = None
        self.before_drawing_shape_pixmap = None
        self.begin_shape_point = None
        self.end_shape_point = None
        self.redo_stack = list()