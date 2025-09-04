import os
import urllib.request


def download_dictionary():
    """Download the ENABLE word list for Boggle"""

    # Create data directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')

    url = 'https://raw.githubusercontent.com/dolph/dictionary/master/enable1.txt'
    filepath = 'enable1.txt'

    if os.path.exists(filepath):
        print(f"Dictionary already exists at {filepath}")
        return

    print("Downloading dictionary...")
    try:
        urllib.request.urlretrieve(url, filepath)
        print(f"Dictionary downloaded successfully to {filepath}")

        # Count words
        with open(filepath, 'r') as f:
            word_count = sum(1 for line in f if len(line.strip()) >= 3)
        print(f"Dictionary contains {word_count} words (3+ letters)")

    except Exception as e:
        print(f"Error downloading dictionary: {e}")
        print("You can manually download from:")
        print(url)


if __name__ == '__main__':
    download_dictionary()