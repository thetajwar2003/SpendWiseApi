def test_register_user(client, mocker):
    # Mock the register_user method in AuthController
    mock_register = mocker.patch(
        'app.views.auth_views.AuthController.register_user')
    mock_register.return_value = (
        {"message": "User registered successfully"}, 201)

    payload = {
        "email": "test@example.com",
        "password": "password123!",
        "first_name": "Test",
        "last_name": "User"
    }
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 201
    assert response.json["message"] == "User registered successfully"


def test_login_user(client, mocker):
    # Mock the login_user method in AuthController
    mock_login = mocker.patch('app.views.auth_views.AuthController.login_user')
    mock_login.return_value = ({"access_token": "fake-access-token"}, 200)

    payload = {
        "email": "test@example.com",
        "password": "password123!"
    }
    response = client.post("/auth/login", json=payload)
    assert response.status_code == 200
    assert response.json["access_token"] == "fake-access-token"
