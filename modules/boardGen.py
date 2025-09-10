import random
from modules.wordFinder import WordFinder  # Add this import at the top


class BoardGenerator:
    """Generates Boggle boards based on difficulty"""

    # Classic Boggle dice configuration (16 dice for 4x4)
    CLASSIC_DICE = [
        "AAEEGN", "ELRTTY", "AOOTTW", "ABBJOO",
        "EHRTVW", "CIMOTU", "DISTTY", "EIOSST",
        "DELRVY", "ACHOPS", "HIMNQU", "EEINSU",
        "EEGHNW", "AFFKPS", "HLNNRZ", "DEILRX"
    ]

    # Big Boggle dice (25 dice for 5x5)
    BIG_DICE = [
        "AAAFRS", "AAEEEE", "AAFIRS", "ADENNN", "AEEEEM",
        "AEEGMU", "AEGMNN", "AFIRSY", "BJKQXZ", "CCNSTW",
        "CEIILT", "CEILPT", "CEIPST", "DDLNOR", "DHHLOR",
        "DHHNOT", "DHLNOR", "EIIITT", "EMOTTT", "ENSSSU",
        "FIPRSY", "GORRVW", "HIPRRY", "NOOTUW", "OOOTTU"
    ]

    def __init__(self, size=4, difficulty='Easy'):
        self.size = size
        self.difficulty = difficulty
        self.word_finder = WordFinder()

    def generate(self):
        """Generate a board that meets difficulty requirements"""
        max_attempts = 50

        for attempt in range(max_attempts):
            if self.size == 4:
                board = self.generate_from_dice(self.CLASSIC_DICE)
            elif self.size == 5:
                board = self.generate_from_dice(self.BIG_DICE)
            else:
                board = self.generate_random()

            # Check if board meets difficulty requirements
            word_count = len(self.word_finder.find_all_words(board))

            if self.meets_difficulty(word_count):
                print(f"Board generated with {word_count} words (Difficulty: {self.difficulty})")
                return board

        # If no suitable board found, return last attempt
        print(f"Warning: Could not generate board meeting {self.difficulty} difficulty")
        return board

    def generate_from_dice(self, dice):
        """Generate board using Boggle dice"""
        shuffled_dice = dice.copy()
        random.shuffle(shuffled_dice)

        board = []
        dice_index = 0

        for row in range(self.size):
            board_row = []
            for col in range(self.size):
                die = shuffled_dice[dice_index]
                letter = random.choice(die)
                # Handle Qu as a single tile
                if letter == 'Q':
                    letter = 'Qu'
                board_row.append(letter)
                dice_index += 1
            board.append(board_row)

        return board

    def generate_random(self):
        """Generate random board with weighted letters"""
        letter_weights = {
            'E': 12, 'T': 9, 'A': 8, 'O': 8, 'I': 7, 'N': 7,
            'S': 6, 'H': 6, 'R': 6, 'L': 4, 'D': 4, 'C': 3,
            'U': 3, 'M': 3, 'W': 2, 'F': 2, 'G': 2, 'Y': 2,
            'P': 2, 'B': 1, 'V': 1, 'K': 1, 'J': 1, 'X': 1,
            'Qu': 1, 'Z': 1
        }

        letter_pool = []
        for letter, weight in letter_weights.items():
            letter_pool.extend([letter] * weight)

        board = []
        for row in range(self.size):
            board_row = []
            for col in range(self.size):
                letter = random.choice(letter_pool)
                board_row.append(letter)
            board.append(board_row)

        return board

    def meets_difficulty(self, word_count):
        """Check if word count meets difficulty requirements"""
        if self.size == 4:
            if self.difficulty == 'Easy':
                return word_count >= 80
            elif self.difficulty == 'Medium':
                return 50 <= word_count < 80
            elif self.difficulty == 'Hard':
                return word_count < 50
        elif self.size == 5:
            # Adjust for 5x5 grid
            if self.difficulty == 'Easy':
                return word_count >= 150
            elif self.difficulty == 'Medium':
                return 100 <= word_count < 150
            elif self.difficulty == 'Hard':
                return word_count < 100
        return True
