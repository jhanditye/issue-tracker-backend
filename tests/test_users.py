from fastapi import HTTPException
import pytest
from app.oauth2 import create_access_token, get_current_user, verify_access_token
from jose import JWTError

@pytest.mark.parametrize(
    "user_data,expected_status",
    [
        ({"email": "testuser@example.com", "password": "securePass123"}, 201),
        ({"email": "invalidemail", "password": "somePassword123"}, 422),
        ({"email": "testuser2@example.com", "password": ""}, 422),
    ],
)
def test_create_user(client, user_data, expected_status):
    response = client.post("/users/", json=user_data)
    assert response.status_code == expected_status

def test_create_user_duplicate_email(client, test_user):
    user_data = {"email": test_user["email"], "password": "anotherPass123"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 400

@pytest.mark.parametrize(
    "login_data,expected_status",
    [
        ({"username": "jane.doe@example.com", "password": "securePassw0rd!"}, 200),
        ({"username": "nonexistent@example.com", "password": "randomPass123"}, 403),
        ({"username": "jane.doe@example.com", "password": "wrongPassword"}, 403),
        ({"username": "invalidemail", "password": "somePassword123"}, 422),
    ],
)
def test_login(client, login_data, expected_status, test_user):
    response = client.post("/login", data=login_data)
    assert response.status_code == expected_status

def test_verify_valid_access_token(test_user):
    token = create_access_token({"user_id": test_user["id"]})
    token_data = verify_access_token(token)
    assert token_data.id == test_user["id"]

def test_verify_invalid_access_token():
    with pytest.raises(JWTError):
        verify_access_token("invalid_token")

def test_get_valid_current_user(token, test_user):
    user = get_current_user(token)
    assert user["id"] == test_user["id"]

def test_get_invalid_current_user():
    with pytest.raises(HTTPException) as exception_info:
        get_current_user("invalid_token")
    assert exception_info.value.status_code == 401
