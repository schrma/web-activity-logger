def test___dash_board___default_value___title_string_available(
    test_client, init_database
):  # pylint: disable='unused-argument'
    response = test_client.get("/dash")

    assert b"dashapp" in response.data
