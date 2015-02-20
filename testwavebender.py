# Written 25/6/14 by dh4gan
# This script tests the wavebender package 
# Found at https://github.com/zacharydenton/wavebender

# This is my hack of the binaural.py example file

from wavebender import sine_wave, compute_samples, write_wavefile

channels = ((sine_wave(170.0, amplitude=0.1),),
            (sine_wave(178.0, amplitude=0.1),))

samples = compute_samples(channels)
write_wavefile("test.wav", samples)
