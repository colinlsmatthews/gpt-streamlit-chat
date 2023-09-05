import sys
from PyQt5 import QtWidgets

app = QtWidgets.QApplication(sys.argv)
windows = QtWidgets.QWidget()

windows.resize(500, 500)
windows.move(100, 100)

windows.setWindowTitle("Hello PyQt5")

# set icon
windows.setWindowIcon(QtWidgets.QIcon("resources\icon.png"))
windows.show()
sys.exit(app.exec_())