import os

import pytest

import activity_logger.models.org
from activity_logger import create_app, db


@pytest.fixture(scope="module")
def new_user():
    user = activity_logger.models.org.User("one@one.com", "one", "secret_password")
    return user


@pytest.fixture(scope="module")
def test_client():
    # Set the Testing configuration prior to creating the Flask application
    os.environ["CONFIG_TYPE"] = "config.TestingConfig"
    flask_app = create_app()

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!


@pytest.fixture(scope="module")
def init_database(test_client):  # pylint: disable=redefined-outer-name, unused-argument
    # Create the database and the database table
    db.create_all()

    admin_role = activity_logger.models.org.Role("Admin")
    user_role = activity_logger.models.org.Role("User")

    db.session.add(admin_role)
    db.session.add(user_role)

    db.session.commit()
    # Insert user data
    default_user = activity_logger.models.org.User(
        username="one", email="one@one.com", password="my_secret"
    )
    second_user = activity_logger.models.org.User(
        username="two", email="two@two.com", password="my_password"
    )

    default_user.role = admin_role
    second_user.role = user_role

    db.session.add(default_user)
    db.session.add(second_user)

    db.session.commit()
    # Commit the changes for the users

    yield  # this is where the testing happens!

    db.drop_all()


@pytest.fixture(scope="function")
def log_in_default_user(test_client):  # pylint: disable=redefined-outer-name
    test_client.post("/login", data={"email": "one@one.com", "password": "my_secret"})

    yield  # this is where the testing happens!

    test_client.get("/logout")


@pytest.fixture(scope="function")
def log_in_second_user(test_client):  # pylint: disable=redefined-outer-name
    test_client.post("login", data={"email": "patrick@yahoo.com", "password": "FlaskIsTheBest987"})

    yield  # this is where the testing happens!

    # Log out the user
    test_client.get("/logout")
