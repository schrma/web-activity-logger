def test___view_login____just_page___correct_response(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get("/login")
    assert response.status_code == 200
    assert b"Email" in response.data
    assert b"Password" in response.data


def test___valid_login_logout___with_user___login_accepted(
    test_client,
):  # pylint: disable=unused-argument
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is posted to (POST)
    THEN check the response is valid
    """
    response = test_client.post(
        "/login", data={"email": "one@one.com", "password": "my_secret"}, follow_redirects=True
    )
    print(response.data)
    assert response.status_code == 200

    response = test_client.get("/logout", follow_redirects=True)
    assert response.status_code == 200


def test___valid_login_logout___with_incorrect_user___login_not_accepted(
    test_client,
):  # pylint: disable=unused-argument
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is posted to (POST)
    THEN check the response is valid
    """
    response = test_client.post(
        "/login", data={"email": "one@one.com", "password": "false_secret"}, follow_redirects=True
    )
    assert response.status_code == 200


def test___check_activitytype___default_values___correct_results(test_client):
    response = test_client.get("/admin/activitytype/")
    assert response.status_code == 200
    assert b"Jogging" in response.data
    assert b"Pushup" in response.data


def test___check_activities___default_values___correct_results(test_client):
    response = test_client.get("/admin/activities/")
    assert response.status_code == 200
    assert b"Jogging" in response.data
    assert b"Pushup" in response.data
    assert b"11.11" in response.data
    assert b"12.22" in response.data
    assert b"13.33" in response.data
    assert b"14.44" in response.data
