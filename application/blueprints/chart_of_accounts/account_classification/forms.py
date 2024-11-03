from dataclasses import dataclass
from flask_login import current_user
from application.extensions import db
from .models import AccountClassification as Obj
from . import app_name


@dataclass
class Form:
    id: int = None
    account_classification_name: str = ""
    priority: str = ""

    errors = {}
    
    def __str__(self):
        return getattr(self, f"{app_name}_name")

    def _attributes(self):
        attributes = [x for x in dir(self) if (not x.startswith("_"))]
        for i in ("errors",):
            attributes.remove(i)
        return attributes

    def _populate(self, obj):
        for attribute in self._attributes():
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
                if attribute in ("priority",):
                    setattr(self, attribute, int(request_form.get(attribute)))
                else:
                    setattr(self, attribute, request_form.get(attribute))

    def _validate_on_submit(self):
        self.errors = {}

        if not self.account_classification_name:
            self.errors["account_classification_name"] = "Please type account classification name."

        if not self.priority and not self.priority == 0:
            self.errors["priority"] = "Please type order number."

        if not self.errors:
            return True
        else:
            return False    
