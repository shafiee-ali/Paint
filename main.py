from functools import partial

from PyQt5.QtGui import QKeySequence, QCursor
from PyQt5.QtWidgets import QShortcut, QColorDialog, QPushButton, QMessageBox
from canvas import Canvas, ToolMode, ShapeMode,loadingScreen
from PyQt5 import QtWidgets, uic, QtCore  # pip install pyqt5
import sys
from qt_material import apply_stylesheet  # pip install qt_material


class Ui(QtWidgets.QMainWindow):
    """ load main window """

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('./UI//mainwindow.ui', self)  # load UI structure
        apply_stylesheet(app, theme='dark_blue.xml')  # apply dark blue theme
        self.canvas = None
        self.addition_to_ui()  # complete UI
        self.connect_btns_functions()  # set UI buttons functions
        self.show()

        # --- Begin adding some shortcuts --- #
        self.undo_shortcut = QShortcut(QKeySequence("Ctrl+Z"), self)
        self.undo_shortcut.activated.connect(self.undo_shortcut_activate)
        self.redo_shortcut = QShortcut(QKeySequence("Ctrl+shift+Z"), self)
        self.redo_shortcut.activated.connect(self.redo_shortcut_activate)
        self.save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        self.save_shortcut.activated.connect(self.save_shortcut_activate)
        # --- End adding some shortcuts --- #

    def addition_to_ui(self):
        """this function used for ui objects or edits that cant done on QT creator"""
        self.penSizeCombobox.setStyleSheet("font-size: 20px;")
        self.canvas = Canvas(1100, 600)  # initiate canvas
        self.canvasHorizontalLayout.addWidget(self.canvas)
        self.show_selected_btn_in_ui()
        self.change_selected_color_icon('#000000')

    def connect_btns_functions(self):
        """ connect Ui buttons to buttons functions"""
        self.newFileBtn.pressed.connect(self.new_file_btn_pressed)
        self.openFileBtn.pressed.connect(self.open_file_btn_pressed)
        self.saveFileBtn.pressed.connect(self.save_file_btn_pressed)
        self.undoBtn.pressed.connect(self.undo_btn_pressed)
        self.redoBtn.pressed.connect(self.redo_btn_pressed)

        self.penBtn.pressed.connect(self.pen_btn_pressed)
        self.eraserBtn.pressed.connect(self.eraser_btn_pressed)
        self.fillBtn.pressed.connect(self.fill_btn_pressed)

        self.penSizeCombobox.currentTextChanged.connect(self.pen_size_combobox_change)

        self.lineShapeBtn.pressed.connect(self.line_shape_btn_pressed)
        self.roundedSquareShapeBtn.pressed.connect(self.rounded_rect_shape_btn_pressed)
        self.squareShapeBtn.pressed.connect(self.rect_shape_btn_pressed)
        self.circleShapeBtn.pressed.connect(self.circle_shape_btn_pressed)

        self.color0Btn.pressed.connect(partial(self.color_btn_pressed))
        self.color1Btn.pressed.connect(partial(self.color_btn_pressed))
        self.color2Btn.pressed.connect(partial(self.color_btn_pressed))
        self.color3Btn.pressed.connect(partial(self.color_btn_pressed))
        self.color4Btn.pressed.connect(partial(self.color_btn_pressed))
        self.color5Btn.pressed.connect(partial(self.color_btn_pressed))
        self.color6Btn.pressed.connect(partial(self.color_btn_pressed))
        self.color7Btn.pressed.connect(partial(self.color_btn_pressed))
        self.color8Btn.pressed.connect(partial(self.color_btn_pressed))
        self.color9Btn.pressed.connect(partial(self.color_btn_pressed))

        self.colorPickerBtn.pressed.connect(self.color_picker_btn_pressed)

    def new_file_btn_pressed(self):
        """ jobs need to do when \"newFileBtn\" pressed

            (this function shows a popup windows to for confirmation and then will clear canvas)
        """
        msg = QMessageBox()
        msg.setWindowTitle("new paint")
        msg.setText("this action will delete all your unsaved files! \n are you sure to create new file?")
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.buttonClicked.connect(self.new_file_btn_popup)
        x = msg.exec_()

    def new_file_btn_popup(self, i):
        """ choose what \"newFileBtn\"s popup btns do!"""
        if i.text() == "&Yes":
            w = self.canvas.canvas_width
            h = self.canvas.canvas_height
            back_clr = self.canvas.background_color
            pen_color = self.canvas.pen_color.name()
            pensize = self.canvas.pen_width
            self.canvasHorizontalLayout.removeWidget(self.canvas)
            self.canvas = Canvas(w, h, back_clr=back_clr, pen_color=pen_color, pensize=pensize)
            self.canvasHorizontalLayout.addWidget(self.canvas)
            self.show_selected_btn_in_ui()
        else:
            pass

    def open_file_btn_pressed(self):
        """ jobs need to do when \"openFileBtn\" pressed

            (this function opens an image for painting)
        """
        self.canvas.open_image_as_pixmap()

    def save_file_btn_pressed(self):
        """ jobs need to do when \"saveFileBtn\" pressed

            (this function saves painting as image)
        """
        self.canvas.save_pixmap_as_image()

    def undo_btn_pressed(self):
        """ jobs need to do when \"undoBtn\" pressed

            (this function will undo what you done one step)
        """
        self.canvas.undo_action()

    def redo_btn_pressed(self):
        """ jobs need to do when \"redoBtn\" pressed

            (this function will redo what you done one step)
        """
        self.canvas.redo_action()

    def pen_btn_pressed(self):
        """ jobs need to do when \"penBtn\" pressed

            (this function sets paint mode to pen)
        """
        self.canvas.set_mode(ToolMode.pen.name)
        self.show_selected_btn_in_ui()

    def eraser_btn_pressed(self):
        """ jobs need to do when \"eraserBtn\" pressed

            (this function sets paint mode to eraser)
        """
        self.canvas.set_mode(ToolMode.eraser.name)
        self.show_selected_btn_in_ui()

    def fill_btn_pressed(self):
        """ jobs need to do when \"fillBtn\" pressed

            (this function sets paint mode to fill)
        """
        self.canvas.set_mode(ToolMode.fill.name)
        self.show_selected_btn_in_ui()
        self.update()

    def pen_size_combobox_change(self):
        """ jobs need to do when \"penSizeCombobox\" changes

            (this function sets line width for tools like : pen , eraser & etc)
        """
        penSize = int(self.penSizeCombobox.currentText())
        self.canvas.set_pen_size(penSize)
        self.update()


    def line_shape_btn_pressed(self):
        """ jobs need to do when \"lineShapeBtn\" pressed

            (this function sets paint mode to shape & sets shape mode to line)
        """
        self.canvas.set_mode(ToolMode.shape.name)
        self.canvas.set_shape_mode(ShapeMode.line.name)
        self.show_selected_btn_in_ui()

    def rounded_rect_shape_btn_pressed(self):
        """ jobs need to do when \"roundedSquareShapeBtn\" pressed

            (this function sets paint mode to shape & sets shape mode to rounded_rect)
        """
        self.canvas.set_mode(ToolMode.shape.name)
        self.canvas.set_shape_mode(ShapeMode.rounded_rect.name)
        self.show_selected_btn_in_ui()

    def rect_shape_btn_pressed(self):
        """ jobs need to do when \"squareShapeBtn\" pressed

            (this function sets paint mode to shape & sets shape mode to rect)
        """
        self.canvas.set_mode(ToolMode.shape.name)
        self.canvas.set_shape_mode(ShapeMode.rect.name)
        self.show_selected_btn_in_ui()

    def circle_shape_btn_pressed(self):
        """ jobs need to do when \"circleShapeBtn\" pressed

            (this function sets paint mode to shape & sets shape mode to circle)
        """
        self.canvas.set_mode(ToolMode.shape.name)
        self.canvas.set_shape_mode(ShapeMode.circle.name)
        self.show_selected_btn_in_ui()

    def show_selected_btn_in_ui(self):
        """ this functions disables the selected tool btn to find out witch one is selected"""
        for btn in self.toolBox.findChildren(QPushButton):
            btn.setEnabled(True)
        for btn in self.shapesBox.findChildren(QPushButton):
            btn.setEnabled(True)
        if self.canvas.mode == ToolMode.pen:
            self.penBtn.setEnabled(False)
        elif self.canvas.mode == ToolMode.eraser:
            self.eraserBtn.setEnabled(False)
        elif self.canvas.mode == ToolMode.fill:
            self.fillBtn.setEnabled(False)
        elif self.canvas.mode == ToolMode.shape:
            if self.canvas.shape_mode == ShapeMode.line:
                self.lineShapeBtn.setEnabled(False)
            elif self.canvas.shape_mode == ShapeMode.rect:
                self.squareShapeBtn.setEnabled(False)
            elif self.canvas.shape_mode == ShapeMode.rounded_rect:
                self.roundedSquareShapeBtn.setEnabled(False)
            elif self.canvas.shape_mode == ShapeMode.circle:
                self.circleShapeBtn.setEnabled(False)
            else:
                pass
        else:
            pass

    def change_selected_color_icon(self, color):
        """
            this functions changes the background of \"selectedColorIcon\" to show what color is selected
            :param color: (string)hex color (example: "#FFFFFF")
        """
        self.selectedColorIcon.setStyleSheet("background-color:" + color + "; border-radius : 20;")

    @QtCore.pyqtSlot()
    def color_btn_pressed(self):
        """
            set color of selected color_btn to selected color
        """
        color = self.sender().palette().button().color().name()
        self.change_selected_color_icon(color)
        self.canvas.set_pen_color(color)

    def color_picker_btn_pressed(self):
        """ jobs need to do when \"colorPickerBtn\" pressed

            open color picker and select what color you want
        """
        color = QColorDialog.getColor()
        self.change_selected_color_icon(color.name())
        self.canvas.set_pen_color(color.name())

    def undo_shortcut_activate(self):
        """ jobs need to do when \"Ctrl+Z\" pressed

            (this function will undo what you done one step)
        """
        self.undo_btn_pressed()

    def redo_shortcut_activate(self):
        """ jobs need to do when \"Ctrl+shift+Z\" pressed

            (this function will redo what you done one step)
        """
        self.redo_btn_pressed()

    def save_shortcut_activate(self):
        """ jobs need to do when \"Ctrl+S\" pressed

            (this function saves painting as image)
        """
        self.save_file_btn_pressed()


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
