import pyaudio  # I think we'll maybe need this?
import numpy
import wave, struct, math

FORMAT = pyaudio.paInt16
CHANNELS = 2
CHUNK = 1024    # Uh
       
sample_rate = 44100 # hertz, test number
sample_duration = 5.0   # seconds
write_frequency = 440.0

max_volume = 32767.0    # literally the max, can we do a slider?

def sample_noise():
    audio = pyaudio.PyAudio()
    stream = audio.open(format = FORMAT, channels = CHANNELS,
                        rate = sample_rate, input = True,
                        frames_per_buffer = CHUNK)
    print("Recording...")
    frames = []
    for i in range(int(sample_rate/CHUNK * sample_duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    print("Finished recording")
    audio.terminate()

    return frames, audio
    
    # write_noise(frames, audio)


def write_noise(frames, audio):
    wavef = wave.open("whitenoise.wav", 'wb')
    wavef.setnchannels(CHANNELS)
    wavef.setsampwidth(audio.get_sample_size(FORMAT))
    wavef.setframerate(sample_rate)
    wavef.writeframes(b''.join(frames))
    wavef.close()
    print("Written to file.")

frames, audio = sample_noise()