import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QVBoxLayout,
                             QHBoxLayout)
from PyQt5.QtCore import Qt

class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Boggle')
        self.setGeometry(300, 300, 800, 600)

        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
            }
            QLabel#TitleLabel {
                font-size: 72px;
                font-weight: bold;
                color: #555;
            }
            QPushButton {
                font-size: 24px;
                color: white;
                padding: 15px 30px;
                border-radius: 20px;
                border: 2px solid #333;
            }
            QPushButton#PlayButton {
                background-color: #4CAF50;
            }
            QPushButton#PlayButton:hover {
                background-color: #45a049;
            }
            QPushButton#AnalyticsButton {
                background-color: #ff9800;
            }
            QPushButton#AnalyticsButton:hover {
                background-color: #fb8c00;
            }
            QPushButton#QuitButton {
                background-color: #f44336;
            }
            QPushButton#QuitButton:hover {
                background-color: #d32f2f;
            }
        """)

        v_layout = QVBoxLayout()
        h_layout = QHBoxLayout()

        title_label = QLabel('Boggle')
        title_label.setObjectName("TitleLabel")
        title_label.setAlignment(Qt.AlignCenter)  # Changed from Qt.AlignmentFlag.AlignCenter

        play_button = QPushButton('Play')
        play_button.setObjectName("PlayButton")
        play_button.clicked.connect(self.play_game)

        analytics_button = QPushButton('Analytics')
        analytics_button.setObjectName("AnalyticsButton")
        analytics_button.clicked.connect(self.show_analytics)

        quit_button = QPushButton('Quit')
        quit_button.setObjectName("QuitButton")
        quit_button.clicked.connect(self.quit_game)

        h_layout.addStretch(1)
        h_layout.addWidget(play_button)
        h_layout.addWidget(analytics_button)
        h_layout.addWidget(quit_button)
        h_layout.addStretch(1)

        v_layout.addStretch(1)
        v_layout.addWidget(title_label)
        v_layout.addStretch(1)
        v_layout.addLayout(h_layout)
        v_layout.addStretch(2)

        self.setLayout(v_layout)

    def play_game(self):
        from modules.configWindow import ConfigWindow
        self.hide()
        self.config_window = ConfigWindow()
        self.config_window.main_menu = self
        self.config_window.show()

    def show_analytics(self):
        print("Displaying game analytics!")

    def quit_game(self):
        QApplication.instance().quit()


# This is the standard entry point for a PyQt application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_menu = MainMenu()
    main_menu.show()
    sys.exit(app.exec())  # **Changed from app.exec_() to app.exec()**