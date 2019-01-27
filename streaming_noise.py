from whitenoisesimulator import *
import time

audio = pyaudio.PyAudio()
print(audio.get_device_count())

stream = audio.open(format = FORMAT, channels = CHANNELS,
                        rate = sample_rate, input = True,
                        frames_per_buffer = CHUNK)
frames = sample_noise(stream,5)
stream.stop_stream()
stream.close()
sample,_ = write_noise("sample.wav", frames, audio)
signal = create_noise(sample)
white_noise, duration = write_noise("whitenoise.wav", signal, audio)


print("Playing...")

try:
    while True:
        # exec white noise
        time.sleep(duration/3)
        stream = audio.open(format = FORMAT, channels = CHANNELS,
                        rate = sample_rate, input = True,
                        frames_per_buffer = CHUNK)
        frames = sample_noise(stream, 2)
        stream.stop_stream()
        stream.close()
        print("Finished recording")
        # audio.terminate()
        sample,_ = write_noise("sample.wav", frames, audio)
        signal = create_noise(sample)
        white_noise, duration = write_noise("whitenoise.wav", signal, audio)

except KeyboardInterrupt:
    print("\nDid that work for you? Let us know what you think!")     # CTRL - C
    audio.terminate()
