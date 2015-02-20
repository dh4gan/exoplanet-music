# Written 25/6/14 by dh4gan
# Creates a wav file with multiple notes
# Parses an XML file to find masses and periods

import pull_exoplanet_system as exo
import glob
from os import path

# Define the limits of human hearing!

frequency_min = 50 # giant planets will reach the low frequencies
frequency_max = 1.0e4 # low mass planets will reach these frequencies

# Amplitude tweak to prevent saturation

amplitude_tweak = 0.005

ifile = 0
nfiles = 2


periods = []
masses = []
radii = []

wavfile = "all.wav"

xmlfiles = glob.glob(exo.catalogue_dir+"*.xml")

for inputfile in xmlfiles:        

    xmlfile = path.basename(inputfile)

    print "Reading from file ",xmlfile
    print "Writing sound to output ",wavfile

    systemperiods,systemmasses,systemradii = exo.pull_exoplanet_system(xmlfile)

    periods = periods + systemperiods
    masses = masses + systemmasses
    radii = radii+ systemradii
   
print "Number of periods collected: ",len(periods)
print "Number of radii collected: ", len(radii) 
print "Periods, radii collected"

for i in range(len(periods)):
    
    print periods[i], radii[i]


# How long will the file last in seconds?
fileTime = 10.0

exo.generate_notes_periods_radii(periods,radii, fileTime, wavfile, frameRate=44100, middleC = 1000.0)

# TODO - Figure out what to do when exoplanet file incomplete (no radii)
