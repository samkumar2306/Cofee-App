from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.services.student_service import StudentService

student_bp = Blueprint("student", __name__)


@student_bp.route("/", methods=["POST"])
@jwt_required()
def create_student():

    data = request.get_json()

    response, status = StudentService.create(data)

    return jsonify(response), status


@student_bp.route("/", methods=["GET"])
@jwt_required()
def get_students():

    response, status = StudentService.get_all()

    return jsonify(response), status


@student_bp.route("/<user_id>", methods=["GET"])
@jwt_required()
def get_student(user_id):

    response, status = StudentService.get_by_id(user_id)

    return jsonify(response), status


@student_bp.route("/<user_id>", methods=["PUT"])
@jwt_required()
def update_student(user_id):

    data = request.get_json()

    response, status = StudentService.update(user_id, data)

    return jsonify(response), status


@student_bp.route("/<user_id>", methods=["DELETE"])
@jwt_required()
def delete_student(user_id):

    response, status = StudentService.delete(user_id)

    return jsonify(response), status