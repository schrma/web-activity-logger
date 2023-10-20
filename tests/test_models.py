import pytest

import activity_logger


def test___check_user___with_user_and_email___correct_result(new_user):
    assert new_user.email == "one@one.com"
    assert new_user.username == "one"
    assert new_user.__repr__() == new_user.username  # pylint: disable=unnecessary-dunder-call


def test___check_user___password___check_password_equals_true(new_user):
    assert new_user.check_password("secret_password")


def test___check_user___password___check_password_equals_false(new_user):
    assert not new_user.check_password("false_password")


def test___init_user___email_as_number___raise_error():
    with pytest.raises(TypeError):
        activity_logger.models.User()  # pylint: disable=no-value-for-parameter
