# Written 25/6/14 by dh4gan
# Creates a wav file with multiple notes
# Parses an XML file to find masses and periods

from wavebender import *
from numpy import log10
import pull_exoplanet_system as exo

# Define the framerate of the file and the pitch of middle C for this sound
frameRate = 44100
middleC = 1000.0 

# Define the limits of human hearing!

frequency_min = 50 # giant planets will reach the low frequencies
frequency_max = 1.0e4 # low mass planets will reach these frequencies

# Filenames
catalogue_dir = "/Users/dhf/programs/open_exoplanet_catalogue/systems/"
xmlfile = "PH-1.xml"
#xmlfile = "WASP-95.xml"
wavfile = "PH-1.wav"

filename = catalogue_dir+xmlfile

periods,masses,radii = exo.pull_exoplanet_system(filename)

print len(periods), len(masses), len(radii)

# TODO - Figure out what to do when exoplanet file incomplete (no periods)


# How long will the file last in seconds?
fileTime = 100.0

# Use this to generate a pitch
# More massive planets have a lower pitch

pitches = []
for i in range(len(radii)):
    pitches.append(middleC/radii[i])

print pitches, radii

# Notes per second - longer periods mean longer durations between notes
# This normalisation means that a period of 1 year = one second between notes

repeatrates = []
for i in range(len(periods)):
    repeatrates.append(frameRate*periods[i])

notes1 = []
notes2= []


if(len(periods)==1):
    notes1.append(damped_wave(frequency=pitches[i], amplitude=radii[i]*0.01, framerate = frameRate, length= repeatrates[i]))
    notes2.append(damped_wave(frequency=pitches[i], amplitude=radii[i]*0.01, framerate = frameRate, length= repeatrates[i]))

else:
    for i in range(len(periods)):
        print "Creating note ",i, "radius: ",radii[i]
    
        if(radii[i]>3.0):
            print "Radius greater than 5 Earth Radii, putting in notes2"
            notes2.append(damped_wave(frequency=pitches[i], amplitude=radii[i]*0.01, framerate = frameRate, length= repeatrates[i])) 
        else:
            notes1.append(damped_wave(frequency=pitches[i], amplitude=radii[i]*0.01, framerate = frameRate, length= repeatrates[i])) 
        
    
channel1 = (notes1[:])   
channel2 = (notes2[:])
channels = (channel1,channel2)

print "Channels complete"
print channels
samples = compute_samples(channels, nsamples = fileTime*frameRate)
print "Samples made"
write_wavefile(wavfile, samples)
print "File written"