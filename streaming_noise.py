from maroonnoisesimulator import *
import time
from pydub import AudioSegment
import subprocess
import asyncio

audio = pyaudio.PyAudio()


print("\nCrying babies on airplanes are a thing of the past! Press CTRL-C to exit.")
print("First, we gather a quick sample of your background noise.")

print("Playing...")

async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

async def ugh():
    #time.wait(duration/2)
    # audio.terminate()

    stream = audio.open(format = FORMAT, channels = CHANNELS,
                        rate = sample_rate, input = True,
                        frames_per_buffer = CHUNK)
    
    old_white = AudioSegment.from_wav("whitenoise.wav")
    frames = sample_noise(stream, 1)
    sample,_ = write_noise("sample.wav", frames, audio)
    signal = create_noise(sample)
    white_noise, duration = write_noise("whitenoise.wav", signal, audio)
    new_white = AudioSegment.from_wav(white_noise)
    combined = old_white.overlay(new_white)
    combined.export("whitenoise.wav", format="wav")
    stream.stop_stream()
    stream.close()
    

async def main():
    stream = audio.open(format = FORMAT, channels = CHANNELS,
                        rate = sample_rate, input = True,
                        frames_per_buffer = CHUNK)
    frames = sample_noise(stream,2)
    stream.stop_stream()
    stream.close()
    sample,_ = write_noise("sample.wav", frames, audio)
    signal = create_noise(sample)
    white_noise, duration = write_noise("whitenoise.wav", signal, audio)
    try:
        while True:
            await asyncio.gather(
                run("afplay whitenoise.wav"),
                ugh()
            )
            
    except KeyboardInterrupt:
         print("\nDid that work for you? Let us know what you think!")     # CTRL - C
         audio.terminate()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("\nDid that work for you? Let us know what you think!")     # CTRL - C
    audio.terminate()