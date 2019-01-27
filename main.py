from utilities import *


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
    um = True
    try:
        while True:
            if um:
                filename = "whitenoise0.wav"
            else:
                filename = "whitenoise1.wav"
            frames = sample_noise()
            print("Sampled")
            name, _ = write_noise(filename, frames)
            new_frames = create_noise(name)
            name,_  = write_noise(filename, new_frames)

            player.filepath = os.path.abspath(filename)
            print("Changed")
            os.remove(filename)
            um = not um

    except KeyboardInterrupt:
        print("Thanks!")
        return

main()