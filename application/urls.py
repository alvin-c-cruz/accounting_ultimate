from flask import url_for
from dataclasses import dataclass

@dataclass
class Url:
    app_name: str
    
    def home(self):
        return url_for(f'{self.app_name}.home')
    
    def add(self):
        return url_for(f"{self.app_name}.add")
    
    def edit(self, record_id):
        if record_id:
            return url_for(f"{self.app_name}.edit", record_id=record_id)

    def approve(self, record_id):
        if record_id:
            return url_for(f"{self.app_name}.approve", record_id=record_id)

    def unlock(self, record_id):
        if record_id:
            return url_for(f"{self.app_name}.unlock", record_id=record_id)

    def activate(self, record_id):
        if record_id:
            return url_for(f"{self.app_name}.activate", record_id=record_id)

    def deactivate(self, record_id):
        if record_id:
            return url_for(f"{self.app_name}.deactivate", record_id=record_id)

    def delete(self, record_id):
        if record_id:
            return url_for(f"{self.app_name}.delete", record_id=record_id)
