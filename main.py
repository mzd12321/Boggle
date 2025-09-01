import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from homepageWindow import MainMenu
from configWindow import ConfigWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_menu = MainMenu()
    main_menu.show()
    sys.exit(app.exec_())