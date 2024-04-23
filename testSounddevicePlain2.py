import sounddevice as sd
import numpy as np

def db_to_amplitude(db):
    """Convert a dB value to a linear amplitude scale."""
    return 10 ** (db / 20)

def rms(data):
    """Calculate the RMS level of audio data."""
    return np.sqrt(np.mean(np.square(data)))

def record_audio_with_silence_detection(sample_rate, channels, duration, silence_duration_threshold=-40, max_silence_length=2):
    """Record audio while detecting prolonged silence to stop early."""
    silence_threshold = db_to_amplitude(silence_duration_threshold) * 32767
    silence_time = 0
    recording = []
    def callback(indata, frames, time, status):
        nonlocal silence_time
        if status:
            print(status)
        current_rms = rms(indata[:, 0])  # Assuming mono channel
        if current_rms < silence_threshold:
            silence_time += frames / sample_rate
            if silence_time >= max_silence_length:
                print("silence abort")
                raise sd.CallbackAbort  # Stops the recording due to silence
                
        else:
            silence_time = 0  # Reset silence counter
            recording.append(indata.copy())  # Append current data to recording
            print("silence reset")


    with sd.InputStream(callback=callback, dtype='float32', channels=channels, samplerate=sample_rate):
        try:
            sd.sleep(duration * 1000)  # Convert to milliseconds and wait
        except sd.CallbackAbort:
            print("Recording stopped due to silence.")
        except KeyboardInterrupt:
            print("Recording stopped manually.")

    # Convert list of numpy arrays into a single numpy array
    if recording:
        recorded_audio = np.concatenate(recording, axis=0)
        return recorded_audio
    else:
        return np.array([])  # Return an empty array if no audio was recorded

# Parameters
sample_rate = 44100  # Sample rate in Hz
duration = 10  # Maximum duration to record unless silence stops it
channels = 1  # Mono recording

# Recording audio with silence detection
audio_data = record_audio_with_silence_detection(sample_rate, channels, duration)
print("Recording finished.")

# If needed, save the recording to a file
if audio_data.size > 0:
    import wavio
    wavio.write('output.wav', audio_data, sample_rate, sampwidth=2)
    print("File saved.")
else:
    print("No audio was recorded.")
