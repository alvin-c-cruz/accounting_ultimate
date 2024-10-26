from flask import Blueprint
from .views import UserView

# Define the blueprint with the URL prefix "/user"
bp = Blueprint('users', __name__, url_prefix="/user", template_folder="pages")

# Register the class-based view for /user URL to handle GET (form) and POST (creation)
bp.add_url_rule('/user/create', view_func=UserView.as_view('create_user'), methods=['GET', 'POST'])

# Route for updating a user (PUT method)
bp.add_url_rule('/user/update/<username>', view_func=UserView.as_view('update_user'), methods=['PUT'])

# Route for deleting a user (DELETE method)
bp.add_url_rule('/user/delete/<username>', view_func=UserView.as_view('delete_user'), methods=['DELETE'])

# Define a success route for after user creation
@bp.route('/created/<username>')
def user_created(username):
    return f"<h1>User '{username}' was successfully created!</h1>"

