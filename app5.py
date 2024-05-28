from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import threading
import speech_recognition as sr
import requests
from openai import OpenAI
import os
from dotenv import load_dotenv
import base64

## this app includes the audio
# purpose is to make it with a clickable button rather than making it listen at all times
## or to stop listening when the AI speaks
# OpeanAI stops listening

app = Flask(__name__)
socketio = SocketIO(app)

load_dotenv()

# Access the OpenAI API key
openai_api_key = os.getenv('API_KEY')
client = OpenAI(api_key=openai_api_key)

is_listening = False
recognizer = sr.Recognizer()
audio_thread = None

def handle_audio():
    global is_listening
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        while is_listening:
            try:
                audio = recognizer.listen(source)
                print("Processing audio...")
                text = recognizer.recognize_google(audio)
                print("You said:", text)
                
                messages = [{
                    "role": "system",
                    "content": "you always answer with opportunism and enthusiasm, pushing me to achieve a ten times better version of myself. You don't answer with practicalities, but focus on my mindset and energy level. You never give the standard solutions, always the creative, out of the box solutions. Your name is Tony."
                }, {
                    "role": "user",
                    "content": text
                }]
                
                response = client.chat.completions.create(model="gpt-4o",messages=messages)
                bot_response = response.choices[0].message.content
                print(bot_response)
                socketio.emit('display_text', {'user_text': text, 'bot_text': bot_response})
                
                url = "https://api.elevenlabs.io/v1/text-to-speech/JqDxs5THf3pyDYeCJfCi"
                payload = {"text": bot_response}
                headers = {
                    "xi-api-key": os.getenv('ELEVENLABS_API_KEY'),
                    "Content-Type": "application/json"
                }

                tony_response = requests.post(url, json=payload, headers=headers)
                if tony_response.status_code == 200:
                    audio_content = tony_response.content
                    audio_base64 = base64.b64encode(audio_content).decode('utf-8')
                    socketio.emit('audio_response', {'data': audio_base64})
                else:
                    socketio.emit('audio_error', {'error': 'Failed to fetch audio'})
            except Exception as e:
                print(f"An error occurred: {e}")

@app.route('/')
def index():
    return render_template('index3.html')

@socketio.on('start_listening')
def start_listening():
    global is_listening, audio_thread
    if not is_listening:
        is_listening = True
        audio_thread = threading.Thread(target=handle_audio)
        audio_thread.start()
        emit('listening_started', {'status': 'Listening started'})

@socketio.on('stop_listening')
def stop_listening():
    global is_listening
    is_listening = False
    emit('listening_stopped', {'status': 'Listening stopped'})

if __name__ == '__main__':
    socketio.run(app, debug=True)
