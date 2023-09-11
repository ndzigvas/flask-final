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

    data = {"title": "Hello REST", "body": "via API"}
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

def test_delete_post():
    # Register:
    resp = requests.post(
        url="http://127.0.0.1:5000/api/auth/register",
        json={"username": "joe@gmail.com", "password": "123456"},
    )

    print(f"register: {resp.status_code}")

    # Login:
    resp = requests.post(
        url="http://127.0.0.1:5000/api/auth/login",
        json={"username": "joe@gmail.com", "password": "123456"},
    )

    print(f"login: {resp.status_code}")
    token = resp.json().get("auth_token")

    # Create new post:
    data = {"title": "My title", "body": "My text"}
    resp = requests.post(
        url="http://127.0.0.1:5000/api/blog/create",
        json=data,
        headers={"Authorization": f"Bearer {token}"},
    )

    print(f"create new post: {resp.status_code}")
    post_id = resp.json().get("post", {}).get("id")

    # Delete created post:
    resp = requests.delete(
        url=f"http://127.0.0.1:5000/api/blog/delete/{post_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    print(f"delete the post: {resp.status_code}")

    # Get deleted post:
    resp = requests.get(
        url=f"http://127.0.0.1:5000/api/blog/{post_id}",
    )

    print(f"get deleted post: {resp.status_code}")
    if resp.status_code == 404:
        print("Post not found.")

if __name__ == "__main__":
    # test_get_all_posts()
    # test_update_post_with_timeout()
    # test_create_new_post()
    test_update_post_with_logout()
    test_delete_post()
