from flask import Flask, request, render_template, send_from_directory
from threading import Thread
from waitress import serve
from autocorrector import prettify_autocorrector

app = Flask('')

@app.route('/', methods=['GET', 'POST'])
def main_route():
    message = ""

    if request.method == 'POST':
        query = request.form.get('textbox', '')
        action = request.form.get('action')
        number = int(action)

        if query:
            try:
                ac_results = prettify_autocorrector(query, number)
                message = ac_results[0]
                dict_length = ac_results[1]

            except Exception as e:
                message = f"Error: {e}"
        else:
            message = "Please enter a query."
            
    return render_template("index.html", message=message, dict_length=dict_length)

def run():
    serve(app, host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()
    print("server is running on port 8080")

@app.route('/downloads/<path:filename>')
def download_file(filename):
    return send_from_directory('downloads', filename, as_attachment=True)

keep_alive()