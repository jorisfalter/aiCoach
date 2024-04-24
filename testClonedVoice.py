from elevenlabs.client import ElevenLabs
import os
from dotenv import load_dotenv
from pydub import AudioSegment
import io
import requests

# Load environment variables from .env file
load_dotenv()

url = "https://api.elevenlabs.io/v1/text-to-speech/JqDxs5THf3pyDYeCJfCi"

payload = {"text": "That's the spirit! Now, multiply that energy by ten. Picture yourself as the best version of you - proactive, passionate, unstoppable. Can you see it? That's who you are about to become today. Let every challenge be an opportunity for growth. Your creativity is your secret weapon, never forget that. You got this!"}
headers = {
    "xi-api-key": os.getenv('ELEVENLABS_API_KEY'),
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

CHUNK_SIZE = 1024
with open('output2.mp3', 'wb') as f:
    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
        if chunk:
            f.write(chunk)


