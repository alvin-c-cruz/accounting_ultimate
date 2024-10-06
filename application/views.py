from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, jsonify, render_template, redirect, url_for
from flask.views import MethodView
from application import db
from application.models import User

class UserAPI(MethodView):
    def get(self):
        # Render the HTML form for user creation
        return render_template('user_form.html')

    def post(self):
        # Handle form submission and user creation
        username = request.form.get('username')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        middle_name = request.form.get('middle_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')

        # Validate that the required fields are filled
        if not username or not email:
            return jsonify({'error': 'Username and email are required.'}), 400

        # Hash the password before saving it
        hashed_password = generate_password_hash(password)

        # Create a new user instance
        user = User(
            username=username,
            password=hashed_password,  # Store hashed password
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            email=email
        )

        # Save the user to the database
        db.session.add(user)
        db.session.commit()

        # Redirect to a success page or show a success message
        return redirect(url_for('users.user_created', username=username))

    def put(self, username):
        # Handle user update
        user = User.query.filter_by(username=username).first()

        if not user:
            return jsonify({'error': 'User not found.'}), 404

        # Get updated fields
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        middle_name = request.form.get('middle_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')

        # Update user information
        if password:
            user.password = generate_password_hash(password)
        if first_name:
            user.first_name = first_name
        if middle_name:
            user.middle_name = middle_name
        if last_name:
            user.last_name = last_name
        if email:
            user.email = email

        # Save updates to the database
        db.session.commit()

        return jsonify({'message': 'User updated successfully.'}), 200

    def delete(self, username):
        # Handle user deletion
        user = User.query.filter_by(username=username).first()

        if not user:
            return jsonify({'error': 'User not found.'}), 404

        # Delete the user
        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'User deleted successfully.'}), 200
