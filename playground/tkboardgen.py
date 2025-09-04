import tkinter as tk
from tkinter import messagebox
import random
import string

class GameBoard:
    def setup_ui(self):
        """Create the main UI layout"""
        # Title Label
        title_frame = tk.Frame(self.root, bg='#2b2b2b')
        title_frame.pack(pady=20)

        title_label = tk.Label(
            title_frame,
            text="BOGGLE",
            font=('Arial', 32, 'bold'),
            fg='#ffffff',
            bg='#2b2b2b'
        )
        title_label.pack()

        # Score and Timer Frame
        info_frame = tk.Frame(self.root, bg='#2b2b2b')
        info_frame.pack(pady=10)

        self.score_label = tk.Label(
            info_frame,
            text=f"Score: {self.score}",
            font=('Arial', 16),
            fg='#ffffff',
            bg='#2b2b2b'
        )
        self.score_label.pack(side=tk.LEFT, padx=20)

        self.timer_label = tk.Label(
            info_frame,
            text="Time: 3:00",
            font=('Arial', 16),
            fg='#ffffff',
            bg='#2b2b2b'
        )
        self.timer_label.pack(side=tk.LEFT, padx=20)

        # Current Word Display
        self.word_display = tk.Label(
            self.root,
            text="",
            font=('Arial', 20, 'bold'),
            fg='#4CAF50',
            bg='#2b2b2b',
            height=2
        )
        self.word_display.pack(pady=10)

        # Game Board Frame
        self.board_frame = tk.Frame(self.root, bg='#1e1e1e')
        self.board_frame.pack(pady=20)

        # Control Buttons Frame
        control_frame = tk.Frame(self.root, bg='#2b2b2b')
        control_frame.pack(pady=10)

        self.submit_btn = tk.Button(
            control_frame,
            text="Submit Word",
            font=('Arial', 12),
            bg='#4CAF50',
            fg='white',
            width=12,
            command=self.submit_word
        )
        self.submit_btn.pack(side=tk.LEFT, padx=5)

        self.clear_btn = tk.Button(
            control_frame,
            text="Clear",
            font=('Arial', 12),
            bg='#f44336',
            fg='white',
            width=12,
            command=self.clear_selection
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)

        self.new_game_btn = tk.Button(
            control_frame,
            text="New Game",
            font=('Arial', 12),
            bg='#2196F3',
            fg='white',
            width=12,
            command=self.new_game
        )
        self.new_game_btn.pack(side=tk.LEFT, padx=5)

        # Found Words Display
        words_frame = tk.Frame(self.root, bg='#2b2b2b')
        words_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        tk.Label(
            words_frame,
            text="Found Words:",
            font=('Arial', 12),
            fg='#ffffff',
            bg='#2b2b2b'
        ).pack()

        self.words_listbox = tk.Listbox(
            words_frame,
            font=('Arial', 10),
            bg='#1e1e1e',
            fg='#ffffff',
            height=6,
            width=50
        )
        self.words_listbox.pack(pady=5)


    def create_game_board(self):
        """Create the 4x4 grid of letter tiles"""
        # Store button references in a 2D list
        self.tiles = []
        self.tile_letters = []

        # Generate random letters for now (we'll improve this later)
        for row in range(self.grid_size):
            tile_row = []
            letter_row = []
            for col in range(self.grid_size):
                # Create button
                letter = random.choice(string.ascii_uppercase)

                btn = tk.Button(
                    self.board_frame,
                    text=letter,
                    font=('Arial', 24, 'bold'),
                    width=4,
                    height=2,
                    bg='#ffffff',
                    fg='#000000',
                    relief=tk.RAISED,
                    bd=3
                )
                btn.grid(row=row, column=col, padx=3, pady=3)

                # Bind click event
                btn.config(command=lambda r=row, c=col: self.tile_clicked(r, c))

                # Bind hover events for visual feedback
                btn.bind("<Enter>", lambda e, r=row, c=col: self.on_hover(e, r, c))
                btn.bind("<Leave>", lambda e, r=row, c=col: self.on_leave(e, r, c))

                tile_row.append(btn)
                letter_row.append(letter)

            self.tiles.append(tile_row)
            self.tile_letters.append(letter_row)


    def tile_clicked(self, row, col):
        """Handle tile click event"""
        # Check if this tile is already selected
        if (row, col) in self.selected_tiles:
            print(f"Tile ({row}, {col}) already selected!")
            return

        # Check if this is the first tile or if it's adjacent to the last selected tile
        if len(self.selected_tiles) == 0 or self.is_adjacent(row, col):
            # Add to selected tiles
            self.selected_tiles.append((row, col))
            self.current_word += self.tile_letters[row][col]

            # Update tile appearance
            self.tiles[row][col].config(bg='#4CAF50', fg='#ffffff')

            # Update word display
            self.word_display.config(text=self.current_word)

            print(f"Selected: ({row}, {col}) - Letter: {self.tile_letters[row][col]}")
            print(f"Current word: {self.current_word}")
        else:
            print(f"Tile ({row}, {col}) is not adjacent to the last selected tile!")
            messagebox.showwarning("Invalid Move", "You can only select adjacent tiles!")


    def is_adjacent(self, row, col):
        """Check if a tile is adjacent to the last selected tile"""
        if not self.selected_tiles:
            return True

        last_row, last_col = self.selected_tiles[-1]

        # Check if within one tile distance (including diagonals)
        row_diff = abs(row - last_row)
        col_diff = abs(col - last_col)

        return row_diff <= 1 and col_diff <= 1


    def on_hover(self, event, row, col):
        """Handle mouse hover over tile"""
        if (row, col) not in self.selected_tiles:
            # Only highlight if it's adjacent to last selected or no tiles selected
            if len(self.selected_tiles) == 0 or self.is_adjacent(row, col):
                self.tiles[row][col].config(bg='#e0e0e0')


    def on_leave(self, event, row, col):
        """Handle mouse leave tile"""
        if (row, col) not in self.selected_tiles:
            self.tiles[row][col].config(bg='#ffffff')


    def clear_selection(self):
        """Clear the current word selection"""
        # Reset all selected tiles
        for row, col in self.selected_tiles:
            self.tiles[row][col].config(bg='#ffffff', fg='#000000')

        self.selected_tiles = []
        self.current_word = ""
        self.word_display.config(text="")
        print("Selection cleared!")


    def submit_word(self):
        """Submit the current word"""
        if len(self.current_word) < 3:
            messagebox.showwarning("Invalid Word", "Words must be at least 3 letters long!")
            return

        if self.current_word in self.found_words:
            messagebox.showwarning("Duplicate Word", "You've already found this word!")
            return

        # For now, accept all words (we'll add dictionary checking later)
        self.found_words.append(self.current_word)
        self.words_listbox.insert(tk.END, self.current_word)

        # Update score (basic scoring for now)
        points = len(self.current_word) - 2  # 1 point for 3 letters, 2 for 4, etc.
        self.score += points
        self.score_label.config(text=f"Score: {self.score}")

        messagebox.showinfo("Success!", f"'{self.current_word}' added! +{points} points")

        # Clear selection after successful submission
        self.clear_selection()


    def new_game(self):
        """Start a new game"""
        # Clear everything
        self.selected_tiles = []
        self.current_word = ""
        self.found_words = []
        self.score = 0

        # Update displays
        self.score_label.config(text=f"Score: {self.score}")
        self.word_display.config(text="")
        self.words_listbox.delete(0, tk.END)

        # Generate new board
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                letter = random.choice(string.ascii_uppercase)
                self.tile_letters[row][col] = letter
                self.tiles[row][col].config(
                    text=letter,
                    bg='#ffffff',
                    fg='#000000'
                )

        print("New game started!")

