import sys
import json
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout,
                             QHBoxLayout, QPushButton, QScrollArea, QMessageBox)
from PyQt5.QtCore import Qt


class AnalyticsWindow(QWidget):
    def __init__(self, game_data, main_window=None):  # Remove config_window parameter
        super().__init__()
        self.game_data = game_data
        self.main_window = main_window

        # Fix missed words calculation
        self.missed_words = []
        for word in game_data['all_possible_words']:
            if word not in game_data['found_words']:
                self.missed_words.append(word)

        self.initUI()


    def initUI(self):
        self.setWindowTitle('Game Analytics')
        self.setGeometry(200, 100, 800, 600)
        self.setStyleSheet("background-color: #f5f5f5;")

        main_layout = QVBoxLayout()

        # Title
        title = QLabel('Post-Game Analytics')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: #333;
            padding: 20px;
        """)

        # Score summary
        score_text = f"Final Score: {self.game_data['score']}"
        score_label = QLabel(score_text)
        score_label.setAlignment(Qt.AlignCenter)
        score_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333; padding: 10px;")

        # Statistics
        stats_layout = QHBoxLayout()

        found_stat = QLabel(f"Words Found:\n{len(self.game_data['found_words'])}")
        found_stat.setAlignment(Qt.AlignCenter)
        found_stat.setStyleSheet("""
            background-color: white;
            padding: 15px;
            border-radius: 10px;
            font-size: 18px;
            font-weight: bold;
            color: #4CAF50;
        """)

        missed_stat = QLabel(f"Words Missed:\n{len(self.missed_words)}")
        missed_stat.setAlignment(Qt.AlignCenter)
        missed_stat.setStyleSheet("""
            background-color: white;
            padding: 15px;
            border-radius: 10px;
            font-size: 18px;
            font-weight: bold;
            color: #f44336;
        """)

        percentage = (len(self.game_data['found_words']) /
                      len(self.game_data['all_possible_words']) * 100
                      if self.game_data['all_possible_words'] else 0)

        percent_stat = QLabel(f"Completion:\n{percentage:.1f}%")
        percent_stat.setAlignment(Qt.AlignCenter)
        percent_stat.setStyleSheet("""
            background-color: white;
            padding: 15px;
            border-radius: 10px;
            font-size: 18px;
            font-weight: bold;
            color: #2196F3;
        """)

        stats_layout.addWidget(found_stat)
        stats_layout.addWidget(missed_stat)
        stats_layout.addWidget(percent_stat)

        # Missed words display
        missed_label = QLabel('Missed Words:')
        missed_label.setStyleSheet("""
            font-size: 18px; 
            font-weight: bold; 
            color: #333; 
            margin-top: 20px;
        """)

        # Scrollable area for missed words
        scroll_area = QScrollArea()
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout()

        missed_text = ', '.join(sorted(self.missed_words)) if self.missed_words else "None."
        missed_display = QLabel(missed_text)
        missed_display.setWordWrap(True)
        missed_display.setStyleSheet("""
            background-color: white;
            padding: 15px;
            border-radius: 10px;
            font-size: 14px;
        """)

        scroll_layout.addWidget(missed_display)
        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)
        scroll_area.setWidgetResizable(True)
        scroll_area.setMaximumHeight(200)

        # Buttons
        button_layout = QHBoxLayout()

        save_btn = QPushButton('Save This Game')
        save_btn.setFixedSize(200, 50)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 25px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        save_btn.clicked.connect(self.save_game)

        delete_btn = QPushButton('Delete This Game')
        delete_btn.setFixedSize(200, 50)
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 25px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        delete_btn.clicked.connect(self.delete_game)

        button_layout.addWidget(save_btn)
        button_layout.addWidget(delete_btn)

        # Assemble layout
        main_layout.addWidget(title)
        main_layout.addWidget(score_label)
        main_layout.addLayout(stats_layout)
        main_layout.addWidget(missed_label)
        main_layout.addWidget(scroll_area)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)
        main_layout.setContentsMargins(30, 30, 30, 30)

        self.setLayout(main_layout)


    def save_game(self):
        """Save game data to file"""
        try:
            # Add timestamp
            self.game_data['timestamp'] = datetime.now().isoformat()

            # Load existing games or create new list
            try:
                with open('data/game_history.json', 'r') as f:
                    games = json.load(f)
            except:
                games = []

            # Add this game
            games.append(self.game_data)

            # Save back to file
            with open('../data/game_history.json', 'w') as f:
                json.dump(games, f, indent=2)

            QMessageBox.information(self, "Success", "Game saved successfully!")
            self.return_to_menu()

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to save game: {str(e)}")


    def delete_game(self):
        """Delete game without saving"""
        reply = QMessageBox.question(self, "Confirm Delete",
                                     "Are you sure you want to delete this game without saving?",
                                     QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.return_to_menu()


    def return_to_menu(self):
        """Return to main menu"""
        if self.main_window:
            self.hide()
            self.main_window.show()
        else:
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game_data = {
        'score': 45,
        'found_words': ['THE', 'AND', 'CAT', 'DOG', 'RUN'],
        'all_possible_words': ['THE', 'AND', 'CAT', 'DOG', 'RUN', 'JUMP', 'PLAY', 'WORD', 'TEST', 'GAME'],
        'board': [['T', 'H', 'E', 'A'],
                  ['C', 'A', 'T', 'N'],
                  ['D', 'O', 'G', 'D'],
                  ['R', 'U', 'N', 'S']],
        'grid_size': 4,
        'time_played': 180  # 3 minutes in seconds
    }
    analywindow = AnalyticsWindow(game_data)
    analywindow.show()
    sys.exit(app.exec_())