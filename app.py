from flask import render_template, jsonify, Flask
from flask import request, redirect, session
import os


app = Flask(__name__)

@app.route('/')
def first():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()
