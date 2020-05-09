import sqlite3
import hashlib
import secrets

from flask import Flask, render_template, abort, request, send_from_directory, session, redirect, g, Response
from flask_session import Session


# xxslayer420: SlayingBeastsEveryDay
# admin: aiqB-G8Io1r_DCz74XEPTVahZZICzwOX-atAk1A7

FLAGS = [
    "ractf{d3velopersM4keM1stake5}",
    "ractf{!!!4dm1n4buse!!!}",
    "ractf{injectingSQLLikeNobody'sBusiness}"
]

DATABSE = """
CREATE TABLE users(
    username TEXT,
    password TEXT,
    algo TEXT DEFAULT "sha256",
    admin BOOLEAN DEFAULT 0
);

CREATE TABLE flags(
    flag TEXT
);

INSERT INTO users(username, password)
VALUES (
    "xxslayer420",
    "153e2d3443415c5df373b59b2ce49a8322f0729cea0fb0dd3914d24e77c40966"
);

INSERT INTO users(username, password, admin)
VALUES (
    "jimmyTehAdmin",
    "a5b2f326b9e73a5c8d320e63be1215f95605384aba6c7f121e9991aebae43e3b",
    1
);

INSERT INTO users(username, password, algo, admin)
VALUES (
    "loginToGetFlag",
    "a5b2f326b9e73a5c8d320e63be1215f95605384aba6c7f121e9991aebae43e3b",
    "none",
    0
);
INSERT INTO users(username, password)
VALUES (
    "pwnboy",
    "f90525e0a4d04fb8252f954922f89bc59bd89427e5716b5ca8137e0d20bb17c7"
);

INSERT INTO users(username, password)
VALUES (
    "3ht0n43br3m4g",
    "394f71c98c6a8fd6466128c0049922bbdd484ec680b700b45d0ae525d2f5d9cf"
);

INSERT INTO users(username, password)
VALUES (
    "pupperMaster",
    "4cb7d300fbb17acca9d5003276b6b422782585cc66d3a3d2beb82b6306dbf537"
);

INSERT INTO users(username, password)
VALUES (
    "h4tj18_8055m4n",
    "985a63e905b98ce2f92d7cf64696fb1bbaa9478cd66c47c6e44c05d320c22563"
);

INSERT INTO users(username, password)
VALUES (
    "develop",
    "b7a73c861bc86094a8a1b4984755406efd418167361deeeac47a48dde2669932"
);

"""

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = "hi"
Session(app)

import os
if os.path.exists('db.sqlite3'): os.remove('db.sqlite3')
DB = sqlite3.connect('db.sqlite3')
DB.executescript(DATABSE)
DB.close()


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(f'file:{os.path.dirname(__file__)}/db.sqlite3?mode=ro', uri=True)
        db.execute('PRAGMA soft_heap_limit=1024')
        db.execute('PRAGMA hard_heap_limit=1024')
        db.execute('PRAGMA cache_size=-512')
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        g._database = None


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        db = get_db()
        cur = db.cursor()
        ps = str(request.form.get("password"))
        ph = hashlib.sha256(ps.encode()).hexdigest()
        if request.form.get("username") == "develop":
            # Stop SQLi for develop user
            cur.execute("SELECT * FROM users WHERE password='{}' AND username='develop'".format(
                ph
            ))
        else:
            try:
                cur.execute("SELECT algo FROM users WHERE username='{}'".format(
                    request.form.get("username")
                ))
                user = cur.fetchall()
                if 'RANDOM' in ps:
                    raise ValueError
                if 'RANDOM' in str(request.form.get("username")):
                    raise ValueError
                if user and user[0][0] == 'none':
                    cur.execute("SELECT * FROM users WHERE username='{}' AND password='{}'".format(
                        request.form.get("username"), ps
                    ))
                else:
                    cur.execute("SELECT * FROM users WHERE password='{}' AND username='{}'".format(
                        ph,
                        request.form.get("username")
                    ))
            except:
                cur.fetchall()
                cur.close()
                import traceback
                return '<pre>' + traceback.format_exc() + '<pre>', 500
        user = cur.fetchall()
        cur.close()

        if not user:
            return render_template("index.html", error="Incorrect login")

        session["user"] = user[0]

    if "user" not in session:
        return render_template("index.html")

    if session["user"][0] == "develop":
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM users")
        users = cur.fetchall()
        cur.close()

        return render_template("users.html", users=users)

    flag = FLAGS[1] if session["user"][3] else None
    if session["user"][0] == "loginToGetFlag":
        flag = FLAGS[2] + " try harder for a real admin account ;)"
    resp = Response(render_template("dash.html", user=session["user"], flag=flag))
    resp.headers["X-OptionalHeader"] = "Location: /__adminPortal"
    return resp

@app.route("/logout")
def logout():
    if "user" in session:
        del session["user"]
    return redirect("/")

@app.route("/backup.txt")
def bpadd():
    return abort(403)

@app.route("/robots.txt")
def robots():
    return send_from_directory("static", "robots.txt")

@app.route("/sitemap.xml")
def sitemap():
    return send_from_directory("static", "sitemap.xml")

@app.route("/sitemap.xml.bak")
def sitemapbak():
    return send_from_directory("static", "sitemap.xml.bak")

@app.route("/_journal.txt")
def journal():
    return send_from_directory(".", "_journal.txt")

@app.route("/__adminPortal")
def adminPortal():
    if "user" not in session or not session["user"][3]:
        return redirect("/")
    return render_template("zalgo.html")

@app.route("/static")
def css():
    name = request.args.get("f")
    return send_from_directory("static", name)


if __name__ == "__main__":
    app.run(port=6969, debug=1, host="0.0.0.0")
