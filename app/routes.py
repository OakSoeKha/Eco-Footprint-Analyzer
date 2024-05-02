from flask import render_template, request, redirect, url_for
from app import app


@app.route("/")
def redirect_home():
    return redirect("/home")


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/calculate", methods=["GET", "POST"])
def calculate():
    if request.method == "POST":
        pass
    return render_template("calculate.html")


@app.route("/about")
def about():
    pass


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        pass
    return render_template("contact.html")
