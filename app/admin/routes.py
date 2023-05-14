from flask import render_template
from .. import app, db, UserModel


@app.route("/admin")
def admin():
    return render_template("index.html")
