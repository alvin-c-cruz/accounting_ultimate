from ..extensions import package_name, package_label

app_name = package_name
app_label = package_label
menu_label = (app_name, f"/{app_name}", app_label)


from .views import bp
from .models import RawMaterial
