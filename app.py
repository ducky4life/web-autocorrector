from flask import Flask, Response, request, render_template, send_from_directory
from threading import Thread
from waitress import serve
import requests
import time
from autocorrector import prettify_autocorrector

app = Flask('')
port = 8080

@app.route('/', methods=['GET', 'POST'])
def main_route():
    message = ""
    output_file_name = ""

    if request.method == 'POST':
        query = request.form.get('textbox', '')

        action = request.form.get('action')
        number = int(action)
        
        dictionary_input = request.form.get('dictionary', '')

        if dictionary_input.startswith("http"): # url from web
            
            if "vercel" not in request.url:
                url_text = requests.get(dictionary_input, params={"downloadformat": "txt"}).text
                filename = dictionary_input.split("/")[-1]

                with open(f"dictionary/{filename}", "w") as file:
                    file.write(url_text)
                dictionary = f"dictionary/{filename}"

            else:
                message = "web urls can only be used locally"
                dictionary = "test_files/20k_shun4midx.txt"
                
        else: # local file path
            dictionary = dictionary_input

        if not dictionary:
            dictionary = "test_files/20k_shun4midx.txt"

        if query:
            output_as_file = request.form.get('output_file_toggle') # 'on' or None

            if output_as_file == "on":
                output_file_name = f"{int(time.time())}.txt"
                output_file = f"downloads/{output_file_name}"
                prettify_autocorrector(query, number, dictionary, output_file)

            else:

                output_file = "None"
                try:
                    message = prettify_autocorrector(query, number, dictionary, output_file)

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

@app.route('/downloads/<path:filename>')
def download_file(filename):
    response = Response(filename, mimetype='text/plain')
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    return response

keep_alive()