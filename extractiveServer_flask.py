from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='.')

@app.route('/url', methods=['GET', 'POST'])
def url_request():
    url_req = request.json
    print()
    print(url_req['search_url'])
    print()
    return jsonify(
        filename='data\\cna_news_for_testing.csv'
    )

@app.route('/')
def index():
    return('<h1>INDEX</h1>')

if __name__ == '__main__':
	app.run(debug=True, port=5500)
