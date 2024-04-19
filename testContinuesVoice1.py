# this one uses sounddevice instead of pyaudio

import sounddevice as sd
import numpy as np
import webrtcvad
from datetime import datetime


# Initialize VAD
vad = webrtcvad.Vad()
vad.set_mode(3)  # Set mode (0 is least aggressive, 3 is most aggressive)

# Define callback function for the audio stream
def callback(indata, frames, time, status):
    if status:
        print(status)
    # We need to convert the float data to int16 for VAD
    if indata.dtype != np.int16:
        audio_data = (indata * 32767).astype(np.int16)
    else:
        audio_data = indata
    # Check each frame in the buffer
    is_speech = vad.is_speech(audio_data.tobytes(), sample_rate)
    if is_speech:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Speech detected at {current_time}!")

# Audio stream parameters
sample_rate = 16000
channels = 1

# Open audio stream with sounddevice
with sd.InputStream(callback=callback, dtype='int16', channels=channels, samplerate=sample_rate, blocksize=160):
    print("Listening... press Ctrl+C to stop.")
    sd.sleep(10000)  # Keep the stream open for a fixed amount of time (ms) or use input()/sleep() in a loop if you want it to run indefinitely

