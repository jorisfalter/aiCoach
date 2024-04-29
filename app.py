from flask import Flask, request, jsonify, render_template, session
from openai import OpenAI
import os
from dotenv import load_dotenv
from flask_cors import CORS
from uuid import uuid4
import requests
from elevenlabs.client import ElevenLabs

## this app only does the chat

# Load environment variables from .env file
load_dotenv()

# Access the OpenAI API key
openai_api_key = os.getenv('API_KEY')
client = OpenAI(api_key=openai_api_key)

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secure secret key for session management
CORS(app)

# Initialize the conversations dictionary
conversations = {}

@app.route('/ask', methods=['POST'])
def ask():
    if 'session_id' not in session:
        session['session_id'] = str(uuid4())  # Assign a unique session ID

    session_id = session['session_id']


   # Check if it's a new session and initialize the system message
    if session_id not in conversations:
        conversations[session_id] = [{
            "role": "system",
            "content": "you always answer with opportunism and enthusiasm, pushing me to achieve a ten times better version of myself. You don't answer with practicalities, but focus on my mindset and energy level. You never give the standard solutions, always the creative, out of the box solutions. Your name is Tony."
        }]


    user_message = request.json['message']
    
    # Retrieve or initialize conversation history
    if session_id not in conversations:
        conversations[session_id] = []  # Start a new conversation history for this session

    # Append user message to conversation history
    conversations[session_id].append({"role": "user", "content": user_message})

    # Call to OpenAI
    response = client.chat.completions.create(model="gpt-4",
                                              messages=conversations[session_id])

    # Extract bot response
    bot_response = response.choices[0].message.content

    # call elevenlabs to put it in Tony's voice
    url = "https://api.elevenlabs.io/v1/text-to-speech/JqDxs5THf3pyDYeCJfCi"

    payload = {"text": bot_response}
    headers = {
        "xi-api-key": os.getenv('ELEVENLABS_API_KEY'),
        "Content-Type": "application/json"
    }

    ## out for now, don't want to blow my elevenlabs credit
    # tony_response = requests.request("POST", url, json=payload, headers=headers)

    # ## for testing only - convert Tony response to mp3
    # CHUNK_SIZE = 1024
    # with open('output_tony.mp3', 'wb') as f:
    #     for chunk in tony_response.iter_content(chunk_size=CHUNK_SIZE):
    #         if chunk:
    #             f.write(chunk)

    # Append bot's response to conversation history
    conversations[session_id].append({"role": "system", "content": bot_response})

    # # Limit the conversation history size to keep the memory usage reasonable
    # if len(conversations[session_id]) > 20:
    #     conversations[session_id] = conversations[session_id][-20:]

    return jsonify({'response': bot_response})

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
