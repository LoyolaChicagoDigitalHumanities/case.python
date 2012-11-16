#
# tokens_ws.py: A simple web service to use nltk to preprocess and get
# the tokens for a sentence.
# 
# by George K. Thiruvathukal
# nltk example provided by Yu Cheng
#

from flask import Flask, jsonify, render_template, request
import nltk
import json

# This code is to setup the app container.
app = Flask(__name__)

# This code is to determine whether we have a JSON request.
# Leave unchanged.

def request_wants_json():
    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes['text/html']

# This is to handle requests of the form
#  GET <base>/tokens?sentence=value

def preprocess(sentence):
    # Preprocessing here....
    sentence = sentence.replace("happy meal", "")
    sentence = sentence.replace("http:", "")
        ## remove http://(:/ is a negative emoticon)
    sentence = sentence.replace("\. " , "\.")  ## remove elipse
    return sentence

@app.route("/tokens", methods=['GET'])
def get_tokens():

    sentence = request.args.get('sentence', "I like happy meal very much.")
    sentence = preprocess(sentence)
    tokens = nltk.word_tokenize(sentence)
    if request_wants_json():
        return json.dumps(tokens)

    # Eventually, we can have it generate an HTML version when someone
    # does GET with the text/html MIME type
    # return render_template('show_tokens.html', items=tokens)

if __name__ == "__main__":
    app.run()

