from app.extensions import db
from app.models.student import Student


def create_student(student):
    db.session.add(student)
    return student


def get_student_by_id(student_id):
    return Student.query.get(student_id)


def get_student_by_user_id(user_id):
    return Student.query.filter_by(user_id=user_id).first()


def get_student_by_admission_no(admission_no):
    return Student.query.filter_by(
        admission_no=admission_no
    ).first()


def get_student_by_roll_no(roll_no):
    return Student.query.filter_by(
        roll_no=roll_no
    ).first()


def get_all_students():
    return Student.query.all()


def update_student():
    db.session.commit()


def delete_student(student):
    db.session.delete(student)
    db.session.commit()