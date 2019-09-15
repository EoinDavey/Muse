from pydub import AudioSegment
from pydub.playback import play
import pydub.generators as gen

#for i, name in enumerate(names):
#    instrument[name] = (lambda local_i: (lambda: AudioSegment.from_file(sound_files[local_i],
#        format="mp3")))(i)

# the global dict that will store all instruments/sounds
# as functions that return AudioSegments

# might construct this programmatically later
# if we have a greater range
# octave = ["C{}", "Db{}", "D{}", "Eb{}", "E{}", "F{}", "Gb{}", "G{}", "Ab{}", "A{}", "Bb{}", "B{}"]


# this is in milliseconds
duration = 550
instrument = dict()

hello_world = [
        [('sine', '880')],
        [('sine', '440')],
        [('sine', '220')]
        ]

chords = [
        [('piano', 'C4'), ('piano', 'G4'), ('piano', 'D4')],
        [('piano', 'E4'), ('piano', 'B4'), ('piano', 'Gb4')],
        [('piano', 'G4'), ('piano', 'D4'), ('piano', 'A4')]
        ]

barbie = [
        [('piano', 'C4'), ('piano', 'G4'), ('piano', 'D4')],
        [('piano', 'E4'), ('piano', 'B4'), ('piano', 'Gb4')],
        [('wait',), ('wait',), ('piano', 'A4')]
 ]

beats = [
        [('kick',), ('kick',), ('clap',)],
        [('wait',), ('piano', 'C4'), ('piano', 'Db4')],
        [('piano', 'C4'), ('wait',), ('hihat',)]
        ]

wavey = [
        [('sine', '880'), ('square', '880'), ('triangle', '880'), ('sawtooth', '880')],
        [('sine', '440'), ('square', '440'), ('triangle', '440'), ('sawtooth', '440')],
        [('sine', '220'), ('square', '220'), ('triangle', '220'), ('sawtooth', '220')]
        ]

def get_audio_segment_for_note(instrument, note):
    return AudioSegment.from_file(f"Erato/sounds/{instrument}/{note}.mp3")

def get_audio_segment_for_drum(instrument):
    return AudioSegment.from_file(f"Erato/sounds/drum/{instrument}.mp3")


def piano(note):
    return get_audio_segment_for_note("piano", note)

def kick():
    return get_audio_segment_for_drum("kick")

def clap():
    return get_audio_segment_for_drum("clap")

def hihat():
    return get_audio_segment_for_drum("hihat")

def snare():
    return get_audio_segment_for_drum("snare")

def guitar(note, vol):
    pass

def sine(frequency):
    sine_wave = gen.Sine(int(frequency))
    return sine_wave.to_audio_segment(duration=duration)

def square(frequency):
    square_wave = gen.Square(int(frequency))
    return square_wave.to_audio_segment(duration=duration)

def triangle(frequency):
    triangle_wave = gen.Triangle(int(frequency))
    return triangle_wave.to_audio_segment(duration=duration)

def sawtooth(frequency):
    sawtooth_wave = gen.Sawtooth(int(frequency))
    return sawtooth_wave.to_audio_segment(duration=duration)

def wait():
    return AudioSegment.silent(duration=duration)

instrument["wait"] = wait
instrument["piano"] = piano
instrument["kick"] = kick
instrument["snare"] = snare
instrument["clap"] = clap
instrument["hihat"] = hihat
instrument["sine"] = sine
instrument["square"] = square
instrument["triangle"] = triangle
instrument["sawtooth"] = sawtooth

def pitch_shift(shift_octave, sound):
    new_sample_rate = int(sound.frame_rate * (2.0 ** shift_octave))
    return sound._spawn(sound.raw_data, overrides={'frame_rate':new_sample_rate})


def generate_audio(sound_matrix):
    """Takes the output from Calliope and returns a sound file."""
    track_list = list()
    final_track = AudioSegment.empty()
    for track in sound_matrix:
        cur = AudioSegment.empty()
        for beat in track:
            cur += instrument[beat[0]](*beat[1:])
        final_track = cur.overlay(final_track)
    return final_track
