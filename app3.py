from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import threading
import speech_recognition as sr
import requests
from playsound import playsound
import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
import requests
import base64
from groq import Groq


## this app is a test version with Groq and LLama3

app = Flask(__name__)
# socketio = SocketIO(app, logger=True, engineio_logger=True)
socketio = SocketIO(app)
# socketio.run(app, debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))

# Load environment variables from .env file
load_dotenv()

# Access the OpenAI API key
groq_api_key = os.getenv('GROQ_API_KEY')
client = Groq(api_key=groq_api_key)

import speech_recognition as sr

@app.route('/')
def index():
    return render_template('index2.html')

def handle_audio():
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 2.0  # seconds of non-speaking audio before a phrase is considered complete
    # Start the microphone and keep listening
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        while True:
            print("In the while loop")
            try:
                print("In the Try")
                audio = recognizer.listen(source)
                print("Processing audio...")
                text = recognizer.recognize_google(audio)  # Transcribe using Google Web Speech API
                print("You said:", text)
              
                messages = [{
                    "role": "system",
                    "content": "you always answer with opportunism and enthusiasm, pushing me to achieve a ten times better version of myself. You don't answer with practicalities, but focus on my mindset and energy level. You never give the standard solutions, always the creative, out of the box solutions. Your name is Tony."
                    }, {
                    "role": "user",
                    "content": text
                }]
                # # Call to Groq
                chat_completion = client.chat.completions.create( messages,
                    model="llama3-8b-8192")
                # # Extract bot response
                bot_response = chat_completion.choices[0].message.content
                # print(bot_response)
                socketio.emit('display_text', {'user_text': text, 'bot_text': bot_response})


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
                  # Emit the response via SocketIO
                if tony_response.status_code == 200:
                    # Extract binary audio content
                    audio_content = tony_response.content
                    # Encode as base64
                    audio_base64 = base64.b64encode(audio_content).decode('utf-8')
                    # Emit the base64-encoded audio content via SocketIO
                    socketio.emit('audio_response', {'data': audio_base64})
                else:
                    print("Failed to get audio from ElevenLabs:", tony_response.status_code)
                    # Handle error appropriately, maybe send an error message to the client
                    socketio.emit('audio_error', {'error': 'Failed to fetch audio'})

                # if tony_response.status_code == 200:
                #     audio_content = tony_response.content
                #     audio_base64 = base64.b64encode(audio_content).decode('utf-8')
                #     return jsonify({"audio_data": audio_base64})
                # else:
                #     return jsonify({"error": "Failed to fetch audio"}), 500

            # if it didn't capture the audio
            except sr.WaitTimeoutError:
                print("Listening timed out whilst waiting for phrase to start")
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
            except Exception as e:
                print(f"An error occurred: {e}")

@app.route('/start_listening', methods=['POST'])
def start_listening():
    # threading.Thread(target=handle_audio).start()
    print("Starting audio capture...")
    socketio.start_background_task(handle_audio)
    return jsonify(success=True)

if __name__ == '__main__':
    # app.run(debug=True)
    socketio.run(app, debug=True)

