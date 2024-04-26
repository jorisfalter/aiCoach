import pyaudio
import wave

# Test to ensure PyAudio reads the default input device
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
stream.start_stream()

print("Recording...")
frames = []

try:
    for i in range(0, int(44100 / 1024 * 2)):  # Record for 2 seconds
        data = stream.read(1024)
        frames.append(data)
finally:
    print("Finished recording.")

    # stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # save data as WAV file
    wf = wave.open("output.wav", 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100)
    wf.writeframes(b''.join(frames))
    wf.close()
