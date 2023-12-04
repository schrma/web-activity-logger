import os

import pytest

import activity_logger
from activity_logger import create_app, db
from activity_logger.models.build import build_default_database


@pytest.fixture(scope="package")
def new_user():
    user = activity_logger.models.org.User("one@one.com", "one", "secret_password")
    return user


@pytest.fixture(scope="package")
def test_client():
    # Set the Testing configuration prior to creating the Flask application
    os.environ["CONFIG_TYPE"] = "config.TestingConfig"
    flask_app = create_app()

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!


@pytest.fixture(scope="package")
def init_database(test_client):  # pylint: disable=redefined-outer-name, unused-argument
    # Create the database and the database table
    db.drop_all()
    db.create_all()
    build_default_database()

    yield  # this is where the testing happens!

    db.drop_all()


@pytest.fixture(scope="function")
def log_in_admin_user(
    test_client, init_database
):  # pylint: disable=redefined-outer-name unused-argument
    response = test_client.post(
        "/login", data={"email": "one@one.com", "password": "my_secret"}, follow_redirects=True
    )

    assert b"Logged in successfully." in response.data

    yield  # this is where the testing happens!

    # Log out the user
    test_client.get("/logout")


@pytest.fixture(scope="function")
def log_in_normal_user(
    test_client, init_database
):  # pylint: disable=redefined-outer-name unused-argument
    response = test_client.post(
        "login", data={"email": "two@two.com", "password": "my_password"}, follow_redirects=True
    )

    assert b"Logged in successfully." in response.data

    yield  # this is where the testing happens!

    # Log out the user
    test_client.get("/logout")


@pytest.fixture(scope="function")
def register_a_person(
    test_client, init_database
):  # pylint: disable=redefined-outer-name unused-argument
    response = test_client.post(
        "/register",
        data={
            "email": "my@my.com",
            "username": "my",
            "password": "my_secret",
            "pass_confirm": "my_secret",
            "role": 2,
        },
        follow_redirects=True,
    )
    return response
