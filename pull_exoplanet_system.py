import xml.etree.ElementTree as ET
from wavebender import damped_wave, compute_samples, write_wavefile


jup2EarthMass = 317.83
jup2EarthRadii = 11.22
year = 365.24


# Define the limits of human hearing!
frequency_min = 50 # giant planets will reach the low frequencies
frequency_max = 1.0e4 # low mass planets will reach these frequencies

def pull_exoplanet_system(xmlfile):
    

    
    # Read in XML file

    print "Reading file ", xmlfile
    tree = ET.parse(xmlfile)

    # Get System Name

    systemname =tree.findtext('name')
    print "System Name: ", systemname

    # Find all Planets in File
    planets = tree.findall(".//planet")

    # Get Total Number of Bodies

    N = len(planets)

    if(N>1):
        print "There are ", N, " Planets in this system"
    else:
        print "There is ", N, " Planet in this system"
    
    periods = []
    masses = []
    radii = []
    
    for planet in planets:
        try:
            periods.append(planet.findtext("./period"))
            periods[-1] = float(periods[-1])/year
        except:
            print "No period found"
            return [], [], []
            
        
        try:
            masses.append(planet.findtext("./mass"))
            masses[-1] = float(masses[-1])*jup2EarthMass 
        except:
            print "No mass found for planet ", planet.findtext("./name")
            masses.append(1.0)
            
        try:
            radii.append(planet.findtext("./radius"))
            radii[-1] = float(radii[-1])*jup2EarthRadii
        except:
            print "No radius found for planet ", planet.findtext("./name")
            return [], [], []
            # If no radius found, infer it from mass
            if(masses[-1]>300):
                radii.append(11.2)
            else:
                radii.append(masses[-1]**0.666) # TODO - check this is the correct prescription!
                  
    return periods, masses, radii

def generate_notes_periods_radii(periods,radii, fileTime, wavefile, frameRate=44100, middleC = 1000.0):
    '''Generates a .wav file using the periods and radii of the exoplanet dataset'''
    
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
        
        
    create_wavefile(notes1,notes2,fileTime,wavefile)
    
    
def generate_notes_periods_only(periods, wavefile, frameRate=44100, middleC = 1000.0):
    '''Generates a .wav file using the orbital periods alone from the exoplanet dataset'''
    
    
def create_wavefile(notes1,notes2, fileTime, wavefile, frameRate = 44100):
    '''Generates a wavefile given notes for channels 1 and 2'''
    
    # Build each channel

    channel1 = (notes1[:])   
    channel2 = (notes2[:])
    channels = (channel1,channel2)

    print "Channels constructed"
    print "Channels constructed"

    # Create a set of samples from these channels

    samples = compute_samples(channels, nsamples = fileTime*frameRate)

    print "Samples made: writing to wavefile ",wavefile
    print "This can take a while, please be patient!"

    # Writes the output to the .wav file
    write_wavefile(wavefile, samples)

    print "File ",wavefile, " written"
