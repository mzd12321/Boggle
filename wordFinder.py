from validation import WordValidator


class WordFinder:
    """Finds all valid words in a Boggle board using DFS with pruning"""

    def __init__(self):
        self.validator = WordValidator()

    def find_all_words(self, board):
        """Find all valid words in the board"""
        words = set()
        rows = len(board)
        cols = len(board[0])

        for row in range(rows):
            for col in range(cols):
                visited = [[False] * cols for _ in range(rows)]
                self.dfs(board, row, col, "", visited, words)

        return sorted(list(words))

    def dfs(self, board, row, col, current_word, visited, found_words):
        """Depth-first search with prefix pruning"""
        if row < 0 or row >= len(board) or col < 0 or col >= len(board[0]):
            return

        if visited[row][col]:
            return

        # Add current letter
        current_word += board[row][col]

        # Pruning: stop if prefix is invalid
        if not self.validator.is_valid_prefix(current_word):
            return

        # Mark as visited
        visited[row][col] = True

        # Check if current word is valid
        if len(current_word) >= 3 and self.validator.is_valid_word(current_word):
            found_words.add(current_word)

        # Continue searching in all 8 directions
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in directions:
            self.dfs(board, row + dr, col + dc, current_word, visited, found_words)

        # Backtrack
        visited[row][col] = False


class TrieNode:
    """Node in the Trie structure for efficient word lookup"""

    def __init__(self):
        self.children = {}
        self.is_word = False


class Trie:
    """Trie data structure for efficient word validation and prefix checking"""

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        """Insert a word into the trie"""
        node = self.root
        for char in word.upper():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_word = True

    def search(self, word):
        """Check if word exists in trie"""
        node = self.root
        for char in word.upper():
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_word

    def starts_with(self, prefix):
        """Check if any word starts with this prefix (for pruning)"""
        node = self.root
        for char in prefix.upper():
            if char not in node.children:
                return False
            node = node.children[char]
        return True

