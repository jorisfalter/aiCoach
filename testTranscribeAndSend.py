from openai import OpenAI
import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs


# Load environment variables from .env file
load_dotenv()

# Access the OpenAI API key
openai_api_key = os.getenv('API_KEY')
client = OpenAI(api_key=openai_api_key)

import speech_recognition as sr

def listen_and_transcribe():
    # Initialize the recognizer
    recognizer = sr.Recognizer()
    
    # Start the microphone and keep listening
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        while True:
            try:
                audio = recognizer.listen(source, timeout=5)  # Listen for 5 seconds
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
                # # Call to OpenAI
                response = client.chat.completions.create(model="gpt-4",messages=messages)
                # # Extract bot response
                bot_response = response.choices[0].message.content
                print(bot_response)

            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
            except Exception as e:
                print(f"An error occurred: {e}")

# Run the function
listen_and_transcribe()
