app_name = "account_classification"
app_label = "Account Classification"
menu_label = (app_name, f"/{app_name}", app_label)


from .views import bp
from .models import AccountClassification
