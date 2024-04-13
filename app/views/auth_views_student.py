from flask import request, jsonify, Blueprint
from flask_jwt_extended import get_jwt_identity, set_access_cookies, get_jwt, unset_jwt_cookies, jwt_required
from datetime import datetime, timedelta
from app.models.auth_models_student import AuthStudent


auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.after_app_request
def refresh(response):
    """Check JWT status. If token expiration imminent, refresh token."""
    try:
        expiry = get_jwt()["exp"]
        now = datetime.now()
        timestamp = datetime.timestamp(now + timedelta(seconds=8))
        if timestamp > expiry:
            access_token = AuthStudent.refresh_jwt_token(get_jwt_identity)
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response
@auth_blueprint.route("/api/auth/register", methods=["POST"])
def register():
    """Register a new auth student"""
    data = request.json
    try:
        email = data["email"]
        password = data["password"]
        student = AuthStudent(email=email, password=password)

        db_insertion_attempt = student.add_student()
        if db_insertion_attempt:
            token = student.create_jwt_token()

            success_msg = "Registration successful"
            resp = jsonify(msg=success_msg, status=201)
            set_access_cookies(resp, token)

            return resp, 201
        else:
            error_msg = "Something went wrong."
            return jsonify(msg=error_msg, status=400), 400
    except KeyError:
        error_msg = "Please provide both an email and a password."
        return jsonify(msg=error_msg, status=400), 400


@auth_blueprint.route("/api/auth/login", methods=["POST"])
def login():
    """Logs an authenticated student into the API."""

    data = request.json
    try:
        email = data["email"]
        password = data["password"]

        student = AuthStudent(email, password)
        retrieved_auth_student = student.get_student(password)

        if isinstance(retrieved_auth_student, AuthStudent):
            token = student.create_jwt_token()
            success_msg = "Login successful."
            resp = jsonify(msg=success_msg, status=200)

            set_access_cookies(resp, token)
            return resp, 200
        elif retrieved_auth_student == "not found":
            error_msg = "Email not found. Please try again."
            return jsonify(msg=error_msg, status=400)

        else:
            error_msg = "Incorrect password. Please try again."
            return jsonify(msg=error_msg, status=400)

    except KeyError:
        error_msg = "Please authenticate."
        return jsonify(msg=error_msg, status=400)

@auth_blueprint.route("/api/auth/logout", methods=["POST"])
def logout():
    """Logs out the student by clearing the JWT token"""
    resp = jsonify(msg="Logout successful")
    unset_jwt_cookies(resp)
    return resp, 200
