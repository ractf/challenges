# This is a huge fucking mess of a challenge
import base64
import sqlite3
import hmac
from jwt import JWT, jwk
import json
import hashlib
from flask import Flask, render_template, request, Response, url_for, make_response, redirect

app = Flask(__name__)

JWT_SECRET = "t0ps3cr3t_JWT_t0k3n-afbyu8terg6ywfbgyUWERTFG687Y"
FLAGS = {
    "robots_flag": "ractf{1m_n0t_4_r0b0T}",
    "lfi_flag": "ractf{qu3ry5tr1ng_m4n1pul4ti0n}",
    "jwt_flag": "ractf{j4va5cr1pt_w3b_t0ken}",
    "sqli_flag": "ractf{Y0u_B3tt3r_N0t_h4v3_us3d_sqlm4p}"
}


def get_jwt():
    if "auth" not in request.cookies:
        return False
    jwt = JWT()
    try:
        if "none" not in base64.urlsafe_b64decode(request.cookies["auth"].split(".")[0] + "========").decode("utf-8").lower():
            msg = jwt.decode(request.cookies["auth"], jwk.OctetJWK(bytes(JWT_SECRET, "utf-8")))
        else:
            msg = json.loads(base64.urlsafe_b64decode(request.cookies["auth"].split(".")[1] + "========").decode("utf-8"))
    except Exception as e:
        print(e)
        return False
    return msg


def template(name, *args, **kwargs):
    if not get_jwt():
        state = {"loggedin": False, "FLAGS": FLAGS}
    else:
        state = {"loggedin": True, "user": get_jwt(), "FLAGS": FLAGS}
    return render_template(name, *args, state=state, **kwargs)


# muh robots.txt challenge
@app.route("/robots.txt")
def robots():
    return Response("User-Agent: *\nDisallow: /admin-stash", mimetype="text")


@app.route("/admin-stash")
def robots_flag():
    return FLAGS["robots_flag"]


@app.route("/admin")
def admin_flag():
    if get_jwt():
        if get_jwt()["privilege"] > 1:
            return FLAGS["jwt_flag"]
    return redirect(url_for("sign_in"))


# muh normal pages
@app.route("/")
def index():
    if get_jwt():
        return redirect(url_for("videos"))
    return template("home.html")


@app.route("/sign-up")
def sign_up():
    if get_jwt():
        return redirect(url_for("videos"))
    return template("sign_up.html")


# muh sql injection challenge
@app.route("/sign-in", methods=["GET", "POST"])
def sign_in():
    if request.method == "GET":
        if get_jwt():
            return redirect(url_for("videos"))
        else:
            return template("sign_in.html")
    if request.method == "POST":
        # Maybe use an actual db here? idk lol
        conn = sqlite3.connect(":memory:")
        c = conn.cursor()
        c.execute("CREATE TABLE users (username char, password char, privilege int)")
        c.execute("INSERT INTO users (username, password, privilege) VALUES ('Harry', 'P@ssw0rd123!s%dgyASD', 1);")
        c.execute("INSERT INTO users (username, password, privilege) VALUES ('John', 'cr1k3yth4ts4l0ngp4ss', 1);")
        c.execute("INSERT INTO users (username, password, privilege) VALUES ('Dave', 'p3rf3ct1nfr4structre', 1);")
        c.execute(f"SELECT * FROM users WHERE username = '{request.form['user']}' AND password = '{request.form['pass']}';")
        res = c.fetchall()
        if len(res) == 0:
            return template("sign_in.html", error="Invalid username / password.")
        if len(res) > 1:
            return template("sign_in.html", error="Attempting to login as more than one user!??")

        key = jwk.OctetJWK(bytes(JWT_SECRET, "utf-8"))

        jwt = JWT()
        jwt = jwt.encode({"user": res[0][0], "privilege": res[0][2]}, key, 'HS256')

        resp = make_response(redirect(url_for("videos")))
        resp.set_cookie("auth", jwt)
        return resp


# muh lfi challenge
@app.route("/videos")
def videos():
    if get_jwt():
        return template("videos.html")
    else:
        return redirect(url_for("sign_in"))


@app.route("/watch/<vid>")
def video(vid):
    if vid not in ["HMHT.mp4", "TCYI.mp4", "TIOK.mp4"]:
        # really shitty simulation of nginx firewall but doesn't matter they dont have source
        if "..%2Fetc%2Fpasswd" in request.url:
            return template("video.html", vdata=base64.b64encode(bytes(FLAGS["lfi_flag"])).decode("utf-8")) + "cm9vdDp4OjA6MDpyb290Oi9yb290Oi9iaW4vYmFzaApkYWVtb246eDoxOjE6ZGFlbW9uOi91c3Ivc2JpbjovdXNyL3NiaW4vbm9sb2dpbgpiaW46eDoyOjI6YmluOi9iaW46L3Vzci9zYmluL25vbG9naW4Kc3lzOng6MzozOnN5czovZGV2Oi91c3Ivc2Jpbi9ub2xvZ2luCnN5bmM6eDo0OjY1NTM0OnN5bmM6L2JpbjovYmluL3N5bmMKZ2FtZXM6eDo1OjYwOmdhbWVzOi91c3IvZ2FtZXM6L3Vzci9zYmluL25vbG9naW4KbWFuOng6NjoxMjptYW46L3Zhci9jYWNoZS9tYW46L3Vzci9zYmluL25vbG9naW4KbHA6eDo3Ojc6bHA6L3Zhci9zcG9vbC9scGQ6L3Vzci9zYmluL25vbG9naW4KbWFpbDp4Ojg6ODptYWlsOi92YXIvbWFpbDovdXNyL3NiaW4vbm9sb2dpbgpuZXdzOng6OTo5Om5ld3M6L3Zhci9zcG9vbC9uZXdzOi91c3Ivc2Jpbi9ub2xvZ2luCnV1Y3A6eDoxMDoxMDp1dWNwOi92YXIvc3Bvb2wvdXVjcDovdXNyL3NiaW4vbm9sb2dpbgpwcm94eTp4OjEzOjEzOnByb3h5Oi9iaW46L3Vzci9zYmluL25vbG9naW4Kd3d3LWRhdGE6eDozMzozMzp3d3ctZGF0YTovdmFyL3d3dzovdXNyL3NiaW4vbm9sb2dpbg"
        else:
            return template("video.html", error="Error opening video.")
    else:
        with open("videos/"+vid, "rb") as f:
            return template("video.html", vdata=base64.b64encode(f.read()).decode("utf-8"))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
