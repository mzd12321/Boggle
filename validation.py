import os

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



class WordValidator:
    """Validates words against dictionary using Trie"""

    def __init__(self, dictionary_path='data/enable1.txt'):
        self.trie = Trie()
        self.load_dictionary(dictionary_path)

    def load_dictionary(self, path):
        """Load dictionary file into Trie"""
        if not os.path.exists(path):
            print(f"Dictionary not found at {path}, using basic word list")
            self.load_basic_words()
            return

        try:
            with open(path, 'r') as f:
                word_count = 0
                for line in f:
                    word = line.strip().upper()
                    if len(word) >= 3:  # Boggle minimum
                        self.trie.insert(word)
                        word_count += 1
                print(f"Loaded {word_count} words from dictionary")
        except Exception as e:
            print(f"Error loading dictionary: {e}")
            self.load_basic_words()

    def load_basic_words(self):
        """Fallback basic word list"""
        basic_words = [
            'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL',
            'CAN', 'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'DAY', 'GET',
            'HAS', 'HIM', 'HIS', 'HOW', 'ITS', 'MAY', 'NEW', 'NOW'
        ]
        for word in basic_words:
            self.trie.insert(word)

    def is_valid_word(self, word):
        """Check if word is valid"""
        return self.trie.search(word)

    def is_valid_prefix(self, prefix):
        """Check if prefix could lead to valid word (for pruning)"""
        return self.trie.starts_with(prefix)



if __name__ == '__main__':
    pass