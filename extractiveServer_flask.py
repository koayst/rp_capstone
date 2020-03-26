#!pip install newspaper3k
#!pip install bert-extractive-summarizer
#!pip install transformers==2.2.0
#!conda install pytorch -c pytorch
#!conda install flask
#
# Date Created: 1 March 2020
#
# To run:
# python extractiveServer_flask.py
#
# Flask server app to process the request from Streamlit webapp.
#
# /url - to get a summary of the news article when a URL is being passed
# /update - update the summarizer machine with the indexes
#

import summaryEngine

from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='.')

# to process the request and then return the summary
@app.route('/url', methods=['GET', 'POST'])
def url_request():
    url_req = request.json
      
    print('\n-----------')
    print('The URL is => ', url_req['search_url'])
    fileSaved = summaryEngine.getSummary(url_req['search_url'])
    print('Filename saved: ', fileSaved)
    print('-----------\n')
    
    return jsonify(filename=fileSaved)

# to update the indexes of the summary
@app.route('/update', methods=['GET', 'POST'])
def update_request():

    url_req = request.json
    print('\n-----------')
    print('File to update: ', url_req['filename'])
    print('Indexes to update: ', url_req['indexes'])
    print('-----------\n')
    
    return jsonify(success=True)

@app.route('/')
def index():
    return('<h1>Hello "extractiveServer_flask.py"</h1>')

if __name__ == '__main__':
	app.run(debug=True, port=5500)
