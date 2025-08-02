from flask import Flask, request, render_template, jsonify
from threading import Thread
from waitress import serve
import requests
import time
from flask_restful import Api
from autocorrector import autocorrector, prettify_autocorrector
from api import AutocorrectorApi

app = Flask('')
port = 8080
api_app = Api(app)
app.json.compact = False

def request_url_to_list(url):
    url_content = requests.get(url, params={"downloadformat": "txt"}).text
    return url_content.split("\n")

@app.route('/', methods=['GET', 'POST'])
def main_route():
    message = ""
    error = ""
    output_file_name = ""

    if request.method == 'POST':

        
        input_text = request.form.get('input', '')
        input_file = request.files.get("input_file_upload")

        action = request.form.get('action')
        number = int(action)

        dictionary_input = request.form.get('dictionary', '')
        dictionary_file = request.files.get("dictionary_file_upload")

        output_as_file = request.form.get('output_file_toggle') # 'on' or None
        alphabetize_output = request.form.get('alphabetize_toggle')
        separator_input = request.form.get('separator')
        separator = separator_input if separator_input else "\n"

        keyboard_layout = request.form.get('keyboard_layout')
        disable_keyboard = request.form.get('disable_keyboard_toggle')
        
        if input_file:
            input_list = input_file.readlines()
            query = [item.decode('utf-8').replace("\n", "").replace("\r", "") for item in input_list]
        
        elif input_text.startswith("http"):
            input_list = request_url_to_list(input_text)
            query = [item.replace("\n", "").replace("\r", "") for item in input_list]

        else:
            input_list = input_text.replace("\r", "").split(separator)
            query = [item.replace("\n", "").replace("\r", "") for item in input_list]



        if dictionary_input.startswith("http"): # url from web
            dictionary = request_url_to_list(dictionary_input)

        elif dictionary_file: # uploaded file
            dictionary_file_content = dictionary_file.readlines()
            dictionary = [item.decode('utf-8').replace("\n", "").replace("\r", "") for item in dictionary_file_content]
                
        elif dictionary_input: # local file path
            dictionary = dictionary_input

        else:
            dictionary = "test_files/20k_shun4midx.txt"


        if disable_keyboard == "on":
            keyboard_layout = []


        if query != ['']:

            print(query)

            if output_as_file == "on":

                output_file_name = f"fqhll_output_{int(time.time())}"
                content = autocorrector(query, number, dictionary, alphabetize_output, keyboard_layout)
                response = jsonify(content)
                response.headers["Content-Disposition"] = f"attachment; filename={output_file_name}"
                return response

            else:
                try:
                    message = prettify_autocorrector(query, number, dictionary, alphabetize_output, keyboard_layout)
                except Exception as e:
                    error = f"Error: {e}"

        else:
            error = "Please enter a query."
            
    return render_template("index.html", message=message, error=error, filepath=output_file_name)

api_app.add_resource(AutocorrectorApi, '/api')

def run():
    serve(app, host="0.0.0.0", port=port)

def keep_alive():
    server = Thread(target=run)
    server.start()
    print(f"server is running on port {port}, api route: http://127.0.0.1:{port}/api")

keep_alive()
