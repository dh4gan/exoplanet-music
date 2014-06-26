# Written 25/6/14 by dh4gan
# Creates a wav file with all planets in a system creating notes
# Parses an XML file to find masses and periods

from wavebender import damped_wave, compute_samples, write_wavefile
import pull_exoplanet_system as exo
import glob
from os import path

# Define the framerate of the file and the pitch of middle C for this sound
frameRate = 44100
middleC = 1000.0 

# Give a path to where the exoplanet catalogue is stored

catalogue_dir = "/Users/dhf/programs/open_exoplanet_catalogue/systems/"

# Define the limits of human hearing!

frequency_min = 50 # giant planets will reach the low frequencies
frequency_max = 1.0e4 # low mass planets will reach these frequencies

xmlfile = []


# User inputs a search string, and the script attempts to find a matching XML file 
# from the Open Exoplanet Catalogue

while(xmlfile==[]):
    xmlchoice = raw_input("Search for a system you want to play: ")
    xmlfile = glob.glob(catalogue_dir+xmlchoice+"*.xml")
    if(xmlfile==[]):
        print "Sorry, couldn't find matches for  ", xmlchoice, ", please try again"

# Now extract the filename minus the path, and construct a .wav filename

try:
    xmlfile = xmlfile[0]
    xmlfile = path.basename(xmlfile)
except IndexError:
    print "No match detected: defaulting to Sun"
    xmlfile = "Sun.xml"

wavfile = xmlfile.rsplit( ".", 1 )[ 0 ]+".wav"

print "Reading from file ",xmlfile
print "Writing sound to output ",wavfile

filename = catalogue_dir+xmlfile

# Pull the data from the XML file
periods,masses,radii = exo.pull_exoplanet_system(filename)

# TODO - Figure out what to do when exoplanet file incomplete (no radii)


# How long will the file last in seconds?
fileTime = 100.0

# Use radii to generate a pitch
# Larger planets have a lower pitch

pitches = []
for i in range(len(radii)):
    pitches.append(middleC/radii[i])
    
    # Keep the notes within human hearing!
    if(pitches[-1]<frequency_min): pitches[-1]=frequency_min
    if(pitches[-1]>frequency_max): pitches[-1]=frequency_max
    

# Notes per second - longer periods mean longer durations between notes
# This normalisation means that a period of 1 year = one second between notes

repeatrates = []
for i in range(len(periods)):
    repeatrates.append(frameRate*periods[i])

# Create lists of iterator objects for each channel
# Terrestrial planets will be in channel 1
# Giant planets will be in channel 2

notes1 = []
notes2 = []

# If there's only one planet in the system, then put it on both channels
if(len(periods)==1):
    notes1.append(damped_wave(frequency=pitches[i], amplitude=radii[i]*0.01, framerate = frameRate, length= repeatrates[i]))
    notes2.append(damped_wave(frequency=pitches[i], amplitude=radii[i]*0.01, framerate = frameRate, length= repeatrates[i]))

else:
    for i in range(len(periods)):
        print "Creating note ",i, "radius: ",radii[i]," pitch: ",pitches[i]
    
        if(radii[i]>3.0):
            notes2.append(damped_wave(frequency=pitches[i], amplitude=radii[i]*0.01, framerate = frameRate, length= repeatrates[i])) 
        else:
            notes1.append(damped_wave(frequency=pitches[i], amplitude=radii[i]*0.01, framerate = frameRate, length= repeatrates[i])) 
        
# Build each channel

channel1 = (notes1[:])   
channel2 = (notes2[:])
channels = (channel1,channel2)

print "Channels constructed"

# Create a set of samples from these channels

samples = compute_samples(channels, nsamples = fileTime*frameRate)

print "Samples made: writing to wavefile ",wavfile
print "This can take a while, please be patient!"

# Writes the output to the .wav file
write_wavefile(wavfile, samples)

print "File ",wavfile, " written"
