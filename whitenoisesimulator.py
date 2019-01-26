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

""" def stream_audio(frames):
    new_frames = array(frames, dtype=int16)
    bytestream = new_frames.tobytes()
    pya = pyaudio.PyAudio()  # unsure of what this is doing tbh
    stream = pya.open(format=pya.get_format_from_width(width=2), channels=1, rate=sample_rate, output=True)
    stream.write(bytestream)
    stream.stop_stream()
    stream.close()

    pya.terminate() """


def write_noise(frames, audio):
    wavef = wave.open("whitenoise.wav", 'wb')
    wavef.setnchannels(CHANNELS)
    wavef.setsampwidth(audio.get_sample_size(FORMAT))
    wavef.setframerate(sample_rate)
    wavef.writeframes(b''.join(frames))
    wavef.close()
    print("Written to file.")

frames, audio = sample_noise()
# stream_audio(frames)
write_noise(frames, audio)