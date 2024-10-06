import pytest
from werkzeug.security import check_password_hash, generate_password_hash
from application import db
from .. models import User

@pytest.fixture(scope='module')
def new_user():
    """Fixture to create a new user instance for testing."""
    user = User(
        username='testuser',
        password=generate_password_hash('pass_word'),  # This will be hashed when saved to the database
        first_name='First',
        middle_name='Middle',
        last_name='Last',
        email='testuser@example.com'
    )
    return user

def test_create_user(new_user):
    """Test creating a new User instance."""
    assert new_user.username == 'testuser'
    assert check_password_hash(new_user.password, 'pass_word')
    assert new_user.first_name == 'First'
    assert new_user.middle_name == 'Middle'
    assert new_user.last_name == 'Last'
    assert new_user.email == 'testuser@example.com'

def test_repr(new_user):
    """Test the __repr__ method of the User model."""
    assert repr(new_user) == '<User testuser>'

def test_add_user_to_db(client, new_user):
    """Test adding a user to the database and checking hashed password."""
    with client.application.app_context():
        db.session.add(new_user)
        db.session.commit()
        
        # Retrieve the user from the database
        saved_user = User.query.filter_by(username='testuser').first()
        assert saved_user is not None
        assert saved_user.username == 'testuser'
        assert saved_user.first_name == 'First'
        assert saved_user.email == 'testuser@example.com'
        
        # Verify that the password is hashed
        assert saved_user.password != 'pass_word'  # Ensure the password is not stored as plain text
        
        # Verify the password hash is correct
        assert check_password_hash(saved_user.password, 'pass_word')  # Compare the raw password with the hash

def test_update_user_in_db(client, new_user):
    """Test updating a user in the database."""
    with client.application.app_context():
        # Retrieve user
        user = User.query.filter_by(username=new_user.username).first()
        user.password = generate_password_hash('updatepassword')
        user.first_name = 'OldFirst'
        user.middle_name = 'OldMiddle'
        user.last_name = 'OldLast'
        user.email = 'update@example.com'
        
        db.session.commit()

        # Retrieve the user and update fields
        saved_user = User.query.filter_by(username=new_user.username).first()
        assert saved_user is not None

        # Update the user's fields
        saved_user.first_name = 'NewFirst'
        saved_user.middle_name = 'NewMiddle'
        saved_user.last_name = 'NewLast'
        saved_user.email = 'newupdate@example.com'
        db.session.commit()

        # Retrieve the updated user and verify the changes
        updated_user = User.query.filter_by(username=new_user.username).first()
        assert updated_user.first_name == 'NewFirst'
        assert updated_user.middle_name == 'NewMiddle'
        assert updated_user.last_name == 'NewLast'
        assert updated_user.email == 'newupdate@example.com'

        # Ensure username and password have not been changed
        assert updated_user.username == new_user.username
        # Check that the password hasn't changed
        assert check_password_hash(updated_user.password, 'updatepassword')

def test_delete_user_from_db(client):
    """Test deleting a user from the database."""
    with client.application.app_context():
        # Create and add a user
        user = User(
            username='deleteuser',
            password='deletepassword',
            first_name='Delete',
            middle_name='User',
            last_name='Last',
            email='delete@example.com'
        )
        db.session.add(user)
        db.session.commit()

        # Ensure the user was added
        saved_user = User.query.filter_by(username='deleteuser').first()
        assert saved_user is not None
        
        # Delete the user
        db.session.delete(saved_user)
        db.session.commit()

        # Verify the user is deleted
        deleted_user = User.query.filter_by(username='deleteuser').first()
        assert deleted_user is None
