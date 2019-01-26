import pyaudio  # I think we'll maybe need this?
import numpy as np  # you haven't used this yet either just be careful
from scipy.io.wavfile import read
import scipy.fftpack as f
# import pylab
import wave, struct, math   # check to make sure you're using all of this
import matplotlib.pyplot as plt
import pandas as pd

audio = pyaudio.PyAudio()

FORMAT = pyaudio.paInt16
CHANNELS = 2
CHUNK = 1024    # Uh
       
sample_rate = 44100 # hertz, test number
sample_duration = 2.0   # seconds
write_frequency = 440.0

min_value = 5000   # minimum intensity for a frequency to be considered important enough to work with

max_volume = 32767.0    # literally the max, can we do a slider?

def create_noise(sound_file):
    _, data = read(sound_file)
    a = data.T[0]   # 2 channel soundtrack, taking the first one (why does it need to be 2 channel?)
    normalized = [(ele/2**8.)*2-1 for ele in a] # this is 8-bit track, b is now normalized on [-1,1)
    fft_data = f.fft(normalized) # calculate fourier transform (complex numbers list)

    signal_length = int(len(fft_data)/2)  # you only need half of the fft list (real signal symmetry)
    # print(abs(fft_data[:(signal_length - 1)]))
    # for x in abs(fft_data[:(signal_length - 1)]):
      #  print(x)

    # this all just plots it for ease of access I spose
    k = np.arange(len(data))
    T = len(data)/sample_rate  # where fs is the sampling frequency
    frq_label = k/T
    # plt.xlabel(frq_label)
    plt.plot(abs(fft_data[:(signal_length-1)]),'r') 
    plt.show()

    for i in range(signal_length):
        if abs(fft_data[i]) < min_value:
            fft_data[i] = 0

    new_signals = f.ifft(fft_data)
    return new_signals




def sample_noise():
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
    
    # write_noise(frames, audio):


""" def stream_audio(frames):
    new_frames = array(frames, dtype=int16)
    bytestream = new_frames.tobytes()
    pya = pyaudio.PyAudio()  # unsure of what this is doing tbh
    stream = pya.open(format=pya.get_format_from_width(width=2), channels=1, rate=sample_rate, output=True)
    stream.write(bytestream)
    stream.stop_stream()
    stream.close()

    pya.terminate() """


def write_noise(filename, frames, audio):
    # filename = "whitenoise.wav"
    wavef = wave.open(filename, 'wb')
    wavef.setnchannels(CHANNELS)
    wavef.setsampwidth(audio.get_sample_size(FORMAT))
    wavef.setframerate(sample_rate)
    wavef.writeframes(b''.join(frames))
    wavef.close()
    print("Written to file.")
    return filename

frames, audio = sample_noise()
# stream_audio(frames)
sample_name = write_noise("samplenoise.wav", frames, audio)
new_signals = create_noise(sample_name)
new_name = write_noise("newnoise.wav", new_signals, audio)