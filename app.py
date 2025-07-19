from flask import Flask, request, render_template, send_from_directory
from threading import Thread
from waitress import serve
from autocorrector import prettify_autocorrector

app = Flask('')
port=8080

@app.route('/', methods=['GET', 'POST'])
def main_route():
    message = ""

    if request.method == 'POST':
        query = request.form.get('textbox', '')
        action = request.form.get('action')
        number = int(action)

        if query:
            try:
                message = prettify_autocorrector(query, number)

            except Exception as e:
                message = f"Error: {e}"
        else:
            message = "Please enter a query."
            
    return render_template("index.html", message=message)

def run():
    serve(app, host="0.0.0.0", port=port)

def keep_alive():
    server = Thread(target=run)
    server.start()
    print(f"server is running on port {port}")

keep_alive()