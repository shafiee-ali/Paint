from canvas import Canvas
from PyQt5 import QtWidgets, uic  # pip install pyqt5
import sys

from qt_material import apply_stylesheet  # pip install qt_material

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('UI\\mainwindow.ui', self)
        apply_stylesheet(app, theme='dark_blue.xml')

        self.addtionToUi()
        self.ConnectBtnsFunctions()
        self.show()

    def addtionToUi(self):
        """this function used for ui objects or edits that cant done on QT creator"""
        self.penSizeCombobox.setStyleSheet("font-size: 20px;")
        self.canvas = Canvas(1100,600)
        self.canvasHorizontalLayout.addWidget(self.canvas)

    def ConnectBtnsFunctions(self):
        #### btn connections ####
        self.newFileBtn.pressed.connect(self.newFileBtnPressed)
        self.openFileBtn.pressed.connect(self.openFileBtnPressed)
        self.saveFileBtn.pressed.connect(self.saveFileBtnPressed)
        self.undoBtn.pressed.connect(self.undoBtnPressed)
        self.redoBtn.pressed.connect(self.redoBtnPressed)

        self.penBtn.pressed.connect(self.penBtnPressed)
        self.eraserBtn.pressed.connect(self.eraserBtnPressed)
        self.fillBtn.pressed.connect(self.fillBtnPressed)

        self.penSizeCombobox.currentTextChanged.connect(self.penSizeComboboxChange)

        self.lineShapeBtn.pressed.connect(self.lineShapeBtnPressed)
        self.roundedSquareShapeBtn.pressed.connect(self.roundedSquareShapeBtnPressed)
        self.squareShapeBtn.pressed.connect(self.squareShapeBtnPressed)
        self.circleShapeBtn.pressed.connect(self.circleShapeBtnPressed)


        self.color0Btn.pressed.connect(self.color0BtnPressed)
        self.color1Btn.pressed.connect(self.color1BtnPressed)
        self.color2Btn.pressed.connect(self.color2BtnPressed)
        self.color3Btn.pressed.connect(self.color3BtnPressed)
        self.color4Btn.pressed.connect(self.color4BtnPressed)
        self.color5Btn.pressed.connect(self.color5BtnPressed)
        self.color6Btn.pressed.connect(self.color6BtnPressed)
        self.color7Btn.pressed.connect(self.color7BtnPressed)
        self.color8Btn.pressed.connect(self.color8BtnPressed)
        self.color9Btn.pressed.connect(self.color9BtnPressed)

        self.colorPickerBtn.pressed.connect(self.colorPickerBtnPressed)
        #### end btn connections ####


    def newFileBtnPressed (self):
        print("newFileBtnPressed")
    def openFileBtnPressed (self):
        print("openFileBtnPressed")
    def saveFileBtnPressed (self):
        print("saveFileBtnPressed")
    def undoBtnPressed (self):
        print("undoBtnPressed")
    def redoBtnPressed (self):
        print("redoBtnPressed")

    def penBtnPressed(self):
        print("penBtnPressed")
    def eraserBtnPressed (self):
        print("eraserBtnPressed")
    def fillBtnPressed (self):
        print("fillBtnPressed")

    def penSizeComboboxChange(self):
        self.canvas.set_pen_size(int(self.penSizeCombobox.currentText()))
        print(self.penSizeCombobox.currentText())

    def lineShapeBtnPressed (self):
        print("lineShapeBtnPressed")
    def roundedSquareShapeBtnPressed (self):
        print("roundedSquareShapeBtnPressed")
    def squareShapeBtnPressed (self):
        print("squareShapeBtnPressed")
    def circleShapeBtnPressed (self):
        print("circleShapeBtnPressed")

    def changeSelectedColorIcon(self,color):
        self.selectedColorIcon.setStyleSheet("background-color:" + color + "; border-radius : 20;")
    def color0BtnPressed (self):
        color = self.color0Btn.palette().button().color().name()
        print(str(color))
        self.changeSelectedColorIcon(color)
        self.canvas.set_pen_color(color)

    def color1BtnPressed (self):
        color = self.color1Btn.palette().button().color().name()
        print(str(color))
        self.changeSelectedColorIcon(color)
        self.canvas.set_pen_color(color)

    def color2BtnPressed (self):
        color = self.color2Btn.palette().button().color().name()
        print(str(color))
        self.changeSelectedColorIcon(color)
        self.canvas.set_pen_color(color)


    def color3BtnPressed (self):
        color = self.color3Btn.palette().button().color().name()
        print(str(color))
        self.changeSelectedColorIcon(color)
        self.canvas.set_pen_color(color)


    def color4BtnPressed(self):
        color = self.color4Btn.palette().button().color().name()
        print(str(color))
        self.changeSelectedColorIcon(color)
        self.canvas.set_pen_color(color)


    def color5BtnPressed(self):
        color = self.color5Btn.palette().button().color().name()
        print(str(color))
        self.changeSelectedColorIcon(color)
        self.canvas.set_pen_color(color)


    def color6BtnPressed(self):
        color = self.color6Btn.palette().button().color().name()
        print(str(color))
        self.changeSelectedColorIcon(color)
        self.canvas.set_pen_color(color)


    def color7BtnPressed(self):
        color = self.color7Btn.palette().button().color().name()
        print(str(color))
        self.changeSelectedColorIcon(color)
        self.canvas.set_pen_color(color)


    def color8BtnPressed(self):
        color = self.color8Btn.palette().button().color().name()
        print(str(color))
        self.changeSelectedColorIcon(color)
        self.canvas.set_pen_color(color)


    def color9BtnPressed(self):
        color = self.color9Btn.palette().button().color().name()
        print(str(color))
        self.changeSelectedColorIcon(color)
        self.canvas.set_pen_color(color)


    def colorPickerBtnPressed(self):
        print("colorPickerBtnPressed")

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()