from pydub import AudioSegment
from pydub.playback import play

# the global dict that will store all instruments/sounds
# as functions that return AudioSegments
instrument = dict()

maths = AudioSegment.from_mp3("maths.mp3")
bushtit = AudioSegment.from_mp3("bushtit.mp3")

# some hardcoded names of audio files for personal testing
sound_files = ["bell.mp3", "ice.mp3", "poker.mp3"]

# corresponding keys by index for the sound files above
names = ["bell", "ice", "poker"]

# this is what the dict construction will look for for nullary funcs
# probably anyways
for i, name in enumerate(names):
    instrument[name] = lambda: AudioSegment.from_file(sound_files[i],
            format="mp3")


def generate_audio(sound_matrix):
    """Takes the output from Calliope and returns a sound file."""
    for key in instrument:
        play(instrument[key]())
