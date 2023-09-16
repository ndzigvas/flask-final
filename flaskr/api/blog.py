from functools import wraps

from flask import Blueprint, make_response, jsonify, request
from flaskr.models import Post, BlackJWToken
from flaskr.validations import validate_post_form
from flaskr.token import decode_auth_token

blog_blueprint = Blueprint("blogAPI", __name__, url_prefix="/api/blog")


@blog_blueprint.route("/", methods=["GET"])
def index():
    return make_response(jsonify([post for post in Post.get_all()])), 200


def auth_required(handler):
    # @wraps(handler)
    def auth(**kwargs):

        auth_header = request.headers.get("Authorization")
        if not auth_header:
            response = {
                "status": "fail",
                "message": "Authorization header not provided!",
            }
            return make_response(jsonify(response)), 400

        _, token = auth_header.split(" ")

        user_id, err = decode_auth_token(token)

        if err:
            response = {
                "status": "fail",
                "message": err,
            }
            return make_response(jsonify(response)), 400
        
        if BlackJWToken(token).is_blacklisted():
            response = {
                "status": "fail",
                "message": "Token Blacklisted",
            }
            return make_response(jsonify(response)), 400
        
        
        return handler(**kwargs, user_id=user_id)

    return auth


@blog_blueprint.route("/create", methods=["POST"])
@auth_required
def create(user_id: int):

    post_data = request.get_json()

    if err := validate_post_form(post_data):
        response = {
            "status": "fail",
            "message": err,
        }
        return make_response(jsonify(response)), 400
    
    post = Post(
        author_id=user_id,
        title=post_data["title"],
        body=post_data["body"]
    )

    post.commit()

    response = {
        "status": "success",
        "message": "Post Created",
    }
    return make_response(jsonify(response)), 201

