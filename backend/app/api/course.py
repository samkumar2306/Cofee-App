from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.services.course_service import CourseService
from app.decorators.roles import roles_required
from app.utils.enums import UserRole

course_bp = Blueprint(
    "course",
    __name__,
    url_prefix="/api/courses"
)


@course_bp.route("", methods=["POST"])
@jwt_required()
# @roles_required(UserRole.ADMIN)
def create_course():
    data = request.get_json()
    return CourseService.create(data)


@course_bp.route("", methods=["GET"])
@jwt_required()
def get_all_courses():
    return CourseService.get_all()


@course_bp.route("/<uuid:course_id>", methods=["GET"])
@jwt_required()
def get_course(course_id):
    return CourseService.get_by_id(course_id)


@course_bp.route("/<uuid:course_id>", methods=["PUT"])
@jwt_required()
# @roles_required(UserRole.ADMIN)
def update_course(course_id):
    data = request.get_json()
    return CourseService.update(course_id, data)


@course_bp.route("/<uuid:course_id>", methods=["DELETE"])
@jwt_required()
# @roles_required(UserRole.ADMIN)
def delete_course(course_id):
    return CourseService.delete(course_id)