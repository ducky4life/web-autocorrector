from flask import Flask, jsonify, current_app, Response
from threading import Thread
from waitress import serve
from flask_restful import Resource, Api, reqparse
import requests
from autocorrector import autocorrector, prettify_autocorrector

parser = reqparse.RequestParser()
parser.add_argument('query', type=str, location='form')
parser.add_argument('number', type=int, choices=(1,2,3), help='number must be between 1 to 3 inclusive', location='form')
parser.add_argument('dictionary', type=str, location='form')
parser.add_argument('separator', type=str, location='form')
parser.add_argument('prettify', type=str, location='form')
parser.add_argument('help', type=str, location='form')

help_message = """Usage: curl -d '[options]=[value]' https://web-autocorrector.vercel.app/api
Options:
    'query' (required) - input text or raw txt file link to be processed.

    'number' - the number of possible autocorrected words to output for each word. defaults to 1.

    'dictionary' - a raw txt file link with one word on each line to be used as the custom dictionary for the algorithm.

    'separator' - a string that separates each word in the input. defaults to spaces. you should use 'separator=\n' for most txt files.

    'prettify' - whether to prettify the json output into human readable form or leave it as one line. defaults to False.

    'help' - shows this message.

Examples can be found at https://github.com/ducky4life/web-autocorrector?tab=readme-ov-file#api-examples
"""

def request_url_to_list(url):
    url_content = requests.get(url, params={"downloadformat": "txt"}).text
    return url_content.split("\n")

class AutocorrectorApi(Resource):
    def post(self):
        args = parser.parse_args()
        query = args['query'] if args['query'] else 'none'
        number = args['number'] if args['number'] else 1
        dictionary = request_url_to_list(args['dictionary']) if args['dictionary'] else "test_files/20k_shun4midx.txt"
        separator = args['separator'] if args['separator'] else " "
        prettify = args['prettify'] if args['prettify'] else "False"
        help_needed = args['help']

        if help_needed == "":
            response = Response(help_message)
            return(response)

        if query.startswith("http"):
            query = request_url_to_list(query)
        elif query:
            print(separator)
            query = query.split(separator)

        if prettify.lower() == "true":
            current_app.json.compact = False
        else:
            current_app.json.compact = True

        print(query)

        ac_results = autocorrector(query, number, dictionary)
        return jsonify(ac_results)
    
    def get(self):
        response = Response(help_message)
        return(response)

