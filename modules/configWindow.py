import sys
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLabel, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt


class ConfigWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.main_menu = None

        # Current option indices
        self.gridsize_index = 0
        self.timer_index = 0
        self.difficulty_index = 0
        self.helper_index = 0

        # Options for each toggle
        self.gridsize_options = ["4x4", "5x5"]
        self.timer_options = ["Off", "3:00", "3:30", "4:00"]
        self.difficulty_options = ["Easy", "Medium", "Hard"]
        self.helper_options = ["Off", "On"]

        self.initUI()


    def initUI(self):
        self.setWindowTitle('Boggle - Configuration')
        self.setGeometry(300, 300, 800, 600)
        self.setStyleSheet("background-color: #f0f0f0;")

        main_layout = QVBoxLayout()

        # Title
        title = QLabel('Game Configuration')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 48px;
            font-weight: bold;
            color: #333;
            padding: 20px;
            margin-bottom: 30px;
        """)

        # Grid for config options
        grid_layout = QGridLayout()
        grid_layout.setSpacing(30)

        # Create each configuration option with label and button
        # Grid Size Label
        gridsize_label = QLabel('Grid Size')
        gridsize_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        gridsize_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #555;")
        self.gridsize_btn = self.create_toggle_button(self.gridsize_options[0])
        self.gridsize_btn.clicked.connect(self.toggle_gridsize)

        # Timer Label
        timer_label = QLabel('Timer')
        timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        timer_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #555;")
        self.timer_btn = self.create_toggle_button(self.timer_options[0])
        self.timer_btn.clicked.connect(self.toggle_timer)

        # Difficulty Label
        difficulty_label = QLabel('Difficulty')
        difficulty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        difficulty_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #555;")
        self.difficulty_btn = self.create_toggle_button(self.difficulty_options[0])
        self.difficulty_btn.clicked.connect(self.toggle_difficulty)

        # AI Helper Label
        helper_label = QLabel('AI Helper')
        helper_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        helper_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #555;")
        self.helper_btn = self.create_toggle_button(self.helper_options[0])
        self.helper_btn.clicked.connect(self.toggle_helper)

        # Add to grid (label above, button below)
        grid_layout.addWidget(gridsize_label, 0, 0)
        grid_layout.addWidget(self.gridsize_btn, 1, 0)

        grid_layout.addWidget(timer_label, 0, 1)
        grid_layout.addWidget(self.timer_btn, 1, 1)

        grid_layout.addWidget(difficulty_label, 2, 0)
        grid_layout.addWidget(self.difficulty_btn, 3, 0)

        grid_layout.addWidget(helper_label, 2, 1)
        grid_layout.addWidget(self.helper_btn, 3, 1)

        # Start Game button
        start_btn = QPushButton('Start Game')
        start_btn.setFixedSize(200, 50)
        start_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 20px;
                font-weight: bold;
                border-radius: 25px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #388E3C;
            }
        """)
        start_btn.clicked.connect(self.start_game)

        # Back button
        back_btn = QPushButton('Back to Menu')
        back_btn.setFixedSize(200, 40)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #607D8B;
                color: white;
                font-size: 16px;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: #455A64;
            }
        """)
        back_btn.clicked.connect(self.back_to_menu)

        # Button container
        button_container = QVBoxLayout()
        button_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_container.addWidget(start_btn)
        button_container.addSpacing(10)
        button_container.addWidget(back_btn)

        # Assemble layout
        main_layout.addWidget(title)
        main_layout.addLayout(grid_layout)
        main_layout.addStretch()
        main_layout.setContentsMargins(50, 30, 50, 30)
        main_layout.addLayout(button_container)

        self.setLayout(main_layout)


    def create_toggle_button(self, text):
        button = QPushButton(text)
        button.setFixedSize(150, 80)
        button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-size: 24px;
                font-weight: bold;
                border-radius: 15px;
                border: 3px solid #1976D2;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)
        return button


    def toggle_gridsize(self):
        """Cycle through grid size options"""
        self.gridsize_index = (self.gridsize_index + 1) % len(self.gridsize_options)
        self.gridsize_btn.setText(self.gridsize_options[self.gridsize_index])
        print(f"Grid size changed to: {self.gridsize_options[self.gridsize_index]}")


    def toggle_timer(self):
        """Cycle through timer options"""
        self.timer_index = (self.timer_index + 1) % len(self.timer_options)
        self.timer_btn.setText(self.timer_options[self.timer_index])
        print(f"Timer changed to: {self.timer_options[self.timer_index]}")


    def toggle_difficulty(self):
        """Cycle through difficulty options"""
        self.difficulty_index = (self.difficulty_index + 1) % len(self.difficulty_options)
        self.difficulty_btn.setText(self.difficulty_options[self.difficulty_index])

        self.difficulty_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #2196F3;
                color: white;
                font-size: 24px;
                font-weight: bold;
                border-radius: 15px;
                border: 3px solid #1976D2;
            }}
            QPushButton:hover {{
                background-color: #1976D2;
            }}
        """)
        print(f"Difficulty changed to: {self.difficulty_options[self.difficulty_index]}")


    def toggle_helper(self):
        """Toggle AI helper on/off"""
        self.helper_index = (self.helper_index + 1) % len(self.helper_options)
        self.helper_btn.setText(self.helper_options[self.helper_index])
        print(f"AI Helper: {self.helper_options[self.helper_index]}")


    def start_game(self):
        """Get current configuration and start game"""
        config = {
            'grid_size': self.gridsize_options[self.gridsize_index],
            'timer': self.timer_options[self.timer_index],
            'difficulty': self.difficulty_options[self.difficulty_index],
            'ai_helper': self.helper_options[self.helper_index]
        }

        from modules.boggleGame import BoggleGame

        self.hide()
        # Pass main_menu reference to BoggleGame
        self.game_window = BoggleGame(config, self.main_menu)  # Pass main_menu
        self.game_window.config_window = self
        self.game_window.show()


    def back_to_menu(self):
        if self.main_menu:
            self.hide()
            self.main_menu.show()
        else:
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ConfigWindow()
    window.show()
    sys.exit(app.exec())