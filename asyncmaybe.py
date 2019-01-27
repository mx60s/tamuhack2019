from tryingagain import *
import numpy as np
#import asyncio

def main():
    # Sampling
    print("Sampling the room...")
    frames = sample_noise()

    name, _ = write_noise("sample.wav", frames)
    new_frames = create_noise(name)
    name,_  = write_noise("whitenoise.wav", new_frames)
    player = WavePlayerLoop("whitenoise.wav",True)
    player.play()

    # Play
    try:
        while True:
            frames = sample_noise()
            print("Sampled")
            name, _ = write_noise("sample.wav", frames)
            new_frames = create_noise(name)
            name,_  = write_noise("whitenoise.wav", new_frames)

            player.filepath = os.path.abspath("whitenoise.wav")
            print("Changed")

    except KeyboardInterrupt:
        print("See you space cowboy~")

main()