import pytest
from application import create_app, db
import os

# Move test database cleanup to a separate fixture for clarity
@pytest.fixture(scope='module')
def init_database():
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield db  # Provide the database session to tests
        db.session.remove()
        db.drop_all()

    # After all tests, delete the test.db file if it exists
    test_db_path = 'test.db'
    if os.path.exists(test_db_path):
        os.remove(test_db_path)


@pytest.fixture(scope='module')
def client(init_database):
    app = create_app('testing')
    client = app.test_client()
    
    with app.app_context():
        yield client  # Provide the test client to the tests
