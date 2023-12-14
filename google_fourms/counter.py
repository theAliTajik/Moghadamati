# Here is a Python program that reads a .txt file, counts all lines, words, and characters, and prints the results.

def count_file_contents(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Initialize counters
        line_count = len(lines)
        word_count = 0
        character_count = 0

        # Count words and characters
        for line in lines:
            words = line.split()
            word_count += len(words)
            character_count += len(line)

        return line_count, word_count, character_count
    except FileNotFoundError:
        return "File not found."
    except:
        return "unknown error"

# The file path needs to be specified here.
file_path = "google_fourms/counter_test.txt"

# Uncomment the line below to run the function with a specific file.
print(count_file_contents(file_path))
