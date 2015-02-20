This Python repo creates music, where each exoplanet creates a note based on:

i) The period of the planet (how often the note is played)

ii) The radius of the planet (the pitch of the note, and amplitude)

The scripts behave as follows:

single_planet_note.py - generates tones based on hardcoded data
single_system_note.py - generates tones for a single system based on Open Exoplanet Catalogue Data
multiple_system_note.py - generates tones for a blend of multiple systems based on Open Exoplanet Catalogue data
all_systems_note.py - parses the entire Open Exoplanet Catalogue and generates notes for all entries (note this isn't working properly at the moment) 

This code relies on the `wavebender` module to generate tones and save them to wave files:

https://github.com/zacharydenton/wavebender

pull_exoplanet_system.py handles all the calls to wavebender, plus the extraction of exoplanet data, which is taken from a local copy of the Open Exoplanet Catalogue

https://github.com/OpenExoplanetCatalogue/open_exoplanet_catalogue

The path to the catalogue is stored in pull_exoplanet_system.py, and should
be modified accordingly before use.
