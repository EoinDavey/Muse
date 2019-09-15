from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from textx import TextXSyntaxError

from tempfile import NamedTemporaryFile

import Calliope.parser as parser
import Erato.audio_engine as audio_engine
from pydub.playback import play
import sys

app = Flask(__name__)
CORS(app)

@app.route('/foo', methods=['POST','GET']) 
def foo():
    data = request.json
    code = data['code']
    try:
        print(code)
        p = parser.parseToAudio(code)
        print(p)
        seg = audio_engine.generate_audio(p)

        fname = '/tmp/temp.mp3'

        with open(fname,'wb+') as f:
            seg.export(f.name, "mp3")

        return send_file(fname, mimetype="audio/mpeg", as_attachment=True), 200

    except TextXSyntaxError as err:
        print(err)
        return ('',204)

    return ('',204)
