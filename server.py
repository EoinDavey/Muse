from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/foo', methods=['POST','GET']) 
def foo():
    data = request.json
    resp = jsonify(data)
    return resp, 200
