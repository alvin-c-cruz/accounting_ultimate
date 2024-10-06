from flask import Blueprint
from .views import UserView

users_bp = Blueprint('users', __name__, url_prefix="/user")

# Register the class-based view for /user URL to handle GET (form) and POST (creation)
users_bp.add_url_rule('/user/create', view_func=UserView.as_view('create_user'), methods=['GET', 'POST'])

# Route for updating a user (PUT method)
users_bp.add_url_rule('/user/update/<username>', view_func=UserView.as_view('update_user'), methods=['PUT'])

# Route for deleting a user (DELETE method)
users_bp.add_url_rule('/user/delete/<username>', view_func=UserView.as_view('delete_user'), methods=['DELETE'])

# Define a success route for after user creation
@users_bp.route('/created/<username>')
def user_created(username):
    return f"<h1>User '{username}' was successfully created!</h1>"
