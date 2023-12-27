import sys
import os
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QListWidget

script_dir = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS_DIRECTORY_PATH = os.path.join(script_dir, 'downloads')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Network File Browser")

        layout = QVBoxLayout()

        self.file_list_widget = QListWidget()
        layout.addWidget(self.file_list_widget)

        self.refresh_button = QPushButton("Refresh File List")
        self.refresh_button.clicked.connect(self.refresh_file_list)
        layout.addWidget(self.refresh_button)

        self.download_button = QPushButton("Download Selected File")
        self.download_button.clicked.connect(self.download_selected_file)
        layout.addWidget(self.download_button)
        
        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def refresh_file_list(self):
        try:
            response = requests.get('http://127.0.0.1:5000/files')
            if response.status_code == 200:
                files = response.json()
                self.file_list_widget.clear()
                for file_name in files:
                    self.file_list_widget.addItem(file_name)
            else:
                print("Error: Unable to fetch files")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    def download_selected_file(self):
        selected_items = self.file_list_widget.selectedItems()
        if selected_items:
            filename = selected_items[0].text()
            try:
                response = requests.get(f'http://127.0.0.1:5000/download/{filename}', stream=True)
                if response.status_code == 200:
                    os.makedirs(DOWNLOADS_DIRECTORY_PATH, exist_ok=True)
                    with open(os.path.join(DOWNLOADS_DIRECTORY_PATH, filename), 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192): 
                            f.write(chunk)
                    print(f"File {filename} downloaded successfully.")
                else:
                    print("Error: Unable to download file")
            except requests.exceptions.RequestException as e:
                print(f"Error: {e}")
        else:
            print("No file selected")



app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()
