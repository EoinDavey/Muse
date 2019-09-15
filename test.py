import Calliope.parser as parser
import Erato.audio_engine as audio_engine
from pydub.playback import play
import sys

lines = sys.stdin.read()
p = parser.parseToAudio(lines)
seg = audio_engine.generate_audio(p)
play(seg)
