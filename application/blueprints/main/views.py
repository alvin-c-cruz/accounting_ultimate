from flask import Blueprint, render_template, current_app, g
from .. user import login_required


bp = Blueprint('main', __name__, template_folder="pages")


@bp.route("/")
@login_required
def home():
    from application.blueprints.chart_of_accounts.account import Account
    from application.blueprints.raw_material.raw_material import RawMaterial

    modules = {
        "accounts": Account, 
        "raw_materials": RawMaterial,
    }

    context = {}
    for module_name, module in modules.items():
        context[module_name] = [record for record in getattr(module, "query").all() if not record.locked]

    return render_template("main/home.html", **context)


@bp.before_app_request
def set_g():
    g.company_name = current_app.config["COMPANY_NAME"]