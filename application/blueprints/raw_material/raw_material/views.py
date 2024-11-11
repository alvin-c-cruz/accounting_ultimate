from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError
from .forms import Form
from .models import RawMaterial as Obj
from ... user import login_required, roles_accepted
from flask_login import current_user
from application.urls import Url
from application.extensions import db

from . import app_name, app_label


bp = Blueprint(app_name, __name__, template_folder="pages", url_prefix=f"/{app_name}")
ROLES_ACCEPTED = app_label


@bp.route("/", methods=["GET", "POST"])
@login_required
@roles_accepted([ROLES_ACCEPTED])
def home():
    rows = Obj.query.order_by(getattr(Obj, "raw_material_code")).all()

    context = {
        "app_label": app_label,
        "rows": rows,
        "url": Url(app_name=app_name),
    }

    return render_template(f"{app_name}/home.html", **context)


@bp.route("/add", methods=["POST", "GET"])
@login_required
@roles_accepted([ROLES_ACCEPTED])
def add():
    form = Form(Obj=Obj, app_name=app_name)
    if request.method == "POST":
        form._post(request.form)
        if form._validate_on_submit():
            form._save()
            flash(f"Saved {form}.", category="success")
            return redirect(url_for(f'{app_name}.home'))

    context = {
        "app_label": app_label,
        "form": form,
        "url": Url(app_name=app_name),
    }

    return render_template(f"{app_name}/form.html", **context)


@bp.route(f"/edit/<int:record_id>", methods=["POST", "GET"])
@login_required
@roles_accepted([ROLES_ACCEPTED])
def edit(record_id):
    form = Form(Obj=Obj, app_name=app_name)   
    if request.method == "POST":
        form._post(request.form)

        if form._validate_on_submit():
            form._save()
            flash(f"Updated {form}.", category="success")
            return redirect(url_for(f'{app_name}.home'))

    else:
        obj = Obj.query.get(record_id)
        form._populate(obj)

    context = {
        "app_label": app_label,
        "form": form,
        "url": Url(app_name=app_name),
    }

    return render_template(f"{app_name}/form.html", **context)


@bp.route("/delete/<int:record_id>", methods=["POST", "GET"])
@login_required
@roles_accepted([ROLES_ACCEPTED])
def delete(record_id):   
    obj = Obj.query.get_or_404(record_id)
    try:
        db.session.delete(obj)
        db.session.commit()
        flash(f"{obj} has been deleted.", category="success")
    except IntegrityError:
        db.session.rollback()
        flash(f"Cannot delete {obj} because it has related records.", category="error")

    return redirect(url_for(f'{app_name}.home'))


@bp.route("/approve/<int:record_id>", methods=['GET'])
@login_required
@roles_accepted([ROLES_ACCEPTED])
def approve(record_id):
    if not current_user.admin:
        flash("Administrator rights required.", category="error")
        return redirect(url_for(f"{app_name}.home"))
    
    obj = Obj.query.get_or_404(record_id)
    obj.locked = True

    db.session.commit()

    flash(f"Approved: {obj}", category="success")
    return redirect(url_for(f'{app_name}.home'))   
    

@bp.route("/activate/<int:record_id>", methods=["POST", "GET"])
@login_required
@roles_accepted([ROLES_ACCEPTED])
def activate(record_id): 
    if not current_user.admin:
        flash("Administrator rights required.", category="error")
        return redirect(url_for(f"{app_name}.home"))
      
    obj = Obj.query.get_or_404(record_id)
    obj.active = True    

    db.session.commit()

    flash(f"{obj} has been activated.", category="error")

    return redirect(url_for(f'{app_name}.home'))


@bp.route("/deactivate/<int:record_id>", methods=["POST", "GET"])
@login_required
@roles_accepted([ROLES_ACCEPTED])
def deactivate(record_id):   
    if not current_user.admin:
        flash("Administrator rights required.", category="error")
        return redirect(url_for(f"{app_name}.home"))

    obj = Obj.query.get_or_404(record_id)
    obj.active = False    

    db.session.commit()

    flash(f"{obj} has been deactivated.", category="error")

    return redirect(url_for(f'{app_name}.home'))


@bp.route("/unlock/<int:record_id>", methods=['GET'])
@login_required
@roles_accepted([ROLES_ACCEPTED])
def unlock(record_id):
    if not current_user.admin:
        flash("Administrator rights required.", category="error")
        redirect(url_for(f'{app_name}.home'))
    
    obj = Obj.query.get_or_404(record_id)
    obj.locked = False

    db.session.commit()

    flash(f"Unlocked: {obj}", category="error")
    return redirect(url_for(f'{app_name}.home'))   
