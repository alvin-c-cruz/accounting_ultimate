from application.extensions import db
from . import app_name


class RawMaterial(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    raw_material_name = db.Column(db.String())
    raw_material_code = db.Column(db.String())

    active = db.Column(db.Boolean())
    locked = db.Column(db.Boolean())
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    user = db.relationship('User', backref=f'{app_name}s', lazy=True)


    def __str__(self):
        return f"{self.raw_material_code}: {self.raw_material_name}"
    
    def options(self):
        _options = [
            {"id": record.id, "dropdown_name": f"{record.raw_material_code}: {record.raw_material_name}"} 
            for record in self.query.order_by("raw_material_code").all() 
            if record.active
            ]
        return _options
