import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from homepageWindow import MainMenu
from configWindow import ConfigWindow
import tkinter as tk
from tkinter import messagebox
import random
import string

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_menu = MainMenu()
    main_menu.show()
    sys.exit(app.exec_())
