import requests
import time


def test_register_with_valid_data():
    resp = requests.post(
        url="http://127.0.0.1:5000/api/auth/register",
        json={"username": "someone@gmail.com", "password": "123456"},
    )
    print(resp.json())


def test_register_with_invalid_data():
    resp = requests.post(
        url="http://127.0.0.1:5000/api/auth/register",
        json={"username": "joe@gmail.com", "passwrd": "123456"},
    )
    print(resp.json())


def test_login_with_valid_data():
    resp = requests.post(
        url="http://127.0.0.1:5000/api/auth/login",
        json={"username": "joe@gmail.com", "password": "1234568"},
    )
    print(resp.json())


def test_logout_with_valid_data():
    resp = requests.post(
        url="http://127.0.0.1:5000/api/auth/login",
        json={"username": "joe@gmail.com", "password": "123456"},
    )
    token = resp.json()["auth_token"]
    time.sleep(6)
    print(resp.json())
    resp = requests.post(
        url="http://127.0.0.1:5000/api/auth/logout",
        headers={"Authorization": f"Bearer {token}"},
    )
    print(resp.json())


if __name__ == "__main__":
    test_logout_with_valid_data()
