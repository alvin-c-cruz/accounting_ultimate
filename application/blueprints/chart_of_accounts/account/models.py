from application.extensions import db
from . import app_name


class Account(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    account_number = db.Column(db.String(255))
    account_name = db.Column(db.String(255))

    account_classification_id = db.Column(db.Integer, db.ForeignKey('account_classification.id'), nullable=True)
    account_classification = db.relationship('AccountClassification', backref=f'{app_name}s', lazy=True)

    active = db.Column(db.Boolean())
    locked = db.Column(db.Boolean())
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    user = db.relationship('User', backref=f'{app_name}s', lazy=True)


    def __str__(self):
        return f"{self.account_number}: {self.account_name}"
    
    def options(self):
        _options = [
            {"id": record.id, "dropdown_name": f"{record.account_number}: {record.account_name}"} 
            for record in self.query.order_by("account_number").all() 
            if record.active
            ]
        return _options
