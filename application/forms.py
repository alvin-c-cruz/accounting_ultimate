from flask_login import current_user
from application.extensions import db
from sqlalchemy import inspect
from typing import Any
from dataclasses import dataclass


@dataclass
class MyForm:
    Obj: Any
    app_name: str
    obj: Any = None

    errors = {}
    
    def __post_init__(self):
        exceptions = ['active', 'locked', 'user_id']  # Columns to exclude

        # Inspect the columns of the model object
        mapper = inspect(self.Obj().__class__)  # Get the mapper for the object's class
        columns = mapper.columns

        # Initialize form fields with appropriate types and default values
        for column in columns:
            if column.name not in exceptions:
                # Determine the type of the column and set the default value accordingly
                column_type = column.type.__class__.__name__

                if column_type == 'String':
                    # For string columns, set the default to an empty string
                    setattr(self, column.name, "")
                elif column_type == 'Integer':
                    # For integer columns, set the default to 0
                    setattr(self, column.name, 0)
                else:
                    # For other types, set to None
                    setattr(self, column.name, None)
                    
    def __str__(self):
        return getattr(self, f"{self.app_name}_name")

    def _attributes(self):
        attributes = [x for x in dir(self) if (not x.startswith("_"))]
        for i in ("errors", "Obj", "obj", "app_name"):
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

            record = self.Obj(**_dict)
            record.active = True
            record.user_id = current_user.id

            db.session.add(record)
            db.session.commit()
            
            #  TODO: Save to history

        else:
            # Update an existing record
            record = self.Obj.query.get_or_404(self.id)

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
                setattr(self, attribute, request_form.get(attribute))