from pydub import AudioSegment
from pydub.playback import play
import numpy as np

# the global dict that will store all instruments/sounds
# as functions that return AudioSegments
instrument = dict()

#maths = AudioSegment.from_mp3("maths.mp3")
#bushtit = AudioSegment.from_mp3("bushtit.mp3")

# some hardcoded names of audio files for personal testing
sound_files = ["bell.mp3", "poker.mp3", "ice.mp3"]

# corresponding keys by index for the sound files above
names = ["bell", "poker", "ice"]

# this is what the dict construction will look for for nullary funcs
# probably anyways
for i, name in enumerate(names):
    instrument[name] = (lambda local_i: (lambda: AudioSegment.from_file(sound_files[local_i],
        format="mp3")))(i)


def generate_audio(sound_matrix):
    """Takes the output from Calliope and returns a sound file."""

def pitch_shift(shift_octave, sound):
    new_sample_rate = int(sound.frame_rate * (2.0 ** shift_octave))
    return sound._spawn(sound.raw_data, overrides={'frame_rate':new_sample_rate})

