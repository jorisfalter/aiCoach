#this one doesn't work

import sounddevice as sd
import numpy as np
import webrtcvad
from datetime import datetime
from pydub import AudioSegment

# Initialize VAD
vad = webrtcvad.Vad()
vad.set_mode(3)  # Most aggressive mode

sample_rate = 16000
channels = 1
audio_format = np.int16
collected_frames = []
silence_threshold = 2.0  # seconds of silence to stop recording
silence_time = 0

def callback(indata, frames, time, status):
    if status:
        print(status)
    # Convert the input data to int16 if not already
    audio_data = (indata * 32767).astype(np.int16) if indata.dtype != np.int16 else indata
    # Check if frame is the correct length for VAD
    frame_length = len(audio_data)
    if frame_length in [160, 320, 480]:  # Check correct frame length
        is_speech = vad.is_speech(audio_data.tobytes(), sample_rate)
        if is_speech:
            collected_frames.append(audio_data.tobytes())
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Speech detected at {current_time}")
        else:
            silence_time += frame_length / sample_rate
    else:
        print(f"Frame length {frame_length} is incorrect")


# Setup the stream and define the callback
stream = sd.InputStream(callback=callback,
                        dtype=audio_format, 
                        channels=channels, 
                        samplerate=sample_rate, 
                        blocksize=int(sample_rate * 0.1))  # 100 ms blocks

with stream:
    print("Listening... press Ctrl+C to stop.")
    while silence_time < silence_threshold:
        sd.sleep(int(sample_rate * 0.1))  # sleep for block size duration

# Export collected audio
if collected_frames:
    audio_data = b''.join(collected_frames)
    audio_segment = AudioSegment(data=audio_data, sample_width=2, frame_rate=sample_rate, channels=channels)
    audio_segment.export("detected_speech.mp3", format="mp3")
    print("Exported detected speech to 'detected_speech.mp3'")
