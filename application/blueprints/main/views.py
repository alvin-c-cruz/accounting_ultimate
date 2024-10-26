from flask import Blueprint, render_template


bp = Blueprint("main", __name__, template_folder="pages", url_prefix="/")


@bp.route("/")
def home():
    return render_template("main/home.html")