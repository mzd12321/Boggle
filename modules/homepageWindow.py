import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QVBoxLayout,
                             QGridLayout, QMessageBox, QComboBox, QSpinBox, QFormLayout,
                             QHBoxLayout)

from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # --- Window Properties ---
        self.setWindowTitle('Boggle')
        self.setGeometry(300, 300, 800, 600)  # x, y, width, height

        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0; /* Light gray background */
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
                border-radius: 20px; /* This creates the rounded corners */
                border: 2px solid #333;
            }
            QPushButton#PlayButton {
                background-color: #4CAF50; /* Green */
            }
            QPushButton#PlayButton:hover {
                background-color: #45a049; /* Darker Green */
            }
            QPushButton#AnalyticsButton {
                background-color: #ff9800; /* Orange */
            }
            QPushButton#AnalyticsButton:hover {
                background-color: #fb8c00; /* Darker Orange */
            }
            QPushButton#QuitButton {
                background-color: #f44336; /* Red */
            }
            QPushButton#QuitButton:hover {
                background-color: #d32f2f; /* Darker Red */
            }
        """)

        # --- Layouts ---
        # Main vertical layout
        v_layout = QVBoxLayout()
        # Horizontal layout for the buttons
        h_layout = QHBoxLayout()

        # --- Widgets ---
        # Title Label
        title_label = QLabel('Boggle')
        title_label.setObjectName("TitleLabel")  # Set object name for specific styling
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # **Changed from Qt.AlignCenter to Qt.AlignmentFlag.AlignCenter**

        # Play Button
        play_button = QPushButton('Play')
        play_button.setObjectName("PlayButton")
        play_button.clicked.connect(self.play_game)

        # Analytics Button
        analytics_button = QPushButton('Analytics')
        analytics_button.setObjectName("AnalyticsButton")
        analytics_button.clicked.connect(self.show_analytics)

        # Quit Button
        quit_button = QPushButton('Quit')
        quit_button.setObjectName("QuitButton")
        quit_button.clicked.connect(self.quit_game)

        # --- Assembling the Layout ---
        # Add buttons to the horizontal layout
        h_layout.addStretch(1)  # Add stretchable space to center the buttons
        h_layout.addWidget(play_button)
        h_layout.addWidget(analytics_button)
        h_layout.addWidget(quit_button)
        h_layout.addStretch(1)

        # Add title and button layout to the main vertical layout
        v_layout.addStretch(1)
        v_layout.addWidget(title_label)
        v_layout.addStretch(1)
        v_layout.addLayout(h_layout)  # Add the horizontal layout inside the vertical one
        v_layout.addStretch(2)

        # Set the main layout for the window
        self.setLayout(v_layout)

    def play_game(self):
        """Transition to configuration window"""
        from modules.configWindow import ConfigWindow  # Import here to avoid circular imports

        self.hide()  # Hide current window
        self.config_window = ConfigWindow()  # Create config window instance

        # If you want to return to main menu from config, pass reference
        self.config_window.main_menu = self
        self.config_window.show()

        print("Opening configuration window!")

    def show_analytics(self):
        """
        self.hide()
        self.game_window = analyticsWindow()
        self.game_window.show()
        """
        print("Displaying game analytics!")
        # Similarly, you would hide this and show the analytics window.

    def quit_game(self):
        """Quits the Software"""
        QApplication.instance().quit()


# This is the standard entry point for a PyQt application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_menu = MainMenu()
    main_menu.show()
    sys.exit(app.exec())  # **Changed from app.exec_() to app.exec()**