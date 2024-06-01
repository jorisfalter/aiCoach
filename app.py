from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import speech_recognition as sr
import io    
import wavio



app = Flask(__name__)
cors = CORS(app, resources={r"/upload": {"origins": "*"}})  # Enable CORS for the /upload route

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
        print("Processing audio...")

        # Use wavio to read the WAV file
        with io.BytesIO(audio_data) as wav_io:
            wav_io.seek(0)
            wav = wavio.read(wav_io)

        # Create an AudioData instance from the wavio output
        audio = sr.AudioData(wav.data.tobytes(), wav.rate, wav.sampwidth)

        text = recognizer.recognize_google(audio)  # Transcribe using Google Web Speech API
        print("You said:", text)
    except sr.UnknownValueError:
        text = "Google Web Speech API could not understand the audio."
    except sr.RequestError as e:
        text = f"Could not request results from Google Web Speech API; {e}"

    response = jsonify({'message': 'File uploaded successfully', 'transcription': text})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run(debug=True, port=3000)
