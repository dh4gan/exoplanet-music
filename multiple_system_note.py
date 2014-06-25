# Written 25/6/14 by dh4gan
# Creates a wav file with multiple notes
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

ifile = 0
nfiles = 2


periods = []
masses = []
radii = []

wavfile = "multiple.wav"

while(ifile < nfiles):
    ifile +=1
    xmlfile = []
    while(xmlfile==[]):
        
        xmlchoice = raw_input("Search for a system you want to play: ")
        xmlfile = glob.glob(catalogue_dir+xmlchoice+"*.xml")
        print xmlfile
        if(xmlfile==[]):
            print "Sorry, couldn't find matches for  ", xmlchoice, ", please try again"


    try:
        xmlfile = xmlfile[0]
        xmlfile = path.basename(xmlfile)
    except IndexError:
        print "No match detected: defaulting to Sun"
        xmlfile = "Sun.xml"

        #wavfile = xmlfile.rsplit( ".", 1 )[ 0 ]+".wav"



    print "Reading from file ",xmlfile
    print "Writing sound to output ",wavfile

    print xmlfile, wavfile

    filename = catalogue_dir+xmlfile

    systemperiods,systemmasses,systemradii = exo.pull_exoplanet_system(filename)

    periods = periods + systemperiods
    masses = masses + systemmasses
    radii = radii+ systemradii
    
print periods
print len(periods), len(masses), len(radii)

# TODO - Figure out what to do when exoplanet file incomplete (no radii)


# How long will the file last in seconds?
fileTime = 100.0

# Use this to generate a pitch
# More massive planets have a lower pitch

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

notes1 = []
notes2= []


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
        
channel1 = (notes1[:])   
channel2 = (notes2[:])
channels = (channel1,channel2)

print "Channels constructed"

samples = compute_samples(channels, nsamples = fileTime*frameRate)
print "Samples made: writing to wavefile ",wavfile
print "This can take a while, please be patient!"

write_wavefile(wavfile, samples)
print "File written"