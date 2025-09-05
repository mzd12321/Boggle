import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QPushButton,
                             QLabel, QVBoxLayout, QHBoxLayout, QMessageBox, QDialog)
from PyQt5.QtCore import Qt, QTimer
from boardGen import BoardGenerator
from validation import WordValidator
from wordFinder import WordFinder


class TileButton(QPushButton):
    """Custom button for Boggle tiles"""

    def __init__(self, letter, row, col):
        super().__init__(letter)
        self.row = row
        self.col = col
        self.is_selected = False
        self.setFixedSize(80, 80)
        self.update_style()

    def update_style(self):
        if self.is_selected:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    font-size: 36px;
                    font-weight: bold;
                    border: 3px solid #2E7D32;
                    border-radius: 10px;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    color: #333;
                    font-size: 36px;
                    font-weight: bold;
                    border: 2px solid #666;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: #E8F5E9;
                    border: 3px solid #4CAF50;
                }
            """)

    def set_selected(self, selected):
        self.is_selected = selected
        self.update_style()


class EndGameDialog(QDialog):
    """Dialog to confirm ending the game"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("End Game?")
        self.setModal(True)
        self.setFixedSize(400, 200)

        layout = QVBoxLayout()

        # Question label
        question = QLabel("End the current game?")
        question.setAlignment(Qt.AlignCenter)
        question.setStyleSheet("font-size: 16px; color: #666; padding: 20px;")

        # Buttons
        button_layout = QHBoxLayout()

        yes_btn = QPushButton("Yes, End and Exit")
        yes_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        yes_btn.clicked.connect(self.accept)

        no_btn = QPushButton("No, Return")
        no_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        no_btn.clicked.connect(self.reject)

        button_layout.addWidget(yes_btn)
        button_layout.addWidget(no_btn)

        layout.addWidget(question)
        layout.addLayout(button_layout)
        self.setLayout(layout)



