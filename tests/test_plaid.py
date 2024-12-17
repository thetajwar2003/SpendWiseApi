import pytest
from unittest.mock import MagicMock


def test_create_link_token(client, mocker):
    # Mock the PlaidController's create_link_token
    mock_create_link_token = mocker.patch(
        'app.views.plaid_views.PlaidController.create_link_token')
    mock_create_link_token.return_value = "fake-link-token"

    payload = {"user_id": "test-user-id"}
    response = client.post("/plaid/create_link_token", json=payload)
    assert response.status_code == 200
    assert response.json["link_token"] == "fake-link-token"


def test_exchange_public_token(client, mocker):
    # Mock the PlaidController's exchange_public_token
    mock_exchange_token = mocker.patch(
        'app.views.plaid_views.PlaidController.exchange_public_token')
    mock_exchange_token.return_value = ("fake-access-token", "fake-item-id")

    # Mock the UserModel's update_item
    mock_update_item = mocker.patch(
        'app.models.user_model.UserModel.update_item')

    payload = {
        "public_token": "fake-public-token",
        "user_id": "test-user-id"
    }
    response = client.post("/plaid/exchange_public_token", json=payload)
    assert response.status_code == 200
    assert response.json["message"] == "Bank account linked successfully"
    assert response.json["access_token"] == "fake-access-token"


def test_get_user_bank_info(client, mocker):
    # Mock UserModel.get_user to return a valid user with access_token
    mock_get_user = mocker.patch('app.models.user_model.UserModel.get_user')
    mock_get_user.return_value = {
        "user_id": "test-user", "access_token": "fake-access-token"}

    # Mock PlaidController.get_accounts to return bank account data
    mock_get_accounts = mocker.patch(
        'app.views.plaid_views.PlaidController.get_accounts')
    mock_get_accounts.return_value = [
        {"account_id": "12345", "name": "Checking Account", "balance": 1000.0},
        {"account_id": "67890", "name": "Savings Account", "balance": 5000.0}
    ]

    # Prepare request headers and body
    headers = {"Authorization": "Bearer fake-access-token"}
    data = {"user_id": "test-user"}

    # Send POST request to the endpoint
    response = client.post("/plaid/get_user_bank_info",
                           json=data, headers=headers)

    # Assertions
    assert response.status_code == 200
    assert response.get_json() == {
        "message": "User bank information retrieved successfully",
        "accounts": [
            {"account_id": "12345", "name": "Checking Account", "balance": 1000.0},
            {"account_id": "67890", "name": "Savings Account", "balance": 5000.0}
        ]
    }

    # Ensure the mocks were called with correct arguments
    mock_get_user.assert_called_once_with("test-user")
    mock_get_accounts.assert_called_once_with("fake-access-token")
