from flask import Flask, request, jsonify,send_from_directory
#from flask_cors import CORS, cross_origin   comment this on deployment
from helpers.url_fetcher import url_fetcher
from helpers.summarizer import get_summary

app = Flask(__name__, static_url_path='', static_folder='build')
#CORS(app)   comment this on deployment
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')


@app.route("/get_url", methods=['POST'])
#@cross_origin(origin='localhost:3000', headers=['Content- Type', 'application/json'])
def get_urls():
    if request.method == 'POST':
        content = request.get_json()
        print(content)
        query = content
        data = url_fetcher(query)
        json_obj = jsonify({'urls': data[1], 'description': data[0]})
        print(json_obj)
        return json_obj


@app.route("/get_summary", methods=['POST'])
#@cross_origin(origin='localhost:3000', headers=['Content- Type', 'application/json'])
def get_summaries():
    if request.method == 'POST':
        content = request.get_json()

        summaries,topic,url = get_summary(content['server_data'], content['selected_url'])
        print(summaries)
        return jsonify({'data': summaries,'topic':topic,'url':url})

if __name__ == '__main__':
    app.run()