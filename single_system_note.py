# Written 25/6/14 by dh4gan
# Creates a wav file with all planets in a system creating notes
# Parses an XML file to find masses and periods


import pull_exoplanet_system as exo
import glob
from os import path


# Give a path to where the exoplanet catalogue is stored

xmlfile = []

# User inputs a search string, and the script attempts to find a matching XML file 
# from the Open Exoplanet Catalogue

while(xmlfile==[]):
    xmlchoice = raw_input("Search for a system you want to play: ")
    xmlfile = glob.glob(exo.catalogue_dir+xmlchoice+"*.xml")
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

# Pull the data from the XML file
periods,masses,radii = exo.pull_exoplanet_system(xmlfile)

# How long will the file last in seconds?
fileTime = 100.0

exo.generate_notes_periods_radii(periods,radii, fileTime, wavfile, frameRate=44100, middleC = 1000.0)

# TODO - Figure out what to do when exoplanet file incomplete (no radii)
