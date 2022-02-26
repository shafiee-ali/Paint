from canvas import Canvas
from PyQt5 import QtWidgets, uic  # pip install pyqt5
import sys

from qt_material import apply_stylesheet  # pip install qt_material


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('UI\\mainwindow.ui', self)
        apply_stylesheet(app, theme='dark_blue.xml')
        self.addition_to_ui()
        self.ConnectBtnsFunctions()
        self.show()

    def addition_to_ui(self):
        """this function used for ui objects or edits that cant done on QT creator"""
        self.penSizeCombobox.setStyleSheet("font-size: 20px;")
        self.canvas = Canvas(1100, 600)
        self.canvasHorizontalLayout.addWidget(self.canvas)

    def ConnectBtnsFunctions(self):
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
        print("newFileBtnPressed")

    def open_file_btn_pressed(self):
        print("openFileBtnPressed")

    def save_file_btn_pressed (self):
        print("saveFileBtnPressed")

    def undo_btn_pressed(self):
        print("undoBtnPressed")

    def redo_btn_pressed(self):
        print("redoBtnPressed")

    def pen_btn_pressed(self):
        self.canvas.set_mode("pen")
        print("penBtnPressed")

    def eraser_btn_pressed(self):
        self.canvas.set_mode("eraser")
        print("eraserBtnPressed")

    def fill_btn_pressed(self):
        self.canvas.set_mode("fill")
        print("fillBtnPressed")

    def pen_size_combobox_change(self):
        self.canvas.set_pen_size(int(self.penSizeCombobox.currentText()))
        print(self.penSizeCombobox.currentText())

    def line_shape_btn_pressed(self):
        self.canvas.set_mode("shape")
        self.canvas.set_shape_mode("line")
        print("lineShapeBtnPressed")

    def rounded_rect_shape_btn_pressed(self):
        self.canvas.set_mode("shape")
        self.canvas.set_shape_mode("rounded rect")
        print("roundedSquareShapeBtnPressed")

    def rect_shape_btn_pressed(self):
        self.canvas.set_mode("shape")
        self.canvas.set_shape_mode("rect")
        print("squareShapeBtnPressed")

    def circle_shape_btn_pressed(self):
        self.canvas.set_mode("shape")
        self.canvas.set_shape_mode("circle")
        print("circleShapeBtnPressed")

    def change_selected_color_icon(self, color):
        self.selectedColorIcon.setStyleSheet("background-color:" + color + "; border-radius : 20;")

    def color0_btn_pressed(self):
        color = self.color0Btn.palette().button().color().name()
        print(str(color))
        self.change_selected_color_icon(color)
        self.canvas.set_pen_color(color)

    def color1_btn_pressed(self):
        color = self.color1Btn.palette().button().color().name()
        print(str(color))
        self.change_selected_color_icon(color)
        self.canvas.set_pen_color(color)

    def color2_btn_pressed(self):
        color = self.color2Btn.palette().button().color().name()
        print(str(color))
        self.change_selected_color_icon(color)
        self.canvas.set_pen_color(color)


    def color3_btn_pressed(self):
        color = self.color3Btn.palette().button().color().name()
        print(str(color))
        self.change_selected_color_icon(color)
        self.canvas.set_pen_color(color)


    def color4_btn_pressed(self):
        color = self.color4Btn.palette().button().color().name()
        print(str(color))
        self.change_selected_color_icon(color)
        self.canvas.set_pen_color(color)


    def color5_btn_pressed(self):
        color = self.color5Btn.palette().button().color().name()
        print(str(color))
        self.change_selected_color_icon(color)
        self.canvas.set_pen_color(color)


    def color6_btn_pressed(self):
        color = self.color6Btn.palette().button().color().name()
        print(str(color))
        self.change_selected_color_icon(color)
        self.canvas.set_pen_color(color)


    def color7_btn_pressed(self):
        color = self.color7Btn.palette().button().color().name()
        print(str(color))
        self.change_selected_color_icon(color)
        self.canvas.set_pen_color(color)


    def color8_btn_pressed(self):
        color = self.color8Btn.palette().button().color().name()
        print(str(color))
        self.change_selected_color_icon(color)
        self.canvas.set_pen_color(color)


    def color9_btn_pressed(self):
        color = self.color9Btn.palette().button().color().name()
        print(str(color))
        self.change_selected_color_icon(color)
        self.canvas.set_pen_color(color)


    def color_picker_btn_pressed(self):
        print("colorPickerBtnPressed")


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()