from flask import Flask, jsonify, current_app
from threading import Thread
from waitress import serve
from flask_restful import Resource, Api, reqparse
import requests
from autocorrector import autocorrector, prettify_autocorrector

parser = reqparse.RequestParser()
parser.add_argument('query', type=str, help='query to autocorrect', location='form')
parser.add_argument('number', type=int, help='number of autocorrect suggestions to output', location='form')
parser.add_argument('dictionary', type=str, help='dictionary from web url or path to file on server', location='form')
parser.add_argument('separator', type=str, help='separator for words. defaults to spaces', location='form')
parser.add_argument('prettify', type=bool, help='whether to make the json output indented', location='form')

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
        prettify = args['prettify'] if args['prettify'] else False

        if args['query'].startswith("http"):
            query = request_url_to_list(args['query'])
        elif args['query']:
            query = query.split(separator)

        if prettify == True:
            current_app.json.compact = False

        print(query)

        ac_results = autocorrector(query, number, dictionary)
        return jsonify(ac_results)
