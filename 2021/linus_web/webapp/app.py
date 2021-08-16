#!/usr/bin/env python3
from os.path import join
from os import walk
from pathlib import Path
from secrets import token_urlsafe
from subprocess import check_call, CalledProcessError

from flask import Flask, redirect, render_template, request, send_from_directory
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'webm'}
YES = "https://www.youtube.com/embed/xvFZjo5PgG0?autoplay=1&controls=0"


app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1000 * 1000
UPLOAD_PATH_OBJ = Path("uploads/")
EXCLUDE_FILE = UPLOAD_PATH_OBJ / "note.txt"
MATERIAL_CARD_TEMPLATE = """
<div class="mdc-layout-grid__cell mdc-layout-grid__cell--align-middle mdc-layout-grid__cell--span-12-desktop mdc-layout-grid__cell--span-4-phone mdc-layout-grid__cell--span-8-tablet">
<div class="mdc-card mdc-elevation-transition resources-tab-card">
<div class="padded-resource-card">
    <h2 class="resource-card-title mdc-typography mdc-typography--headline6">{0}</h2>
    <h3 class="resource-card-subtitle mdc-typography mdc-typography--subtitle2">User</h3>
</div>
<div class="resource-card-secondary">
    <video controls playsinline>
    <source src="{1}" type="video/webm">
</video>
</div>
</div>
</div>
"""


def ffmpeg_pipeline(inp_fp):
    file_path = Path(inp_fp)

    if file_path.exists():
        encoded_name = (Path("uploads") / token_urlsafe()).with_suffix(".mp4")
        try:
            shell_cmd = f'ffmpeg -i static/perfect.mp3 -f lavfi -i color=size=1920x1080:duration=4:rate=25:color=black -vf "drawtext=fontfile=static/Roboto-Light.ttf:fontsize=30:fontcolor=white:textfile={str(file_path)}" {encoded_name}'
            return not bool(check_call(f"{shell_cmd} 2>/dev/null >/dev/null", shell=True)), encoded_name

        except(CalledProcessError):
            encoded_name.unlink(True)
            return False, None
    else:
        return False, None


def valid_filename(fname: str) -> bool:
    return '.' in fname and fname.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=["GET"])
def index_page():
    user_items = ""
    for i in next(walk(str(UPLOAD_PATH_OBJ)))[2]:
        this_file = UPLOAD_PATH_OBJ / i
        if valid_filename(str(this_file)):
            user_items += MATERIAL_CARD_TEMPLATE.format(this_file.stem, this_file)
    return render_template("index.html", user_content=user_items)


@app.route('/uploads/<video_name>', methods=["GET"])
def load_video(video_name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], video_name)


@app.route('/upload/content', methods=["POST"])
def upload_video():

    if request.method == 'POST':
        try:
            source = request.form.get("source", "").lower()

            if source == "internal":
                fp_internal = request.form.get("file", None)
                if fp_internal is not None:
                    status, name = ffmpeg_pipeline(fp_internal)

                    if status:
                        return {"success": True, "message": "Video uploaded successfully, refreshing page in 5s"}, 200
                    else:
                        return {"success": True, "message": "Video upload failed, file doesn't exist"}, 200

            elif source == "external":

                file = request.files.get('file')
                no_file = 'file' not in request.files
                filename = secure_filename(file.filename)
                this_fp = Path(join(app.config['UPLOAD_FOLDER'], filename))

                if no_file:
                    return redirect("/")

                elif file.filename == '' or not valid_filename(filename) or this_fp.exists():
                    return {"success": False, "message": "Video upload failed, invalid file type or already exists"}, 200

                elif file:
                    file.save(str(this_fp))
                    return {"success": True, "message": "Video uploaded successfully, refreshing page in 5s"}, 200

            else:
                this_fp.unlink(True)
                return {"success": False, "message": "Video upload failed, invalid file type or source"}, 200

        except(RequestEntityTooLarge):
            return {"success": False, "message": "Video is too large, >10MB"}, 200

        except(PermissionError):
            return {"success": False, "message": "Video upload failed, invalid file type or source"}, 200


# Prevent users from reading the secret credentials at /uploads/note.txt!
@app.route('/<path:any_file>', methods=["GET", "POST"], strict_slashes=False)
@app.route('/uploads/note.txt', methods=["GET", "POST"], strict_slashes=False)
def kekW_moments(any_file=None):
    return redirect(YES, code=302)
