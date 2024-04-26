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
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
            except Exception as e:
                print(f"An error occurred: {e}")

# Run the function
listen_and_transcribe()
