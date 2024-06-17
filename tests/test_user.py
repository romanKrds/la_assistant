def test_get_user_info(client, auth):
    response = client.get('/user/info')

    assert response.status_code == 401

    auth.login()

    with client:
        response = client.get('/user/info')

        assert response.status_code == 200
        assert response.json == {"id": 1, "username": "test"}

