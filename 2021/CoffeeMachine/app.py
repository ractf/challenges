import os
import re
import secrets
import subprocess
from flask import Flask, flash, request, redirect, url_for, render_template_string

UPLOAD_FOLDER = '/tmp/'
FILE_REGEX = r"^[a-zA-Z]+\.jar$"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1024 * 256
app.config['SECRET_KEY'] = secrets.token_urlsafe(1024)

def allowed_file(name):
    return bool(re.match(FILE_REGEX, name))

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if not allowed_file(file.filename):
            flash("Disallowed file name or type")
            return redirect(request.url)
        if file:
            filename = secrets.token_hex(32) + ".jar"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash(subprocess.check_output(['java', '-jar', 'coffeemachine.jar', 'file:///tmp/'+filename]).decode("utf-8"))
            return redirect(request.url)
    return render_template_string('''
    <!doctype html>
    <title>Coffee Machine</title>
    <center>
    <h1>Welcome to my Hyper-Secure Coffee Machine</h1>
    <h2>I'm so confident in how secure it is, I'm letting you upload jarfiles for FREE to run on my server. How generous am I?</h2>
    <h4>{{ get_flashed_messages()[0] }}</h4>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    </center>
    ''')

if __name__ == '__main__':
    app.run('0.0.0.0', 5000)
