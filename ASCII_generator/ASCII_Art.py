import json
import os

def generate_ascii_art(text, json_file):
    with open(json_file, 'r') as file:
        font = json.load(file)

    if font["allcapital"]:
        text = text.upper()

    ascii_art_lines = [""] * font["char_height"]

    for char in text:
        if char in font:
            for i in range(font["char_height"]):
                ascii_art_lines[i] += font[char][i] + "  "
        else:
            for i in range(font["char_height"]):
                ascii_art_lines[i] += "     "

    ascii_art = "\n".join(ascii_art_lines)

    return ascii_art

def list_json_files(directory):
    return [file for file in os.listdir(directory) if file.endswith('.json')]


directory = 'ASCII_generator/Fonts/'

json_files = list_json_files(directory)
for i, file in enumerate(json_files):
    print(f"{i + 1}: {file}")

file_index = int(input("Select a font file by number: ")) - 1
json_file = os.path.join(directory, json_files[file_index])


text = input("Enter the text you want to convert: ")
ascii_art = generate_ascii_art(text, json_file)
print(ascii_art)
