# import speech_recognition as sr

# # Initialize recognizer class
# recognizer = sr.Recognizer()

# # Load audio file
# with sr.AudioFile('detected_speech.wav') as source:
#     audio_data = recognizer.record(source)

# # Transcribe audio file
# try:
#     text = recognizer.recognize_google(audio_data)
#     print(text)
# except sr.UnknownValueError:
#     print("Google Speech Recognition could not understand audio")
# except sr.RequestError as e:
#     print(f"Could not request results from Google Speech Recognition service; {e}")

from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the OpenAI API key
openai_api_key = os.getenv('API_KEY')
client = OpenAI(api_key=openai_api_key)

audio_file= open("detected_speech.wav", "rb")
transcription = client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_file
)
print(transcription.text)