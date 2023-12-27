from flask import Flask, jsonify, send_from_directory
import os

app = Flask(__name__)

script_dir = os.path.dirname(os.path.abspath(__file__))
DIRECTORY_PATH = os.path.join(script_dir, 'files')

@app.route('/files', methods=['GET'])
def list_files():
    try:
        files = [f for f in os.listdir(DIRECTORY_PATH) if os.path.isfile(os.path.join(DIRECTORY_PATH, f))]
        return jsonify(files)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download/<path:filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join(DIRECTORY_PATH, filename)
    print(f"Requested file: {file_path}") 
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        return jsonify({"error": "File not found"}), 404
    try:
        return send_from_directory(DIRECTORY_PATH, filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
