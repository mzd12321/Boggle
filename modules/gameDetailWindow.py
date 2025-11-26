import sys
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
                             QPushButton, QScrollArea, QFrame)
from PyQt5.QtCore import Qt

"""
GameDetailWindow displays detailed breakdown of a single game.
Shows completion percentage, timestamp, and words grouped by length.

Key Features:
- Words grouped by length (3-letter, 4-letter, etc., 7+ for long words)
- Color-coded: Green for found words, Red for missed words
- Green words displayed first, then red words
- Completion percentage shown for each word length category
- Back button returns to GameHistoryWindow
"""


class GameDetailWindow(QWidget):
    """Detailed view of a single game's results"""

    def __init__(self, game_data, history_window=None):
        super().__init__()
        self.game_data = game_data
        self.history_window = history_window
        self.initUI()

    def initUI(self):
        """Build the detail window UI"""
        self.setWindowTitle('Game Details')
        self.setGeometry(200, 100, 900, 700)
        self.setStyleSheet("background-color: #f0f0f0;")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 20, 30, 20)

        # Header section
        header_layout = QVBoxLayout()
        header_layout.setSpacing(10)

        # Completion percentage
        found = len(self.game_data.get('found_words', []))
        total = len(self.game_data.get('all_possible_words', []))
        completion = (found / total * 100) if total > 0 else 0

        completion_label = QLabel(f'Completion: <span style="color: #FF9800;">{completion:.1f}%</span>')
        completion_label.setStyleSheet("""
            font-size: 42px;
            font-weight: bold;
            color: #333;
        """)

        # Timestamp and game info
        timestamp_str = self.game_data.get('timestamp', '')
        formatted_time = self.format_timestamp(timestamp_str)

        grid_size = self.game_data.get('grid_size', 4)
        difficulty = self.game_data.get('difficulty', 'Unknown')
        timer = self.game_data.get('timer', 'Unknown')

        info_text = f"{formatted_time} • {grid_size}x{grid_size} Grid, {difficulty} mode, {timer}"
        info_label = QLabel(info_text)
        info_label.setStyleSheet("""
            font-size: 16px;
            color: #666;
        """)

        # Back button (top right)
        top_bar = QHBoxLayout()
        back_btn = QPushButton('← Back')
        back_btn.setFixedSize(120, 40)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #607D8B;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 10px;
                border: 2px solid #455A64;
            }
            QPushButton:hover {
                background-color: #455A64;
            }
        """)
        back_btn.clicked.connect(self.back_to_history)

        top_bar.addStretch()
        top_bar.addWidget(back_btn)

        header_layout.addLayout(top_bar)
        header_layout.addWidget(completion_label)
        header_layout.addWidget(info_label)

        # Separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: #ddd;")
        separator.setFixedHeight(2)

        # Scrollable area for word groups
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)

        # Container for word groups
        scroll_content = QWidget()
        words_layout = QVBoxLayout()
        words_layout.setSpacing(20)

        # Group words by length
        word_groups = self.group_words_by_length()

        # Display each word length group
        for length in sorted(word_groups.keys()):
            if length >= 7:
                continue  # Handle 7+ separately

            group_widget = self.create_word_group_widget(length, word_groups[length])
            words_layout.addWidget(group_widget)

        # Handle 7+ letter words
        if any(l >= 7 for l in word_groups.keys()):
            long_words = {'found': [], 'missed': []}
            for length in [l for l in word_groups.keys() if l >= 7]:
                long_words['found'].extend(word_groups[length]['found'])
                long_words['missed'].extend(word_groups[length]['missed'])

            if long_words['found'] or long_words['missed']:
                group_widget = self.create_word_group_widget('7+', long_words)
                words_layout.addWidget(group_widget)

        words_layout.addStretch()
        scroll_content.setLayout(words_layout)
        scroll.setWidget(scroll_content)

        # Assemble main layout
        main_layout.addLayout(header_layout)
        main_layout.addWidget(separator)
        main_layout.addWidget(scroll)

        self.setLayout(main_layout)

    def format_timestamp(self, timestamp_str):
        """Convert ISO timestamp to readable format: 'Monday 25th November 20:18'"""
        try:
            dt = datetime.fromisoformat(timestamp_str)
            day_name = dt.strftime('%A')
            day = dt.day
            month_name = dt.strftime('%B')
            time = dt.strftime('%H:%M')

            # Add ordinal suffix (st, nd, rd, th)
            if 10 <= day % 100 <= 20:
                suffix = 'th'
            else:
                suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')

            return f"{day_name} {day}{suffix} {month_name} {time}"
        except:
            return "Unknown date"

    def group_words_by_length(self):
        """Group all words by their length, separating found and missed"""
        found_words = set(word.upper() for word in self.game_data.get('found_words', []))
        all_words = set(word.upper() for word in self.game_data.get('all_possible_words', []))
        missed_words = all_words - found_words

        word_groups = {}

        # Process all possible words
        for word in all_words:
            length = len(word)
            if length not in word_groups:
                word_groups[length] = {'found': [], 'missed': []}

            if word in found_words:
                word_groups[length]['found'].append(word)
            else:
                word_groups[length]['missed'].append(word)

        # Sort words within each group alphabetically
        for length in word_groups:
            word_groups[length]['found'].sort()
            word_groups[length]['missed'].sort()

        return word_groups

    def create_word_group_widget(self, length, words_dict):
        """Create a widget for a specific word length group"""
        container = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)

        # Calculate completion percentage for this group
        found_count = len(words_dict['found'])
        total_count = found_count + len(words_dict['missed'])
        completion = (found_count / total_count * 100) if total_count > 0 else 0

        # Header with length and completion
        length_str = f"{length}" if isinstance(length, int) else length
        header = QLabel(f'{length_str} Letter Words <span style="color: #4CAF50;">{completion:.1f}%</span>')
        header.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #555;
        """)
        layout.addWidget(header)

        # Words container with wrapping
        words_container = QWidget()
        words_container.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
            }
        """)

        words_layout = QVBoxLayout()
        words_layout.setSpacing(5)

        # Create flow layout for words (custom wrapping)
        all_words = []

        # Add found words (green) first
        for word in words_dict['found']:
            word_label = QLabel(word.lower())
            word_label.setStyleSheet("""
                font-size: 16px;
                color: #4CAF50;
                font-weight: bold;
                padding: 5px 10px;
            """)
            all_words.append(word_label)

        # Add missed words (red) after
        for word in words_dict['missed']:
            word_label = QLabel(word.lower())
            word_label.setStyleSheet("""
                font-size: 16px;
                color: #f44336;
                padding: 5px 10px;
            """)
            all_words.append(word_label)

        # Arrange words in rows (flow layout simulation)
        row_layout = QHBoxLayout()
        row_layout.setSpacing(10)
        words_per_row = 8  # Approximate number of words per row

        for i, word_label in enumerate(all_words):
            row_layout.addWidget(word_label)

            # Start new row every words_per_row words
            if (i + 1) % words_per_row == 0 and i < len(all_words) - 1:
                row_layout.addStretch()
                words_layout.addLayout(row_layout)
                row_layout = QHBoxLayout()
                row_layout.setSpacing(10)

        # Add remaining words
        if row_layout.count() > 0:
            row_layout.addStretch()
            words_layout.addLayout(row_layout)

        words_container.setLayout(words_layout)
        layout.addWidget(words_container)

        container.setLayout(layout)
        return container

    def back_to_history(self):
        """Return to game history window"""
        if self.history_window:
            self.hide()
            self.history_window.show()
        else:
            self.close()