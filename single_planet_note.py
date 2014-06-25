# Written 25/6/14 by dh4gan
# Creates a single repeating note from an exoplanet data set
from wavebender import *

# Define the framerate of the file and the pitch of middle C for this sound
frameRate = 44100
middleC = 261.6 

# How long will the file last in seconds?
fileTime = 10.0

# Period in years
period =  3.0

# Mass in Earth Masses
mass = 1.0

# Use this to generate a pitch
# More massive planets have a lower pitch

pitch = middleC/mass

# Notes per second - longer periods mean longer durations between notes
# This normalisation means that a period of 1 year = one second between notes
repeatrate = frameRate*period

try:
    notespersec = 1.0/repeatrate
except ZeroDivisionError:
    notespersec = 1.0
    
channels = ((damped_wave(frequency=pitch, amplitude=0.3, framerate = 44100, length = repeatrate),),
            (damped_wave(frequency=pitch, amplitude=0.1, framerate = 44100, length=repeatrate),))

samples = compute_samples(channels, nsamples = fileTime*frameRate)
write_wavefile("planet2.wav", samples)