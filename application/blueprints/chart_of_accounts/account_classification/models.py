from application.extensions import db
from . import app_name


class AccountClassification(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    account_classification_name = db.Column(db.String(255))
    priority = db.Column(db.Integer())
    active = db.Column(db.Boolean())
    locked = db.Column(db.Boolean())
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    user = db.relationship('User', backref=f'{app_name}s', lazy=True)

    def __str__(self):
        return getattr(self, f"{app_name}_name")
    
    def options(self):
        _options = [(record.id, getattr(record, f"{app_name}_name")) for record in self.query.order_by("priority").all() if record.active]
        return _options
