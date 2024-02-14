from flask import Flask, render_template, request
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from heapq import nlargest

nlp = spacy.load("en_core_web_sm")
app = Flask(__name__)
#for documents
def txt_summarizer(raw_docx):
    stopwords = list(STOP_WORDS)
    docx = nlp(raw_docx)
    
    word_frequencies = {}
    for word in docx:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in word_frequencies.keys():
                word_frequencies[word.text.lower()] = 1
            else:
                word_frequencies[word.text.lower()] += 1
    
    maximum_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word] / maximum_frequency)
    
    sentence_list = [sentence for sentence in docx.sents]
    
    sentence_scores = {}
    for sent in sentence_list:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if len(sent.text.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word.text.lower()]
                    else:
                        sentence_scores[sent] += word_frequencies[word.text.lower()]
    
    summarized_sentences = nlargest(7, sentence_scores, key=sentence_scores.get)
    final_sentences = [w.text for w in summarized_sentences]
    summary = ' '.join(final_sentences)
    
    return summary
# for auido files
def audiotranscription():
    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    raw_doc = request.form["text"]
    print("Received input:", raw_doc)  # Check if the input is received
    summary = txt_summarizer(raw_doc)
    print("Generated summary:", summary)  # Check if the summary is generated
    print(summary)  # Print the summary to the console
    return "Check the console for the summary"
@app.route('/avsummarize',methods = ['POST'])
def avsummarize():
    audio_file = request.form["audio"]
    print("receive input:", audio_file)
    transcription = audiotranscription(audio_file)
    print(transcription)
    return "transcribed text is: "


    
if __name__=='__main__':
    app.run(port=5000, debug=True)