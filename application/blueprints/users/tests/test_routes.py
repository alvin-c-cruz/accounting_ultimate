from .. models import User, db


def test_create_user(client):
    """Test creating a user via the POST request."""
    response = client.post('/user/create', data={
        'username': 'testuser',
        'password': 'pass_word',
        'confirm_password': 'pass_word',
        'first_name': 'firstname',
        'middle_name': 'middlename',
        'last_name': 'lastname',
        'email': 'test@example.com',
    })
       
    # Check if the response indicates a redirect (302) after successful creation
    assert response.status_code == 302
    
    # Follow the redirect to verify success page or final response
    follow_response = client.get(response.headers['Location'])
    assert follow_response.status_code == 200
    assert b"User 'testuser' was successfully created!" in follow_response.data

    # Check if the user is actually in the database
    created_user = User.query.filter_by(username='testuser').first()
    assert created_user is not None
    assert created_user.username == 'testuser'
    assert created_user.email == 'test@example.com'


def test_read_user(client):
    """Test retrieving a user."""
    # Create a new user in the database for testing the read operation
    response = client.post('/user/create', data={
        'username': 'readuser',
        'password': 'readpassword',
        'confirm_password': 'readpassword',
        'first_name': 'Read',
        'middle_name': 'User',
        'last_name': 'Lastname',
        'email': 'readuser@example.com',
    })
    
    assert response.status_code == 302  # Confirm redirection after creation
    
    # Follow the redirect to ensure the user was created successfully
    follow_response = client.get(response.headers['Location'])
    assert follow_response.status_code == 200

    # Retrieve the user and verify the user exists
    retrieved_user = User.query.filter_by(username='readuser').first()
    assert retrieved_user is not None
    assert retrieved_user.username == 'readuser'
    assert retrieved_user.email == 'readuser@example.com'


def test_update_user(client):
    """Test updating a user's information."""
    # First, create a user
    user = User(username='updateuser', password='updatepassword', email='updateuser@example.com')
    db.session.add(user)
    db.session.commit()

    # Update the user via a PUT request
    response = client.put(f'/user/update/{user.username}', data={
        'password': 'new_password',  # New password
        'confirm_password': 'new_password',
        'first_name': 'UpdatedFirst',
        'middle_name': 'UpdatedMiddle',
        'last_name': 'UpdatedLast',
        'email': 'newupdate@example.com',  # Updated email
    })
    
    assert response.status_code == 200  # Check success

    # Verify the updated information by querying the database
    updated_user = User.query.filter_by(username='updateuser').first()
    assert updated_user is not None
    assert updated_user.first_name == 'UpdatedFirst'
    assert updated_user.middle_name == 'UpdatedMiddle'
    assert updated_user.last_name == 'UpdatedLast'
    assert updated_user.email == 'newupdate@example.com'

    # Ensure the password has been updated (hashed)
    from werkzeug.security import check_password_hash
    assert check_password_hash(updated_user.password, 'new_password')


def test_delete_user(client):
    """Test deleting a user."""
    # First, create a user to delete
    user = User(username='deleteuser', password='deletepassword', email='deleteuser@example.com')
    db.session.add(user)
    db.session.commit()

    # Delete the user via a DELETE request
    response = client.delete(f'/user/delete/{user.username}')
    assert response.status_code == 200  # Check success
    
    # Verify the user no longer exists in the database
    deleted_user = User.query.filter_by(username='deleteuser').first()
    assert deleted_user is None