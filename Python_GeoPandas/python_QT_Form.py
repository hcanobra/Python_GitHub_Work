from PyQt5 import QtWidgets, uic
import sys

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('/Users/canobhu/Documents/GitHub/QGIS/QGIS_Forms/Escalations.ui', self)
        self.show()
        
app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()