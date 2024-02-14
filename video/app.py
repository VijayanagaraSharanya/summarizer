from flask import Flask, render_template, request, redirect, url_for
from moviepy.editor import VideoFileClip
import speech_recognition as sr

app = Flask(__name__)

def extract_audio(video_path, output_path):
    video_clip = VideoFileClip(video_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(output_path)
    video_clip.close()

def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
        transcription = recognizer.recognize_google(audio_data)

    return transcription

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe_video', methods=['POST'])
def transcribe_video():
    if 'video_file' not in request.files:
        return redirect(url_for('index'))

    video_file = request.files['video_file']

    if video_file.filename == '':
        return redirect(url_for('index'))

    try:
        # Save the uploaded video file
        video_path = 'uploads/' + video_file.filename
        video_file.save(video_path)

        # Extract audio from the video
        audio_path = 'uploads/audio.wav'
        extract_audio(video_path, audio_path)

        # Transcribe the audio
        transcription = transcribe_audio(audio_path)

        return render_template('index.html', transcription=transcription)
    except Exception as e:
        return render_template('index.html', error=f'Error processing video: {e}')

if __name__ == '__main__':
    app.run(debug=True)
