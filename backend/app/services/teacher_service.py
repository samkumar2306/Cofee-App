from app.extensions import db

from app.models.user import User
from app.models.teacher import Teacher

from app.repositories.user_repository import (
    get_user_by_email,
    create_user
)

from app.repositories.teacher_repository import (
    create_teacher,
    get_teacher_by_employee_id,
    get_teacher_by_id,
    get_all_teachers,
    update_teacher,
    delete_teacher
)

from app.utils.password import hash_password
from app.utils.enums import UserRole


class TeacherService:

    @staticmethod
    def create(data):

        if not data:
            return {
                "status": "error",
                "message": "Request body is required"
            }, 400

        required_fields = [
            "full_name",
            "email",
            "password",
            "employee_id",
            "department",
            "designation"
        ]

        for field in required_fields:
            if not data.get(field):
                return {
                    "status": "error",
                    "message": f"{field} is required"
                }, 400

        existing_user = get_user_by_email(data["email"])

        if existing_user:
            return {
                "status": "error",
                "message": "Email already exists"
            }, 409

        existing_teacher = get_teacher_by_employee_id(
            data["employee_id"]
        )

        if existing_teacher:
            return {
                "status": "error",
                "message": "Employee ID already exists"
            }, 409

        try:

            user = User(
                full_name=data["full_name"],
                email=data["email"],
                password=hash_password(data["password"]),
                phone=data.get("phone"),
                role=UserRole.TEACHER
            )

            create_user(user)

            db.session.flush()

            teacher = Teacher(
                user_id=user.id,
                employee_id=data["employee_id"],
                department=data["department"],
                designation=data["designation"],
                qualification=data.get("qualification"),
                experience=data.get("experience"),
                date_of_joining=data.get("date_of_joining"),
                salary=data.get("salary"),
                address=data.get("address")
            )

            create_teacher(teacher)

            db.session.commit()

            return {
                "status": "success",
                "message": "Teacher created successfully",
                "teacher": {
                    "id": str(teacher.id),
                    "user_id": str(user.id),
                    "full_name": user.full_name,
                    "email": user.email,
                    "employee_id": teacher.employee_id,
                    "department": teacher.department,
                    "designation": teacher.designation
                }
            }, 201

        except Exception as e:

            db.session.rollback()

            return {
                "status": "error",
                "message": str(e)
            }, 500

    @staticmethod
    def get_all():

        teachers = get_all_teachers()

        data = []

        for teacher in teachers:
            data.append({
                "id": str(teacher.id),
                "user_id": str(teacher.user_id),
                "full_name": teacher.user.full_name,
                "email": teacher.user.email,
                "phone": teacher.user.phone,
                "employee_id": teacher.employee_id,
                "department": teacher.department,
                "designation": teacher.designation,
                "qualification": teacher.qualification,
                "experience": teacher.experience,
                "date_of_joining": teacher.date_of_joining,
                "salary": float(teacher.salary) if teacher.salary else None,
                "address": teacher.address
            })

        return {
            "status": "success",
            "count": len(data),
            "teachers": data
        }, 200

    @staticmethod
    def get_by_id(teacher_id):

        teacher = get_teacher_by_id(teacher_id)

        if not teacher:
            return {
                "status": "error",
                "message": "Teacher not found"
            }, 404

        return {
            "status": "success",
            "teacher": {
                "id": str(teacher.id),
                "user_id": str(teacher.user_id),
                "full_name": teacher.user.full_name,
                "email": teacher.user.email,
                "phone": teacher.user.phone,
                "employee_id": teacher.employee_id,
                "department": teacher.department,
                "designation": teacher.designation,
                "qualification": teacher.qualification,
                "experience": teacher.experience,
                "date_of_joining": teacher.date_of_joining,
                "salary": float(teacher.salary) if teacher.salary else None,
                "address": teacher.address
            }
        }, 200
    
    @staticmethod
    def update(teacher_id, data):

        teacher = get_teacher_by_id(teacher_id)

        if not teacher:
            return {
                "status": "error",
                "message": "Teacher not found"
            }, 404

        user = teacher.user

        if "full_name" in data:
            user.full_name = data["full_name"]

        if "phone" in data:
            user.phone = data["phone"]

        if "department" in data:
            teacher.department = data["department"]

        if "designation" in data:
            teacher.designation = data["designation"]

        if "qualification" in data:
            teacher.qualification = data["qualification"]

        if "experience" in data:
            teacher.experience = data["experience"]

        if "date_of_joining" in data:
            teacher.date_of_joining = data["date_of_joining"]

        if "salary" in data:
            teacher.salary = data["salary"]

        if "address" in data:
            teacher.address = data["address"]

        try:

            update_teacher()

            return {
                "status": "success",
                "message": "Teacher updated successfully",
                "teacher": {
                    "id": str(teacher.id),
                    "user_id": str(teacher.user_id),
                    "full_name": user.full_name,
                    "email": user.email,
                    "phone": user.phone,
                    "employee_id": teacher.employee_id,
                    "department": teacher.department,
                    "designation": teacher.designation,
                    "qualification": teacher.qualification,
                    "experience": teacher.experience,
                    "date_of_joining": teacher.date_of_joining,
                    "salary": float(teacher.salary) if teacher.salary else None,
                    "address": teacher.address
                }
            }, 200

        except Exception as e:

            db.session.rollback()

            return {
                "status": "error",
                "message": str(e)
            }, 500

    @staticmethod
    def delete(teacher_id):

        teacher = get_teacher_by_id(teacher_id)

        if not teacher:
            return {
                "status": "error",
                "message": "Teacher not found"
            }, 404

        try:

            user = teacher.user

            delete_teacher(teacher)

            db.session.delete(user)

            db.session.commit()

            return {
                "status": "success",
                "message": "Teacher deleted successfully"
            }, 200

        except Exception as e:

            db.session.rollback()

            return {
                "status": "error",
                "message": str(e)
            }, 500