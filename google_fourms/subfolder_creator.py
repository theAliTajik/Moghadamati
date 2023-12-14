import os

main_folder = "google_fourms\main_folder"
subfolders = ["subfolder1", "subfolder2"]

os.makedirs(main_folder, exist_ok=True)

for subfolder in subfolders:
    os.makedirs(os.path.join(main_folder, subfolder), exist_ok=True)
