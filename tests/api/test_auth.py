from flaskr.db import get_db
from werkzeug.test import Client


def test_register(client: Client, app):
    response = client.post("api/auth/register", json={"username": "a", "password": "a"})
    assert response.status == "201 CREATED", "Failed to Create User"
    with app.app_context():
        assert (
            get_db()
            .execute(
                "SELECT * FROM user WHERE username = 'a'",
            )
            .fetchone()
            is not None
        )


def test_invalid_login(client: Client):
    resp = client.post("api/auth/login", json={"username": "Phil", "password": "test"})
    assert resp.get_json() == {"message": "Try again", "status": "fail"}
