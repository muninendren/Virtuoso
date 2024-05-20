# from flask import Flask,render_template,url_for

# app=Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# if __name__=="__main__":
#     app.run(debug=True)

import os
from flask import Flask, jsonify, render_template, request, redirect, url_for
import requests
import spacy
from gtts import gTTS
import moviepy.editor as mp
import numpy as np
import video_gen
import merge
import time

app = Flask(__name__)

# Load spaCy English language model
nlp = spacy.load("en_core_web_sm")

@app.route('/')
def index():
    return render_template('index.html')
  

@app.route('/process', methods=['POST'])
def process():
    input_text = request.form['input-text']
    text_response = process_input(input_text)
    generate_video(text_response, "output.mp4")
    video_gen.video()
    merge.merge()
    while not os.path.exists("D:\\projectfinal\\Flaskproject\\static\\videos\\outputt.mp4"):
         time.sleep(3)  # Adjust sleep duration as needed
    # return redirect(url_for('index'))
    video_path_response = requests.get('http://127.0.0.1:5000/video_path')  # Adjust URL as needed
    video_path_data = video_path_response.json()
    video_path = video_path_data['video_path']
    
    return render_template('index.html', video_path=video_path)
    # while not os.path.exists("D:\\projectfinal\\Flaskproject\\static\\videos\\outputt.mp4"):
    #     time.sleep(1)  # Adjust sleep duration as needed
    # # return redirect(url_for('index', video_path='outputt.mp4'))
    # return jsonify({'video_ready': True})

@app.route('/video_path')
def video_path():
    # Provide the path to the generated video file
    return jsonify({'video_path': 'static/videos/outputt.mp4'})

def process_input(input_text):
    # Define a dictionary to map search queries to responses
    search_responses = {
        "Elon Musk": "Elon Musk is the founder of Tesla.",
        "OpenAI": "OpenAI is an artificial intelligence research laboratory.",
        "Apple": "Apple was founded by Steve Jobs. It is a multinational technology company that designsncomputer software, and online services.",
        "Microsoft": "Microsoft was founded by Bill Gates and Paul Allen. It develops, manufactures, licenses, supports, and sells computer software",
        "Google": "Google was founded by Larry Page and Sergey Brin. It specializes in Internet-related services and products, which include online advertising technologies, a search engine, cloud computing, software, and hardware. Google's search engine is the most widely used search engine in the world.",
        "Amazon": "Amazon was founded by Jeff Bezos. It is one of the Big Four technology companies, along with Google, Apple, and Microsoft. The company focuses on e-commerce, cloud computing, digital streaming, and artificial intelligence. Amazon is the largest online retailer in the world.",
        "Facebook": "Facebook was founded by Mark Zuckerberg. It is a social media and technology company that owns and operates several social networking platforms, including Facebook, Instagram, WhatsApp, and Oculus VR. Facebook is one of the world's most valuable companies.",
        "muni": "Founder of virtuoso",
        "prem": "Co-Founder of virtuoso",
        "sukifer": "CEO of virtuoso",
        "jai": "Managing Director of virtuoso",
        "pooja": "Manager of virtuoso",
        "rubini": "Head",
        
        # Add more search responses as needed
    }
    
    # Perform natural language understanding (NLU) using spaCy
    doc = nlp(input_text)
    
    # Extract named entities
    entities = [ent.text for ent in doc.ents]
    
    # Extract search query
    search_query = " ".join(token.text for token in doc if token.text not in entities)
    
    # Look up the search query in the dictionary
    # response = search_responses.get(search_query, "I'm sorry, I don't have information on that.")
    response=search_responses.get(input_text)
    
    return response

def generate_frames(audio_duration):
    # Define a function to generate frames for the entire duration of the audio
    def make_frame(t):
        # Dummy frame generator
        return np.zeros((480, 640, 3), dtype=np.uint8)

    # Generate frames for the entire duration of the audio
    return [make_frame(t) for t in np.arange(0, audio_duration, 1/24)]  # Assuming 24 frames per second

def generate_video(text_input, output_filename):
    # Convert text to speech
    tts = gTTS(text=text_input, lang='en')
    tts.save("output.mp3")

    # Calculate duration of the audio based on the length of the input text
    audio_duration = len(text_input.split()) / 5  # Assuming an average reading speed of 5 words per second

    # Generate frames for the entire duration of the audio
    frames = generate_frames(audio_duration)

    # Generate video with text-to-speech audio
    clip = mp.ImageSequenceClip(frames, fps=24)
    clip = clip.set_audio(mp.AudioFileClip("output.mp3"))
    clip.write_videofile(output_filename, fps=24)


# if __name__ == "__main__":
#     app.run()

