from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO
import os
import io    
from openai import OpenAI
from dotenv import load_dotenv
import requests
import base64


app = Flask(__name__)
cors = CORS(app, resources={r"/upload": {"origins": "*"}})  # Enable CORS for the /upload route
load_dotenv()
openai_api_key = os.getenv('API_KEY')
client = OpenAI(api_key=openai_api_key)
socketio = SocketIO(app)

@app.route('/')
def index():
    print("loading html")
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
        print("Behind the messages")
        # # Call to OpenAI
        response = client.chat.completions.create(model="gpt-4o",messages=messages)
        # print(response)

        # # Extract bot response
        bot_response = response.choices[0].message.content
        print(bot_response)

        # call elevenlabs to put it in Tony's voice
        url = "https://api.elevenlabs.io/v1/text-to-speech/JqDxs5THf3pyDYeCJfCi"

        payload = {
            "text": bot_response     
            # "speed": 1.25  # Adjust the speed of the speech - apparently this doesn't work
        }
        headers = {
            "xi-api-key": os.getenv('ELEVENLABS_API_KEY'),
            "Content-Type": "application/json"
        }

        tony_response = requests.request("POST", url, json=payload, headers=headers)
        print("received tony response")
        if tony_response.status_code == 200:
            # Extract binary audio content
            audio_content = tony_response.content
            # Encode as base64
            audio_base64 = base64.b64encode(audio_content).decode('utf-8')
            # Emit the base64-encoded audio content via SocketIO
            socketio.emit('audio_response', {'data': audio_base64})

  
        else:
            print("Failed to get audio from ElevenLabs:", tony_response.status_code)

    except Exception as e:
        text = f"An error occurred: {e}"

    return jsonify({'message': 'File uploaded successfully', 'transcription': transcription.text, 'bot_response': bot_response})


    # response = jsonify({'message': 'File uploaded successfully', 'transcription': transcription.text})
    # response.headers.add('Access-Control-Allow-Origin', '*')
    # return response

if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    print(port)
    # app.run(debug=True, port=port)
    socketio.run(app, host='0.0.0.0', port=port)
