from app.extensions import db
from app.models.course import Course


def create_course(course):
    db.session.add(course)


def get_all_courses():
    return Course.query.all()


def get_course_by_id(course_id):
    return Course.query.filter_by(id=course_id).first()


def get_course_by_code(course_code):
    return Course.query.filter_by(course_code=course_code).first()


def update_course():
    db.session.commit()


def delete_course(course):
    db.session.delete(course)