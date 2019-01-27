import os
import sys
import threading
import wave

# PyAudio Library
import pyaudio
import scipy.fftpack as f
from pydub import AudioSegment
from scipy.io.wavfile import read
import numpy as np

FORMAT = pyaudio.paInt16
CHANNELS = 2
CHUNK = 1024    # Uh
sample_rate = 44100 # hertz, test number

class WavePlayerLoop(threading.Thread) :

  CHUNK = 1024

  def __init__(self,filepath,loop=True) :
    """
    Initialize `WavePlayerLoop` class.
    PARAM:
        -- filepath (String) : File Path to wave file.
        -- loop (boolean)    : True if you want loop playback. 
                               False otherwise.
    """
    super(WavePlayerLoop, self).__init__()
    self.filepath = os.path.abspath(filepath)
    self.loop = loop

  def run(self):
    # Open Wave File and start play!
    try:
      wf = wave.open(self.filepath, 'rb')
      player = pyaudio.PyAudio()
      old_file = self.filepath

      # Open Output Stream (basen on PyAudio tutorial)
      stream = player.open(format = player.get_format_from_width(wf.getsampwidth()),
          channels = wf.getnchannels(),
          rate = wf.getframerate(),
          output = True)

      # PLAYBACK LOOP
      data = wf.readframes(self.CHUNK)
      while self.loop :
        stream.write(data)
        data = wf.readframes(self.CHUNK)
        if data == b'' : # If file is over then rewind.
          wf.rewind()
          data = wf.readframes(self.CHUNK)

      stream.close()
      player.terminate()
    except KeyboardInterrupt:
      print("Thanks!")
      self.stop()
      return


  def play(self) :
    try:
      self.start()
    except KeyboardInterrupt:
      print("Thanks!")
      self.stop()
      return

  def stop(self) :
    self.loop = False


def sample_noise():
  audio = pyaudio.PyAudio()
  stream = audio.open(format = FORMAT, channels = CHANNELS,
                        rate = sample_rate, input = True,
                        frames_per_buffer = CHUNK)
  frames = []
  for i in range(int(sample_rate/CHUNK * 2)):
    data = stream.read(CHUNK)
    frames.append(data)

  return frames

def write_noise(filename, frames):
  audio = pyaudio.PyAudio()
  wavef = wave.open(filename, 'wb')
  wavef.setnchannels(CHANNELS)
  wavef.setsampwidth(audio.get_sample_size(FORMAT))
  wavef.setframerate(sample_rate)
  wavef.writeframes(b''.join(frames))
  wavef.close()

  frames = wavef.getnframes()
  rate = wavef.getframerate()
  duration = frames / float(rate)

  noise = AudioSegment.from_wav(filename)
  noise = noise - 40
  noise.export(filename, "wav")
 
  return filename, duration

def create_noise(sound_file):
  _, data = read(sound_file)
  a = data.T[0]   # 2 channel soundtrack, taking the first one (why does it need to be 2 channel?)
  normalized = [(ele/2**8.)*2-1 for ele in a] # this is 8-bit track, b is now normalized on [-1,1)
  fft_data = f.fft(normalized) # calculate fourier transform (complex numbers list)
  print(abs(fft_data[0]))
  for i in range(1,5):
    print(abs(fft_data[len(fft_data)-i]))


  signal_length = int(len(fft_data)/2)  # you only need half of the fft list (real signal symmetry)

  for i in range(signal_length):
    if abs(fft_data[i]) < 10000:
      fft_data[i] = abs(fft_data[i])/2
    else:
      fft_data[i] = abs(fft_data[i])**2

  new_signals = f.ifft(fft_data)

  return fft_data
