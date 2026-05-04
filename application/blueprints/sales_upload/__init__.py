app_name = "sales_upload"
app_label = "Sales Upload"
menu_label = (app_name, f"/{app_name}", app_label)


from .views import bp
