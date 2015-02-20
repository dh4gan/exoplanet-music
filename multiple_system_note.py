# Written 25/6/14 by dh4gan
# Creates a wav file with multiple notes
# Parses an XML file to find masses and periods

import pull_exoplanet_system as exo
import glob
from os import path

# Define the framerate of the file and the pitch of middle C for this sound
frameRate = 44100
middleC = 1000.0 

# Define the limits of human hearing!

frequency_min = 50 # giant planets will reach the low frequencies
frequency_max = 1.0e4 # low mass planets will reach these frequencies

ifile = 0
nfiles = input("How many systems do you want to mix together? ")

periods = []
masses = []
radii = []

wavfile = "multiple.wav"

while(ifile < nfiles):
    ifile +=1
    xmlfile = []
    while(xmlfile==[]):
        
        xmlchoice = raw_input("Search for a system you want to play: ")
        xmlfile = glob.glob(exo.catalogue_dir+xmlchoice+"*.xml")
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

    systemperiods,systemmasses,systemradii = exo.pull_exoplanet_system(xmlfile)

    periods = periods + systemperiods
    masses = masses + systemmasses
    radii = radii+ systemradii
    
print periods
print len(periods), len(masses), len(radii)

# How long will the file last in seconds?
fileTime = 100.0

exo.generate_notes_periods_radii(periods,radii, fileTime, wavfile, frameRate=44100, middleC = 1000.0)
# TODO - Figure out what to do when exoplanet file incomplete (no radii)
