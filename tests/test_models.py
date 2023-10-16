
def test___check_user___with_user_and_email___correct_result(new_user):
    assert new_user.email == "one@one.com"
    assert new_user.username == "one"
    assert new_user.__repr__() ==  f"UserName: {new_user.username}"

def test___check_user___password___check_password_equals_true(new_user):
    assert new_user.check_password("secret_password")

def test___check_user___password___check_password_equals_false(new_user):
    assert not new_user.check_password("false_password")
