import sys
from PyQt6.QtWidgets import QApplication
from modules.homepageWindow import MainMenu
from modules.configWindow import ConfigWindow
import tkinter as tk
from tkinter import messagebox
import random
import string

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_menu = MainMenu()
    main_menu.show()
    sys.exit(app.exec())
