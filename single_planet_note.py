# Written 25/6/14 by dh4gan
# Creates a single repeating note from hardcoded exoplanet data

import pull_exoplanet_system as exo

# Define the framerate of the file and the pitch of middle C for this sound

# How long will the file last in seconds?
fileTime = 10.0

# Period in years
periods =  [3.0]

# Mass in Earth Masses
mass = 1.0

# Radius in Earth Radii
radii = [1.0]

wavfile = 'singleplanet.wav'

exo.generate_notes_periods_radii(periods,radii, fileTime, wavfile, frameRate=44100, middleC = 1000.0)
