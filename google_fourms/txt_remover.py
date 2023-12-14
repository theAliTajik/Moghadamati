import os

def remove_txt_at(path):
    for filename in os.listdir(path):
        if filename.endswith(".txt"):
            file_path = os.path.join(path, filename)
            os.remove(file_path)

if __name__ == "__main__":
    remove_txt_at(input("enter path to remove .txt at: "))