from flask import Flask, jsonify
from threading import Thread
from waitress import serve
from flask_restful import Resource, Api, reqparse
import requests
from autocorrector import autocorrector, prettify_autocorrector

api_app = Flask('')
port = 5000
api = Api(api_app)
parser = reqparse.RequestParser()
parser.add_argument('query', type=str, help='query to autocorrect', location='form')
parser.add_argument('number', type=int, help='number of autocorrect suggestions to output', location='form')
parser.add_argument('dictionary', type=str, help='dictionary from web url or path to file on server', location='form')
parser.add_argument('separator', type=str, help='separator for words. defaults to spaces', location='form')

def request_url_to_list(url):
    url_content = requests.get(url, params={"downloadformat": "txt"}).text
    return url_content.split("\n")

class AutocorrectorApi(Resource):
    def post(self):
        args = parser.parse_args()
        query = args['query'] if args['query'] else ''
        number = args['number'] if args['number'] else 1
        dictionary = request_url_to_list(args['dictionary']) if args['dictionary'] else "test_files/20k_shun4midx.txt"
        separator = args['separator'] if args['separator'] else " "

        if args['query'].startswith("http"):
            query = request_url_to_list(args['query'])
        elif args['query']:
            query = query.split(separator)

        print(query)

        ac_results = autocorrector(query, number, dictionary)
        return jsonify(ac_results)

api.add_resource(AutocorrectorApi, '/')

def run():
    serve(api_app, host="0.0.0.0", port=port)

def keep_alive():
    server = Thread(target=run)
    server.start()
    print(f"server is running on port {port}, use 'curl -d 'query=[your query]' http://127.0.0.1:{port}'")