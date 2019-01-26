import pyaudio  # I think we'll maybe need this?
import numpy as np  # you haven't used this yet either just be careful
from scipy.io.wavfile import read
from scipy.fftpack import fft
import pylab
import wave, struct, math   # check to make sure you're using all of this
import matplotlib.pyplot as plt

FORMAT = pyaudio.paInt16
CHANNELS = 2
CHUNK = 1024    # Uh
       
sample_rate = 44100 # hertz, test number
sample_duration = 5.0   # seconds
write_frequency = 440.0

min_value = 0   # minimum intensity for a frequency to be considered important enough to work with

max_volume = 32767.0    # literally the max, can we do a slider?

def create_noise(sound_file):
    _, data = read(sound_file)
    a = data.T[0]   # 2 channel soundtrack, taking the first one (why does it need to be 2 channel?)
    normalized = [(ele/2**8.)*2-1 for ele in a] # this is 8-bit track, b is now normalized on [-1,1)
    fft_data = fft(normalized) # calculate fourier transform (complex numbers list)

    # this all just plots it for ease of access I spose
    signal_length = int(len(fft_data)/2)  # you only need half of the fft list (real signal symmetry)
    plt.plot(abs(fft_data[:(signal_length-1)]),'r') 
    k = np.arange(len(data))
    T = len(data)/sample_rate  # where fs is the sampling frequency
    frq_label = k/T
    plt.xlabel(frq_label)
    plt.show()
    




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


def write_noise(frames, audio):
    filename = "whitenoise.wav"
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
name = write_noise(frames, audio)
create_noise(name)