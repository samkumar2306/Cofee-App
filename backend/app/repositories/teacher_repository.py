from app.extensions import db
from app.models.teacher import Teacher
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import joinedload


def create_teacher(teacher):
    db.session.add(teacher)
    return teacher


def get_teacher_by_id(teacher_id):
    return Teacher.query.options(
        joinedload(Teacher.user)
    ).filter_by(id=teacher_id).first()

def get_teacher_by_user_id(user_id):
    return Teacher.query.filter_by(user_id=user_id).first()


def get_teacher_by_employee_id(employee_id):
    return Teacher.query.filter_by(employee_id=employee_id).first()


def get_all_teachers():
    return Teacher.query.all()


def get_all_teachers():
    return Teacher.query.options(
        joinedload(Teacher.user)
    ).all()


def delete_teacher(teacher):
    db.session.delete(teacher)

def update_teacher():
    db.session.commit()    