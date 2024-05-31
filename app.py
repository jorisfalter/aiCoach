from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return send_from_directory('.', 'newIndex.html')

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file found'}), 400

    file = request.files['audio']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    response = jsonify({'message': 'File uploaded successfully', 'file_path': file_path})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5000)
