from PyQt5 import QtCore, QtGui, QtWidgets

class ScreenCapture(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Screen Capture')
        self.setGeometry(100, 100, 800, 600)
        self.setWindowOpacity(0.3)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.showFullScreen()

    def mousePressEvent(self, event):
        self.origin = event.pos()
        self.rubberBand = QtWidgets.QRubberBand(QtWidgets.QRubberBand.Rectangle, self)
        self.rubberBand.setGeometry(QtCore.QRect(self.origin, QtCore.QSize()))
        self.rubberBand.show()

    def mouseMoveEvent(self, event):
        self.rubberBand.setGeometry(QtCore.QRect(self.origin, event.pos()).normalized())

    def mouseReleaseEvent(self, event):
        self.rubberBand.hide()
        self.close()
        self.selected_rect = QtCore.QRect(self.origin, event.pos()).normalized()
        # Implement saving the selected area if needed

app = QtWidgets.QApplication([])
window = ScreenCapture()
app.exec_()
