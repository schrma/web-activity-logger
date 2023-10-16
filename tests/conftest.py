"""
    Dummy conftest.py for activity_logger.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html
"""

import pytest
import activity_logger.models


@pytest.fixture(scope='module')
def new_user():
    user = activity_logger.models.User('one@one.com', 'one', 'secret_password')
    return user
