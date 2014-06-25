# Written 25/6/14 by dh4gan
# Creates a wav file with multiple notes
# Parses an XML file to find masses and periods

from wavebender import *
from numpy import log10
import pull_exoplanet_system as exo

# Define the framerate of the file and the pitch of middle C for this sound
frameRate = 44100
middleC = 500.0 

# Define the limits of human hearing!

frequency_min = 50 # giant planets will reach the low frequencies
frequency_max = 1.0e4 # low mass planets will reach these frequencies


# Filename
catalogue_dir = "/Users/dhf/programs/open_exoplanet_catalogue/systems/"
xmlfile = catalogue_dir+"Sun.xml"

periods,masses,radii = exo.pull_exoplanet_system(xmlfile)

print masses

# How long will the file last in seconds?
fileTime = 100.0


# Use this to generate a pitch
# More massive planets have a lower pitch

pitches = []
for i in range(len(masses)):
    pitches.append(middleC/masses[i])

print pitches, log10(masses)

# Notes per second - longer periods mean longer durations between notes
# This normalisation means that a period of 1 year = one second between notes

repeatrates = []
for i in range(len(periods)):
    repeatrates.append(frameRate*periods[i])

notes1 = []

for i in range(4,6):
    print "Creating note ",i
    notes1.append(damped_wave(frequency=pitches[i], amplitude=0.5, framerate = frameRate, length= repeatrates[i])) 
    
channel1 = (notes1[:])

notes2=[]

for i in range(4,6):
    notes2.append(damped_wave(frequency=pitches[i], amplitude=0.5, framerate = frameRate, length= repeatrates[i])) 

channel2 = (notes2[:])
channels = (channel1,channel2)

print "Channels complete"
print channels
samples = compute_samples(channels, nsamples = fileTime*frameRate)
print "Samples made"
write_wavefile("Sun.wav", samples)
print "File written"