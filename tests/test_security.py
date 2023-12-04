

def test___access_register___no_logging___not_allowed(test_client, init_database, register_a_person):  # pylint: disable='unused-argument'
    response = register_a_person # pylint: disable=pointless-statement

    assert b'Please log in to access this page.' in response.data




def test___access_register___admin_logging___ok(test_client, log_in_admin_user, register_a_person):  # pylint: disable='unused-argument'
    log_in_admin_user # pylint: disable=pointless-statement
    response = register_a_person # pylint: disable=pointless-statement

    assert b'Thanks for registering! Now you can login!' in response.data


def test___access_register___normal_logging___not_allowed(test_client, log_in_normal_user, register_a_person):  # pylint: disable='unused-argument'
    log_in_normal_user # pylint: disable='pointless-statement'
    response = register_a_person # pylint: disable=pointless-statement

    assert b'403 Access Forbidden!' in response.data

def test___access_admin___admin_logging___user_role_available(test_client, log_in_admin_user):  # pylint: disable='unused-argument'
    log_in_admin_user # pylint: disable='pointless-statement'
    response = test_client.get("/admin",follow_redirects=True)

    assert b'User' in response.data
    assert b'Role' in response.data



def test___access_addmin___normal_logging___user_role_not_available(test_client, log_in_normal_user):  # pylint: disable='unused-argument'
    log_in_normal_user # pylint: disable='pointless-statement'
    response = test_client.get("/admin",follow_redirects=True)

    assert b'Unit' in response.data
    assert b'Activities' in response.data
    assert b'Activity Type' in response.data
    assert b'User' not in response.data
    assert b'Role' not in response.data


def test___access_addmin___no_logging___user_role_not_available(test_client):  # pylint: disable='unused-argument'
    response = test_client.get("/admin",follow_redirects=True)

    assert b'Unit' not in response.data
    assert b'Activities' not in response.data
    assert b'Activity Type' not in response.data
    assert b'User' not in response.data
    assert b'Role' not in response.data
