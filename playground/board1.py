import random
import string


class BoardGenerator:
    """Generates Boggle boards based on difficulty"""

    # Common letter frequencies for more realistic boards
    LETTER_WEIGHTS = {
        'E': 12, 'T': 9, 'A': 8, 'O': 8, 'I': 7, 'N': 7,
        'S': 6, 'H': 6, 'R': 6, 'L': 4, 'D': 4, 'C': 3,
        'U': 3, 'M': 3, 'W': 2, 'F': 2, 'G': 2, 'Y': 2,
        'P': 2, 'B': 1, 'V': 1, 'K': 1, 'J': 1, 'X': 1,
        'Q': 1, 'Z': 1
    }

    def __init__(self, size=4, difficulty='Easy'):
        self.size = size
        self.difficulty = difficulty
        self.setup_letter_pool()

    def setup_letter_pool(self):
        """Create weighted letter pool"""
        self.letter_pool = []
        for letter, weight in self.LETTER_WEIGHTS.items():
            self.letter_pool.extend([letter] * weight)

    def generate(self):
        """Generate a board based on difficulty"""
        # For now, generate random board
        # TODO: Implement difficulty-based generation
        board = []
        for row in range(self.size):
            board_row = []
            for col in range(self.size):
                letter = random.choice(self.letter_pool)
                board_row.append(letter)
            board.append(board_row)
        return board


class WordValidator:
    """Validates words against dictionary"""

    def __init__(self):
        # For now, accept common words
        # TODO: Load actual dictionary file
        self.valid_words = {
            'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL',
            'CAN', 'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'DAY', 'GET',
            'HAS', 'HIM', 'HIS', 'HOW', 'ITS', 'MAY', 'NEW', 'NOW',
            'OLD', 'SEE', 'TWO', 'WAY', 'WHO', 'BOY', 'DID', 'ITS',
            'LET', 'PUT', 'SAY', 'SHE', 'TOO', 'USE', 'HER', 'FEW',
            'BIG', 'GOD', 'WHY', 'RUN', 'HOT', 'EAT', 'FAR', 'FUN',
            'BAD', 'BAG', 'YET', 'ARM', 'BAD', 'LAY', 'JOB', 'CUT',
            'YES', 'KEY', 'LOT', 'SAD', 'HIT', 'EAR', 'FAT', 'AGE', 'HIDE'
        }

    def is_valid_word(self, word):
        """Check if word is valid"""
        return word.upper() in self.valid_words

