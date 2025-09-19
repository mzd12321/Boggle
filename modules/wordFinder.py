from modules.validation import WordValidator

'''
This file discovers all valid words hidden in a Boggle board.
We use DFS with prefix pruning to ensure optimisation.

Key Attributes:
 - self.validator - WordValidator instance containing the Trie dictionary

Key Methods:
 - __init__(self): 
        - Constructor that initialises the word finder
        - Creates a WordValidator instance with loaded dictionary Trie
 - find_all_words(self, board):
        - Completes the search across the board
        - Creates empty set to store unique words
        - Determines board dimensions (4x4 or 5x5)
        - Stats DFS from every possible starting position
        - Creates new visited matrix for each starting position
        - Returns a sorted list of all discovered words
        - We must start from every cell because words can begin anywhere on the board
 - dfs(self, board, row, col, current_word, visited, found_words):
        - Recursive depth-first search that explores all possible word paths
        - Parameters:
            - board - Boggle board represented as a list of lists
            - row, col - int values of current position
            - current_word - Word being built as we traverse
            - visited - 2D boolean array tracking used tiles in current path
            - found_words - Set of all discovered valid words (Prevent duplication) 
        - Algorithm flow:
            - Base case - Stops recursion if pointer is at grid boundary (prevent searching outside the grid)
            - Revisit prevention - Prevents visiting tiles already visited 
            - Word building - Append current tile's letter to 'current_word' (process 'Qu' as single letter)
            - Prefix pruning - Prefix pruning using self.validator
            - Path marking - Marks the current tile as visited temporarily
            - Word Validation - Checks if current word is complete and valid according to Boggle Rules
            - Append found word - Add the current word if valid
            - Directional search - Recursively explores all 8 adjacent tiles 
            - Backtracking - Unmarks the current tile as unvisited
        - Complexity:
            - Time complexity - O(n)
            - Space complexity - O(n) 
        
'''
class WordFinder:
    """Finds all valid words in a Boggle board using DFS with pruning"""

    def __init__(self):
        self.validator = WordValidator()

    def find_all_words(self, board):
        """Find all valid words in the board"""
        words = set() # Set to prevent duplication
        rows = len(board)
        cols = len(board[0])

        for row in range(rows):
            for col in range(cols):
                visited = [[False] * cols for _ in range(rows)]
                self.dfs(board, row, col, "", visited, words)

        return sorted(list(words))

    def dfs(self, board, row, col, current_word, visited, found_words):
        """Depth-first search with prefix pruning"""
        # Check if at the edge of the board to prevent searching outside the grid
        if row < 0 or row >= len(board) or col < 0 or col >= len(board[0]):
            return

        # Check if the tile is visited
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
