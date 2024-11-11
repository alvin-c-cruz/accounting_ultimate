from sqlalchemy import func
from application.forms import MyForm


class Form(MyForm):
    def _validate_on_submit(self):
        self.errors = {}

        validations = [
            ("raw_material_code", "raw material code"),
            ("raw_material_name", "raw material name"),
        ]

        for attribute, label in validations:
            if not getattr(self, attribute):
                self.errors[attribute] = f"Please type {label}."
            else:
                if not self.id:
                    _dict = {attribute: getattr(self, attribute)}
                    _existing = self.Obj.query.filter_by(**_dict).first()
                else:
                    _existing = self.Obj.query.filter(
                        func.lower(getattr(self.Obj, attribute)) == func.lower(getattr(self, attribute)), 
                        self.Obj.id != self.id
                        ).first()
                    
                if _existing:
                    self.errors[attribute] = f"{getattr(self, attribute)} already exists."
        
        if not self.errors:
            return True
        else:
            return False
