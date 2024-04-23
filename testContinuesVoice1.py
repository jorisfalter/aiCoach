# this one uses sounddevice instead of pyaudio
# it can record voice now, but it stops automatically after 8 seconds
# also the sound quality is poor

import sounddevice as sd
import numpy as np
import webrtcvad
from datetime import datetime
from pydub import AudioSegment
import time


# Initialize VAD
vad = webrtcvad.Vad()
vad.set_mode(3)  # Set mode (0 is least aggressive, 3 is most aggressive)
# Audio stream parameters
sample_rate = 16000
channels = 1
#
audio_format = np.int16
collected_frames = []
silence_threshold = 2.0  # seconds of silence to stop recording

# # Define callback function for the audio stream
# def callback(indata, frames, time, status):
#     if status:
#         print(status)

#     if is_speech:
#         collected_frames.append(audio_data)
#         current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         print(f"Speech detected at {current_time}")

def callback(indata, frames, time, status):
    global silence_time  # Declare silence_time as global
    if status:
        print(status)
    audio_data = (indata * 32767).astype(np.int16).tobytes()
    collected_frames.append(audio_data)
    # We need to convert the float data to int16 for VAD
    if indata.dtype != np.int16:
        audio_data = (indata * 32767).astype(np.int16)
    else:
        audio_data = indata
    # Check each frame in the buffer
    is_speech = vad.is_speech(audio_data.tobytes(), sample_rate)
    if is_speech:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Speech detected at {current_time}")
        silence_time = 0  # reset silence time
    else:
        silence_time += frames / sample_rate  # increment silence time by the duration of the current frame
        print("Silence time")

# Open audio stream with sounddevice
stream = sd.InputStream(callback=callback, dtype=audio_format, channels=channels, samplerate=sample_rate, blocksize=320)

with stream:
    print("Listening... press Ctrl+C to stop.")
    start_time = time.time()
    while True:
        time.sleep(0.1)  # Short sleep to reduce CPU usage
        if silence_time >= silence_threshold:
            break
        if time.time() - start_time > 30:  # Stops after 30 seconds regardless of silence
            break


# Concatenate all frames of detected speech into one AudioSegment
if collected_frames:
    audio_data = b''.join(collected_frames)
    audio_segment = AudioSegment(data=audio_data, sample_width=2, frame_rate=sample_rate, channels=channels)

    audio_segment.export("detected_speech.wav", format="wav")
    print("Exported detected speech to 'detected_speech.wav'")