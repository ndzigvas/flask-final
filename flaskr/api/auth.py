from flask import Blueprint, make_response, jsonify, request

from flaskr.validations import validate_auth_form
from flaskr.models import User, BlackJWToken
from flaskr.token import encode_auth_token, decode_auth_token

auth_blueprint = Blueprint("authAPI", __name__, url_prefix="/api/auth")


@auth_blueprint.route("/register", methods=["POST"])
def register():
    post_data = request.get_json()

    if err := validate_auth_form(post_data):
        response = {"status": "fail", "message": err}
        return make_response(jsonify(response)), 400

    if err := User.from_post_data(post_data).commit():
        response = {"status": "fail", "message": err}
        return make_response(jsonify(response)), 418

    response = {
        "status": "Success",
        "message": "Successfully Registered. Please Log in!",
    }

    return make_response(jsonify(response)), 201


@auth_blueprint.route("/login", methods=["POST"])
def login():
    post_data = request.get_json()

    if err := validate_auth_form(post_data):
        response = {"status": "fail", "message": err}
        return make_response(jsonify(response)), 400

    if user := User.get_one(post_data):
        auth_token = encode_auth_token(user.id)
        response = {
            "status": "success",
            "message": "Successfully logged in",
            "auth_token": auth_token,
        }
        return make_response(jsonify(response)), 200

    else:
        response = {
            "status": "fail",
            "message": "Try again",
        }
        return make_response(jsonify(response)), 401


@auth_blueprint.route("/logout", methods=["POST"])
def logout():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        response = {
            "status": "fail",
            "message": "Authorization header not provided!",
        }
        return make_response(jsonify(response)), 400

    _, token = auth_header.split(" ")

    _, err = decode_auth_token(token)

    if err:
        response = {
            "status": "fail",
            "message": err,
        }
        return make_response(jsonify(response)), 400

    BlackJWToken(token).commit()

    response = {
        "status": "succes",
        "message": "Successfully logged out",
    }

    return make_response(jsonify(response)), 200
