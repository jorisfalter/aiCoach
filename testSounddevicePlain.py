import sounddevice as sd
import numpy as np
import wavio

# Parameters
sample_rate = 44100  # Sample rate in Hz
duration = 30  # Duration in seconds
filename = 'output.wav'  # Output filename

def record_audio(duration, sample_rate):
    print("Recording...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished
    print("Recording finished.")
    return audio

def save_audio(audio, filename, sample_rate):
    print(f"Saving to {filename}...")
    wavio.write(filename, audio, sample_rate, sampwidth=2)
    print("File saved.")

# Record audio
audio_data = record_audio(duration, sample_rate)

# Save recorded audio to a WAV file
save_audio(audio_data, filename, sample_rate)
