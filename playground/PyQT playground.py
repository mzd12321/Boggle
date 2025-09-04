import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Boggle")
window.setGeometry(300, 300, 400, 400)
window.show()
sys.exit(app.exec_())

