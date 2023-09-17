from werkzeug.test import Client


def test_create_new_post(client: Client):
    resp = client.post("api/auth/login", json={"username": "test", "password": "test"})

    token = resp.get_json()["auth_token"]

    data = {"title": "Hello REST", "body": "via API"}
    resp = client.post(
        "api/blog/create",
        json=data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status == "201 CREATED", "Failed to Create Post"
