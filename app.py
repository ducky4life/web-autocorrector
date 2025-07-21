from flask import Flask, request, render_template, Response
from threading import Thread
from waitress import serve
import requests
import time
from autocorrector import autocorrector, prettify_autocorrector

app = Flask('')
port = 8080

@app.route('/', methods=['GET', 'POST'])
def main_route():
    message = ""
    output_file_name = ""

    if request.method == 'POST':

        
        input_text = request.form.get('input', '')
        input_file = request.files.get("input_file_upload")

        action = request.form.get('action')
        number = int(action)

        dictionary_input = request.form.get('dictionary', '')
        dictionary_file = request.files.get("dictionary_file_upload")

        output_as_file = request.form.get('output_file_toggle') # 'on' or None
        separator_input = request.form.get('separator')
        separator = separator_input if separator_input else "\n"



        if input_file:
            input_file_content = input_file.readlines()
            query = separator.join([item.decode('utf-8').replace("\n", "").replace("\r", "") for item in input_file_content])
        
        else:
            query = input_text



        if dictionary_input.startswith("http"): # url from web
            url_content = requests.get(dictionary_input, params={"downloadformat": "txt"}).text
            dictionary = url_content.split("\n")

        elif dictionary_file: # uploaded file
            dictionary_file_content = dictionary_file.readlines()
            dictionary = [item.decode('utf-8').replace("\n", "").replace("\r", "") for item in dictionary_file_content]
                
        elif dictionary_input: # local file path
            dictionary = dictionary_input

        else:
            dictionary = "test_files/20k_shun4midx.txt"



        if query:

            if output_as_file == "on":

                output_file_name = f"fqhll_output_{int(time.time())}.txt"
                content = autocorrector(query, number, dictionary, separator)
                response = Response(content, mimetype='text/plain')
                response.headers["Content-Disposition"] = f"attachment; filename={output_file_name}"
                return response

            else:
                try:
                    message = prettify_autocorrector(query, number, dictionary, separator)

                except Exception as e:
                    message = f"Error: {e}"

        else:
            message = "Please enter a query."
            
    return render_template("index.html", message=message, filepath=output_file_name)

def run():
    serve(app, host="0.0.0.0", port=port)

def keep_alive():
    server = Thread(target=run)
    server.start()
    print(f"server is running on port {port}")

keep_alive()