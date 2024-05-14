from flask import render_template, request, redirect, url_for, Blueprint

bp = Blueprint("main", __name__)


@bp.route("/")
def redirect_home():
    return redirect("/home")


@bp.route("/home")
def home():
    return render_template("home.html")


@bp.route("/calculate", methods=["GET", "POST"])
def calculate():
    if request.method == "POST":
        return redirect(url_for())
    return render_template("calculate.html")


@bp.route("/about")
def about():
    return render_template("about.html")


@bp.route("/history")
def contact():
    return render_template("history.html")
