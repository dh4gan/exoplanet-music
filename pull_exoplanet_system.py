import xml.etree.ElementTree as ET

def pull_exoplanet_system(xmlfile):
    
    jup2EarthMass = 317.83
    jup2EarthRadii = 11.22
    year = 365.24
    
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
                radii.append(masses[-1]**0.666)
                  
    return periods, masses, radii
