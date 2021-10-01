from flask import Flask
import datetime
from youtube_transcript_api import YouTubeTranscriptApi
from flask import request
import json
from youtube_transcript_api.formatters import TextFormatter
from transformers import T5ForConditionalGeneration, T5Tokenizer
import validators
from flask_cors import CORS


# define a variable to hold you app
app = Flask(__name__)
CORS(app)

def summarize(text):
    # initialize the model architecture and weights
    model = T5ForConditionalGeneration.from_pretrained("t5-base")
    # initialize the model tokenizer
    tokenizer = T5Tokenizer.from_pretrained("t5-base")
    inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(
    inputs, 
    max_length=1500, 
    min_length=40, 
    length_penalty=2.0, 
    num_beams=4, 
    early_stopping=True)
    return tokenizer.decode(outputs[0])

# define your resource endpoints
# http://[hostname]/api/summarize?youtube_url=<url>
# https://www.youtube.com/watch?v=3oqSom_V7Zg
@app.route('/api/summarize', methods=['GET'])
def get_transcript():
    print("Request generated...")
    youtube_url = request.args.get('youtube_url', '')
    #validate the url
    valid=validators.url(youtube_url)
    if valid==False:
        return "No response, pls check the url :)"

    try:
        video_id = youtube_url.split('?')[1].split('=')[1]
    except:
        return "No response, pls check the url :)" 
    
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    formatter = TextFormatter()
    text_formatted = formatter.format_transcript(transcript)
    return summarize(text_formatted)
     

# server the app when this file is run
if __name__ == '__main__':
    app.run(debug=True)