class BoggleGame(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.config_window = None

        # Parse config
        self.grid_size = int(config['grid_size'][0])
        self.timer_seconds = self.parse_timer(config['timer'])
        self.difficulty = config['difficulty']
        self.ai_helper_enabled = config['ai_helper'] == 'On'

        # Game state
        self.board_letters = []
        self.tiles = []
        self.selected_path = []
        self.current_word = ""
        self.found_words = []
        self.all_possible_words = []
        self.score = 0
        self.is_dragging = False
        self.ai_helper_uses = 0

        # Initialize components
        self.board_gen = BoardGenerator(self.grid_size, self.difficulty)
        self.validator = WordValidator()
        self.word_finder = WordFinder()

        self.initUI()
        self.generate_board()

        if self.timer_seconds > 0:
            self.start_timer()


    def parse_timer(self, timer_str):

        #Convert timer string to seconds
        if timer_str == "Off":
            return 0
        minutes, seconds = timer_str.split(':')
        return int(minutes) * 60 + int(seconds)


    def initUI(self):
        self.setWindowTitle('Boggle Game')
        self.setGeometry(200, 100, 900, 700)
        self.setStyleSheet("background-color: #f5f5f5;")

        main_layout = QVBoxLayout()

        # Top bar with timer and end game button
        top_bar = QHBoxLayout()

        # Timer on the left
        self.timer_label = QLabel('Time: --:--')
        self.timer_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #333;
            padding: 10px;
            background-color: white;
            border-radius: 10px;
        """)

        # End Game button on the right
        end_game_btn = QPushButton('End Game')
        end_game_btn.setFixedSize(120, 40)
        end_game_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        end_game_btn.clicked.connect(self.confirm_end_game)

        top_bar.addWidget(self.timer_label)
        top_bar.addStretch()
        top_bar.addWidget(end_game_btn)

        # Score display
        self.score_label = QLabel('Score: 0')
        self.score_label.setAlignment(Qt.AlignCenter)
        self.score_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #333;
            padding: 10px;
        """)

        # Current word display
        self.word_display = QLabel('')
        self.word_display.setAlignment(Qt.AlignCenter)
        self.word_display.setStyleSheet("""
            font-size: 36px;
            font-weight: bold;
            color: #4CAF50;
            padding: 15px;
            background-color: white;
            border: 3px solid #4CAF50;
            border-radius: 10px;
            min-height: 60px;
        """)

        # Game board
        board_container = QWidget()
        self.board_layout = QGridLayout()
        self.board_layout.setSpacing(5)
        board_container.setLayout(self.board_layout)
        board_container.setMaximumSize(500, 500)



        # Found words display
        self.words_label = QLabel('Found Words:')
        self.words_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")

        self.words_display = QLabel('')
        self.words_display.setStyleSheet("""
            background-color: white;
            border: 2px solid #ddd;
            border-radius: 10px;
            padding: 10px;
            font-size: 14px;
        """)
        self.words_display.setWordWrap(True)
        self.words_display.setMaximumHeight(100)

        # Assemble layout
        main_layout.addLayout(top_bar)
        main_layout.addWidget(self.score_label)
        main_layout.addWidget(self.word_display)
        main_layout.addWidget(board_container, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.words_label)
        main_layout.addWidget(self.words_display)
        main_layout.addStretch()

        self.setLayout(main_layout)
        self.setMouseTracking(True)


    def generate_board(self):
        """Generate a new game board"""
        self.board_letters = self.board_gen.generate()

        # Find all possible words for analytics
        self.all_possible_words = self.word_finder.find_all_words(self.board_letters)

        # Clear existing tiles
        for i in reversed(range(self.board_layout.count())):
            self.board_layout.itemAt(i).widget().setParent(None)

        self.tiles = []

        # Create tile buttons
        for row in range(self.grid_size):
            tile_row = []
            for col in range(self.grid_size):
                letter = self.board_letters[row][col]
                tile = TileButton(letter, row, col)
                tile.pressed.connect(lambda r=row, c=col: self.start_selection(r, c))
                self.board_layout.addWidget(tile, row, col)
                tile_row.append(tile)
            self.tiles.append(tile_row)


    def confirm_end_game(self):
        """Show confirmation dialog for ending game"""
        if hasattr(self, 'timer'):
            self.timer.stop()  # Pause timer

        dialog = EndGameDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.end_game()
        else:
            # Resume timer if it was running
            if hasattr(self, 'timer') and self.timer_seconds > 0:
                self.timer.start()


    def submit_word(self):
        """Submit current word"""
        if len(self.current_word) < 3:
            self.clear_selection()
            return

        if self.current_word.upper() in self.found_words:
            QMessageBox.warning(self, "Already Found", f"You already found '{self.current_word}'")
            self.clear_selection()
            return

        if self.validator.is_valid_word(self.current_word):
            self.found_words.append(self.current_word.upper())
            points = max(1, len(self.current_word) - 2)
            self.score += points
            self.score_label.setText(f'Score: {self.score}')

            # Update display
            self.words_display.setText(', '.join(self.found_words))
        else:
            QMessageBox.warning(self, "Invalid Word", f"'{self.current_word}' is not valid")

        self.clear_selection()


    def start_selection(self, row, col):
        """Start selecting a word"""
        self.clear_selection()
        self.is_dragging = True
        self.add_to_selection(row, col)


    def add_to_selection(self, row, col):
        """Add a tile to selection"""
        if (row, col) in self.selected_path:
            return

        if self.selected_path and not self.is_adjacent(row, col):
            return

        self.selected_path.append((row, col))
        self.tiles[row][col].set_selected(True)
        self.current_word += self.board_letters[row][col]
        self.word_display.setText(self.current_word)


    def is_adjacent(self, row, col):
        """Check if tile is adjacent to last selected"""
        if not self.selected_path:
            return True
        last_row, last_col = self.selected_path[-1]
        return abs(row - last_row) <= 1 and abs(col - last_col) <= 1


    def mouseMoveEvent(self, event):
        """Handle mouse drag"""
        if not self.is_dragging:
            return

        pos = event.pos()
        widget = self.childAt(pos)

        if isinstance(widget, TileButton):
            self.add_to_selection(widget.row, widget.col)


    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        if self.is_dragging:
            self.is_dragging = False
            self.submit_word()


    def clear_selection(self):
        """Clear current selection"""
        for row, col in self.selected_path:
            self.tiles[row][col].set_selected(False)
        self.selected_path = []
        self.current_word = ""
        self.word_display.setText("")

    def start_timer(self):
        """Start game timer"""
        self.time_left = self.timer_seconds
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)
        self.update_timer()


    def update_timer(self):
        """Update timer display"""
        if self.time_left <= 0:
            self.timer.stop()
            self.end_game()
            return

        minutes = self.time_left // 60
        seconds = self.time_left % 60
        self.timer_label.setText(f'Time: {minutes:02d}:{seconds:02d}')
        self.time_left -= 1


    def end_game(self):
        """End game and show analytics"""
        if hasattr(self, 'timer'):
            self.timer.stop()

        # Prepare game data
        game_data = {
            'score': self.score,
            'found_words': self.found_words,
            'all_possible_words': self.all_possible_words,
            'board': self.board_letters,
            'grid_size': self.grid_size,
            'time_played': self.timer_seconds - (self.time_left if hasattr(self, 'time_left') else 0)
        }

        # Open analytics window
        from analyticsWindow import AnalyticsWindow
        self.hide()
        self.analytics = AnalyticsWindow(game_data, self.config_window)
        self.analytics.show()


if __name__ == '__main__':
    # Create a test configuration
    test_config = {
        'grid_size': '4x4',
        'timer': '3:00',
        'difficulty': 'Easy',
        'ai_helper': 'Off'
    }

    app = QApplication(sys.argv)
    game = BoggleGame(test_config)  # Note: BoggleGame with capital B, not boggleGame
    game.show()
    sys.exit(app.exec_())