from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import pydub
import numpy as np
import requests


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_audio():
    uploaded_audio = request.files['audio']


    # Handle potential errors (file size, type, etc.)
    if not uploaded_audio:
        return jsonify({'error': 'No file uploaded'}), 400
    if not allowed_file(uploaded_audio.filename):
        return jsonify({'error': 'File type not allowed'}), 400


    # Save the audio file temporarily
    uploaded_audio.save('uploaded.wav')


    # Transcribe the audio using your preferred method (see options below)
    transcription = transcribe_audio('uploaded.wav')


    # Return the transcription as JSON
    return jsonify({'transcription': transcription})


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def transcribe_audio(filepath):
    # Choose your transcription method from the options below:


    # Option 1: Using speech_recognition library
    recognizer = sr.Recognizer()
    audiofile = sr.AudioFile(filepath)
    with audiofile as source:
        audio_data = recognizer.record(source)
    return recognizer.recognize_google(audio_data)


    # Option 2: Using a cloud-based API (replace with your API key and endpo
