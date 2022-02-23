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
        self.show()

    def addtionToUi(self):
        """this function used for ui objects or edits that cant done on QT creator"""
        self.penSizeCombobox.setStyleSheet("font-size: 20px;")
        self.canvas = Canvas(1100,600)
        self.canvasHorizontalLayout.addWidget(self.canvas)

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()