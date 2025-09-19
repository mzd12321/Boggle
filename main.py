import sys
from PyQt5.QtWidgets import QApplication
from modules.homepageWindow import MainMenu


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_menu = MainMenu()
    main_menu.show()
    sys.exit(app.exec_())  # Changed back to exec_()