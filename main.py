import PyQt5
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut, QAction, QColorDialog, QGroupBox, QPushButton

from canvas import Canvas,ToolMode ,ShapeMode
from PyQt5 import QtWidgets, uic, QtGui, QtCore, Qt  # pip install pyqt5
import sys
from qt_material import apply_stylesheet  # pip install qt_material

from PyQt5.QtWidgets import QMessageBox


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('./UI//mainwindow.ui', self)
        apply_stylesheet(app, theme='dark_blue.xml')
        self.addition_to_ui()
        self.connect_btns_functions()
        self.show()
        self.undo_shortcut = QShortcut(QKeySequence("Ctrl+Z"), self)
        self.undo_shortcut.activated.connect(self.undo_shortcut_activate)
        self.redo_shortcut = QShortcut(QKeySequence("Ctrl+Y"), self)
        self.redo_shortcut.activated.connect(self.redo_shortcut_activate)
        self.save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        self.save_shortcut.activated.connect(self.save_shortcut_activate)

    def addition_to_ui(self):
        """this function used for ui objects or edits that cant done on QT creator"""
        self.penSizeCombobox.setStyleSheet("font-size: 20px;")
        self.canvas = Canvas(1100, 600)
        self.canvasHorizontalLayout.addWidget(self.canvas)
        self.show_selected_btn_in_ui()
        self.change_selected_color_icon('#000000')
    def connect_btns_functions(self):
        #### btn connections ####
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

        self.color0Btn.pressed.connect(self.color0_btn_pressed)
        self.color1Btn.pressed.connect(self.color1_btn_pressed)
        self.color2Btn.pressed.connect(self.color2_btn_pressed)
        self.color3Btn.pressed.connect(self.color3_btn_pressed)
        self.color4Btn.pressed.connect(self.color4_btn_pressed)
        self.color5Btn.pressed.connect(self.color5_btn_pressed)
        self.color6Btn.pressed.connect(self.color6_btn_pressed)
        self.color7Btn.pressed.connect(self.color7_btn_pressed)
        self.color8Btn.pressed.connect(self.color8_btn_pressed)
        self.color9Btn.pressed.connect(self.color9_btn_pressed)

        self.colorPickerBtn.pressed.connect(self.color_picker_btn_pressed)
        #### end btn connections ####



    def new_file_btn_pressed(self):
        msg = QMessageBox()
        msg.setWindowTitle("new paint")
        msg.setText("this action will delete all your unsaved files! \n are you sure to create new file?")
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.buttonClicked.connect(self.new_file_btn_popup)
        x = msg.exec_()


    def new_file_btn_popup(self, i):
        if i.text() == "&Yes":
            self.canvas.new_pixmap()
        else :
            pass

    def open_file_btn_pressed(self):
        self.canvas.open_image_as_pixmap()
    def save_file_btn_pressed (self):
        self.canvas.save_pixmap_as_image()

    def undo_btn_pressed(self):
        self.canvas.undo_action()

    def redo_btn_pressed(self):
        self.canvas.redo_action()

    def pen_btn_pressed(self):
        self.canvas.set_mode(ToolMode.pen.name)
        self.show_selected_btn_in_ui()


    def eraser_btn_pressed(self):
        self.canvas.set_mode(ToolMode.eraser.name)
        self.show_selected_btn_in_ui()

    def fill_btn_pressed(self):
        self.canvas.set_mode(ToolMode.fill.name)
        self.show_selected_btn_in_ui()

    def fill_btn_popup(self, i):
        if i.text() == "&Yes":
            self.canvas.new_pixmap()
        else :
            pass

    def pen_size_combobox_change(self):
        self.canvas.set_pen_size(int(self.penSizeCombobox.currentText()))

    def line_shape_btn_pressed(self):
        self.canvas.set_mode(ToolMode.shape.name)
        self.canvas.set_shape_mode(ShapeMode.line.name)
        self.show_selected_btn_in_ui()

    def rounded_rect_shape_btn_pressed(self):
        self.canvas.set_mode(ToolMode.shape.name)
        self.canvas.set_shape_mode(ShapeMode.rounded_rect.name)
        self.show_selected_btn_in_ui()

    def rect_shape_btn_pressed(self):
        self.canvas.set_mode(ToolMode.shape.name)
        self.canvas.set_shape_mode(ShapeMode.rect.name)
        self.show_selected_btn_in_ui()

    def circle_shape_btn_pressed(self):
        self.canvas.set_mode(ToolMode.shape.name)
        self.canvas.set_shape_mode(ShapeMode.circle.name)
        self.show_selected_btn_in_ui()

    def show_selected_btn_in_ui(self):
        for btn in self.toolBox.findChildren(QPushButton):
            btn.setEnabled(True)
        for btn in  self.shapesBox.findChildren(QPushButton):
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
        self.selectedColorIcon.setStyleSheet("background-color:" + color + "; border-radius : 20;")

    def color0_btn_pressed(self):
        color = self.color0Btn.palette().button().color().name()
        self.change_selected_color_icon(color)
        self.canvas.set_pen_color(color)

    def color1_btn_pressed(self):
        color = self.color1Btn.palette().button().color().name()
        self.change_selected_color_icon(color)
        self.canvas.set_pen_color(color)

    def color2_btn_pressed(self):
        color = self.color2Btn.palette().button().color().name()
        self.change_selected_color_icon(color)
        self.canvas.set_pen_color(color)


    def color3_btn_pressed(self):
        color = self.color3Btn.palette().button().color().name()
        self.change_selected_color_icon(color)
        self.canvas.set_pen_color(color)


    def color4_btn_pressed(self):
        color = self.color4Btn.palette().button().color().name()
        self.change_selected_color_icon(color)
        self.canvas.set_pen_color(color)


    def color5_btn_pressed(self):
        color = self.color5Btn.palette().button().color().name()
        self.change_selected_color_icon(color)
        self.canvas.set_pen_color(color)


    def color6_btn_pressed(self):
        color = self.color6Btn.palette().button().color().name()
        self.change_selected_color_icon(color)
        self.canvas.set_pen_color(color)


    def color7_btn_pressed(self):
        color = self.color7Btn.palette().button().color().name()
        self.change_selected_color_icon(color)
        self.canvas.set_pen_color(color)


    def color8_btn_pressed(self):
        color = self.color8Btn.palette().button().color().name()
        self.change_selected_color_icon(color)
        self.canvas.set_pen_color(color)

    def color9_btn_pressed(self):
        color = self.color9Btn.palette().button().color().name()
        self.change_selected_color_icon(color)
        self.canvas.set_pen_color(color)

    def color_picker_btn_pressed(self):
        color = QColorDialog.getColor()
        self.change_selected_color_icon(color.name())
        self.canvas.set_pen_color(color.name())

    def undo_shortcut_activate(self):
        self.undo_btn_pressed()


    def redo_shortcut_activate(self):
        self.redo_btn_pressed()

    def save_shortcut_activate(self):
        self.save_file_btn_pressed()


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
