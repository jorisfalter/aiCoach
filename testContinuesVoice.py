import webrtcvad
vad = webrtcvad.Vad()

# Set mode (0 is least aggressive about filtering out non-speech, 3 is most aggressive)
vad.set_mode(1)

import pyaudio
import struct

# Setup audio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=160)  # 10 ms of audio per buffer

# Check if speech is detected in each buffer
try:
    while True:
        frame = stream.read(160)
        is_speech = vad.is_speech(frame, 16000)
        if is_speech:
            print("Speech detected!")
            # Here you would forward the audio data to the AI service for processing
except KeyboardInterrupt:
    pass

# Cleanup
stream.stop_stream()
stream.close()
p.terminate()
