import requests
import time


def test_get_all_posts():
    resp = requests.get(
        url="http://127.0.0.1:5000/api/blog",
    )
    print(resp.json())


def test_create_new_post():
    resp = requests.post(
        url="http://127.0.0.1:5000/api/auth/login",
        json={"username": "joe@gmail.com", "password": "123456"},
    )
    token = resp.json()["auth_token"]

    data = {"title": "Hi Students", "body": "via API"}
    resp = requests.post(
        url="http://127.0.0.1:5000/api/blog/create",
        json=data,
        headers={"Authorization": f"Bearer {token}"},
    )

    print(resp.json())


def test_update_post_with_timeout():
    resp = requests.post(
        url="http://127.0.0.1:5000/api/auth/login",
        json={"username": "joe@gmail.com", "password": "123456"},
    )
    token = resp.json()["auth_token"]
    time.sleep(6)
    data = {"title": "updated Hello REST", "body": "via API"}
    resp = requests.post(
        url="http://127.0.0.1:5000/api/blog/update/3",
        json=data,
        headers={"Authorization": f"Bearer {token}"},
    )

    print(resp.json())


def test_update_post_with_logout():
    resp = requests.post(
        url="http://127.0.0.1:5000/api/auth/login",
        json={"username": "joe@gmail.com", "password": "123456"},
    )
    token = resp.json()["auth_token"]
    resp = requests.post(
        url="http://127.0.0.1:5000/api/auth/logout",
        headers={"Authorization": f"Bearer {token}"},
    )

    data = {"title": "updated Hello REST", "body": "via API"}
    resp = requests.post(
        url="http://127.0.0.1:5000/api/blog/update/3",
        json=data,
        headers={"Authorization": f"Bearer {token}"},
    )

    print(resp.json())


if __name__ == "__main__":
    test_create_new_post()
