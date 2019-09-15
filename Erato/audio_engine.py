from pydub import AudioSegment
from pydub.playback import play

#maths = AudioSegment.from_mp3("maths.mp3")
#bushtit = AudioSegment.from_mp3("bushtit.mp3")

# some hardcoded names of audio files for personal testing
#sound_files = ["bell.mp3", "poker.mp3", "ice.mp3"]

# corresponding keys by index for the sound files above
#names = ["bell", "poker", "ice"]

# this is what the dict construction will look for for nullary funcs
# probably anyways
#for i, name in enumerate(names):
#    instrument[name] = (lambda local_i: (lambda: AudioSegment.from_file(sound_files[local_i],
#        format="mp3")))(i)

# the global dict that will store all instruments/sounds
# as functions that return AudioSegments

# might construct this programmatically later
# if we have a greater range
octave = ["C{}", "Db{}", "D{}", "Eb{}", "E{}", "F{}", "Gb{}", "G{}", "Ab{}", "A{}", "Bb{}", "B{}"]


instrument = dict()
piano_keys = dict()

for note in octave:
    resolved_note = note.format("4")
    piano_notes[note] = get_audio_segment_for_note("piano",resolved_note)


def get_audio_segment_for_note(instrument, note):
    return AudioSegment.from_file(f"sounds/{instrument}/{note}.mp3")

def piano(note):
    return get_audio_segment_for_note("piano", note)

def drum(vol):
    pass

def guitar(note, vol):
    pass

instrument["piano"] = piano


def pitch_shift(shift_octave, sound):
    new_sample_rate = int(sound.frame_rate * (2.0 ** shift_octave))
    return sound._spawn(sound.raw_data, overrides={'frame_rate':new_sample_rate})


def generate_audio(sound_matrix):
    track_list = list()
    final_track = AudioSegment.empty()
    """Takes the output from Calliope and returns a sound file."""
    for track in sound_matrix:
        cur = AudioSegment.empty()
        for beat in track:
            cur += instrument[beat[0]](*beat[1:])
        final_track = cur.overlay(final_track)
    return final_track
