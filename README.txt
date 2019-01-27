Maroon Noise: a custom white noise generator
By Maggie von Ebers and Kevin Wang for TamuHack 2019

---------
This project aims to be better at blocking your own environment noises than typicaly white or pink noise. It takes
an initial sample of the ambient noise around you from your microphone and creates "maroon" noise based off of it.
Next, it will update every few seconds to any new, annoying noises around you as it loops continuously for your 
listening pleasure.
---------

This project runs from a docker container. It will continue to run until CTRL-C is pressed.