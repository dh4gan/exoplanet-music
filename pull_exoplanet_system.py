import xml.etree.ElementTree as ET

def pull_exoplanet_system(xmlfile):
    
    jup2EarthMass = 317.83
    jup2EarthRadii = 11.22
    year = 365.24
    pi = 3.1415925685
    
    # Read in XML file

    print "Reading file ", xmlfile
    tree = ET.parse(xmlfile)

    # Get System Name

    systemname =tree.findtext('name')
    print "System Name: ", systemname

    # Find all Stars and Planets in File

    stars = tree.findall(".//star")
    planets = tree.findall(".//planet")

    # Get Total Number of Bodies

    N = len(planets)

    print "There are ", N, " Planets in this system"
    
    periods = []
    masses = []
    radii = []
    
    for planet in planets:
        try:
            periods.append(planet.findtext("./period"))
        except:
            print "No period found"
            periods.append("1.0")
        
        try:
            masses.append(planet.findtext("./mass"))
        except:
            print "No mass found for planet ", planet.findtext("./name")
            
        try:
            radii.append(planet.findtext("./radius"))
        except:
            print "No radius found for planet ", planet.findtext("./name")
            
            
    # Convert data into appropriate units
    print type(periods[0])
    for i in range(len(periods)):
        periods[i] = float(periods[i])/year
        masses[i] = float(masses[i])*jup2EarthMass 
        radii[i] = float(radii[i])*jup2EarthRadii 
      
    return periods, masses, radii
