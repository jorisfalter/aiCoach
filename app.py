from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import io    
from openai import OpenAI
from dotenv import load_dotenv



app = Flask(__name__)
cors = CORS(app, resources={r"/upload": {"origins": "*"}})  # Enable CORS for the /upload route
load_dotenv()
openai_api_key = os.getenv('API_KEY')
client = OpenAI(api_key=openai_api_key)


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
        audio_file = io.BytesIO(audio_data)
        audio_file.name = "recording.wav"
        # Send the audio file to OpenAI Whisper API
        transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
        print(transcription.text)
        # text = transcription['text']
        # print("You said:", text)

        messages = [{
            "role": "system",
            "content": "you always answer with opportunism and enthusiasm, pushing me to achieve a ten times better version of myself. You don't answer with practicalities, but focus on my mindset and energy level. You never give the standard solutions, always the creative, out of the box solutions. Your name is Tony."
            }, {
            "role": "user",
            "content": transcription.text
        }]
        print(messages)
        # # Call to OpenAI
        response = client.chat.completions.create(model="gpt-4o",messages=messages)
        print(bot_response)

        # # Extract bot response
        bot_response = response.choices[0].message.content
        print(bot_response)
    except Exception as e:
        text = f"An error occurred: {e}"

    # response = jsonify({'message': 'File uploaded successfully', 'transcription': transcription.text})
    # response.headers.add('Access-Control-Allow-Origin', '*')
    # return response

if __name__ == '__main__':
    app.run(debug=True, port=3000)
