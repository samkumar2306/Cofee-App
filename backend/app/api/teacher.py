from flask import Blueprint, request

from app.services.teacher_service import TeacherService
from flask_jwt_extended import jwt_required
from app.decorators.roles import roles_required
from app.utils.enums import UserRole

teacher_bp = Blueprint("teacher", __name__, url_prefix="/api/teachers")


@teacher_bp.route("", methods=["POST"])
@jwt_required()
#@roles_required(UserRole.ADMIN)
def create_teacher():
    data = request.get_json()
    return TeacherService.create(data)


@teacher_bp.route("", methods=["GET"])
@jwt_required()
def get_all_teachers():
    return TeacherService.get_all()


@teacher_bp.route("/<uuid:teacher_id>", methods=["GET"])
@jwt_required()
def get_teacher(teacher_id):
    return TeacherService.get_by_id(teacher_id)


@teacher_bp.route("/<uuid:teacher_id>", methods=["PUT"])
@jwt_required()
@roles_required(UserRole.ADMIN)
def update_teacher(teacher_id):
    data = request.get_json()
    return TeacherService.update(teacher_id, data)


@teacher_bp.route("/<uuid:teacher_id>", methods=["DELETE"])
@jwt_required()
@roles_required(UserRole.ADMIN)
def delete_teacher(teacher_id):
    return TeacherService.delete(teacher_id)