#!pip install newspaper3k
#!pip install bert-extractive-summarizer
#!pip install transformers==2.2.0
#!conda install pytorch -c pytorch
#!conda install flask

import summaryEngine

from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='.')

@app.route('/url', methods=['GET', 'POST'])
def url_request():
    url_req = request.json
      
    #print('\n\n-----------')
    #print('The URL is => ', url_req['search_url'])
    fileSaved = summaryEngine.getSummary(url_req['search_url'])
    #print('Filename saved: ', fileSaved)
    #print('-----------\n')
    
    return jsonify(filename=fileSaved)

@app.route('/')
def index():
    return('<h1>Hello "extractiveServer_flask.py"</h1>')

if __name__ == '__main__':
	app.run(debug=True, port=5500)
