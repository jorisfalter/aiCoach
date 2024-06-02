from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import speech_recognition as sr
import io    
from openai import OpenAI
from dotenv import load_dotenv
from pydub import AudioSegment



app = Flask(__name__)
cors = CORS(app, resources={r"/upload": {"origins": "*"}})  # Enable CORS for the /upload route
load_dotenv()
openai_api_key = os.getenv('API_KEY')
client = OpenAI(api_key=openai_api_key)


# UPLOAD_FOLDER = 'uploads'
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

recognizer = sr.Recognizer()


@app.route('/')
def index():
    return send_from_directory('.', 'newIndex.html')

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file found'}), 400

    file = request.files['audio']
    audio_data = file.read()
   
    # audio_file = sr.AudioFile(io.BytesIO(audio_data))
    # print(audio_file)

    try:

        # Send the audio file to OpenAI Whisper API
        transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_data
        )
  
        text = response['text']
        print("You said:", text)
    except Exception as e:
        text = f"An error occurred: {e}"

    response = jsonify({'message': 'File uploaded successfully', 'transcription': text})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run(debug=True, port=3000)
