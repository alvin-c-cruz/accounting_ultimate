from dataclasses import dataclass
from sqlalchemy import func
from flask_login import current_user
from application.extensions import db
from .models import Account as Obj
from .. account_classification import AccountClassification
from . import app_name


@dataclass
class Form:
    id: int = None
    account_number: str = ""
    account_name: str = ""
    account_classification_id: int = None
    
    account_classification_name: str = ""

    errors = {}
    
    def __str__(self):
        return getattr(self, f"{app_name}_name")

    def _attributes(self):
        attributes = [x for x in dir(self) if (not x.startswith("_"))]
        for i in ("errors", "account_classification_name"):
            attributes.remove(i)
        return attributes

    def _populate(self, obj):
        for attribute in self._attributes():
            if attribute == "account_classification_id":
                account_classification = AccountClassification.query.get(getattr(obj, attribute))
                setattr(self, attribute, account_classification.id)
                self.account_classification_name = account_classification.account_classification_name
            else:    
                setattr(self, attribute, getattr(obj, attribute))

    def _save(self):
        if self.id is None:
            # Add a new record
            _dict = {}
            for attribute in self._attributes(): 
                _dict[attribute] = getattr(self, attribute)

            record = Obj(**_dict)
            record.active = True
            record.user_id = current_user.id

            db.session.add(record)
            db.session.commit()
            
            #  TODO: Save to history

        else:
            # Update an existing record
            record = Obj.query.get_or_404(self.id)

            if record:
                for i in self._attributes():
                    setattr(record, i, getattr(self, i))

                record.active = True
                record.user_id = current_user.id

            db.session.commit()
            
            #  TODO: Save to history

    def _post(self, request_form):
        self.id = request_form.get('record_id')
        for attribute in self._attributes():
            if attribute != "id":
                if attribute == "account_classification_id":
                    account_classification_name = request_form.get('account_classification_name')
                    account_classification = AccountClassification.query.filter_by(
                        account_classification_name=account_classification_name
                        ).first()
                    if account_classification:
                        setattr(self, attribute, account_classification.id)
                    self.account_classification_name = account_classification_name
                else:
                    setattr(self, attribute, request_form.get(attribute))

    def _validate_on_submit(self):
        self.errors = {}

        if not self.account_number:
            self.errors["account_number"] = "Please type account number."
        else:
            if not self.id:
                _existing = Obj.query.filter(Obj.account_number==self.account_number).first()
            else:
                _existing = Obj.query.filter(
                    func.lower(Obj.account_number) == func.lower(self.account_number), 
                    Obj.id != self.id
                    ).first()
                
            if _existing:
                self.errors["account_number"] = f"{self.account_number} already exists."

        if not self.account_name:
            self.errors["account_name"] = "Please type account title."
        else:
            if not self.id:
                _existing = Obj.query.filter(Obj.account_name==self.account_name).first()
            else:
                _existing = Obj.query.filter(
                    func.lower(Obj.account_name) == func.lower(self.account_name), 
                    Obj.id != self.id
                    ).first()
                
            if _existing:
                self.errors["account_name"] = f"{self.account_name} already exists."
        
        if not self.account_classification_name:
            self.errors["account_classification_name"] = "Please type account classification."
        else:
            account_classification = AccountClassification.query.filter(AccountClassification.account_classification_name==self.account_classification_name).first()
            if not account_classification:
                self.errors["account_classification_name"] = f"{self.account_classification_name} does not exists."

        if not self.errors:
            return True
        else:
            return False    
