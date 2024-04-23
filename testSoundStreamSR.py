import speech_recognition as sr

def listen_for_speech(timeout=5):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source, timeout=timeout)
        print("Processing audio...")

    try:
        # Process audio (you can use Google, IBM, etc.)
        transcript = recognizer.recognize_google(audio)
        print("Transcription:", transcript)
    except sr.UnknownValueError:
        print("No speech detected.")
    except sr.RequestError as e:
        print(f"Could not process audio: {e}")

# This will listen for the first speech and stop after a period of silence.
listen_for_speech()
