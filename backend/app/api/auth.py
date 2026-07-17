from flask import Blueprint, jsonify, request

from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    response, status_code = AuthService.register(data)

    return jsonify(response), status_code

@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    response, status = AuthService.login(data)

    return jsonify(response), status

@auth_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():

    user_id = get_jwt_identity()

    data = request.get_json()

    response, status = AuthService.update_profile(user_id, data)

    return jsonify(response), status

@auth_bp.route("/change-password", methods=["PUT"])
@jwt_required()
def change_password():

    user_id = get_jwt_identity()

    data = request.get_json()

    response, status = AuthService.change_password(user_id, data)

    return jsonify(response), status


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():

    user_id = get_jwt_identity()

    response, status = AuthService.me(user_id)

    return jsonify(response), status
