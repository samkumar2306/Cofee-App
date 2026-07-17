from app.models.user import User
from app.models.student import Student
from app.extensions import db

from app.repositories.user_repository import (
    get_user_by_email,
    create_user
)

from app.repositories.student_repository import (
    create_student,
    get_student_by_admission_no,
    get_student_by_roll_no
)

from app.utils.password import hash_password
from app.utils.enums import UserRole


class StudentService:

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
            "admission_no",
            "roll_no",
            "department",
            "year",
            "section"
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
        
        existing_admission = get_student_by_admission_no(
            data["admission_no"]
        )    

        if existing_admission:
            return {
                "status": "error",
                "message": "Admission number already exists"
            }, 409
        
        existing_roll = get_student_by_roll_no(
            data["roll_no"]
        )

        if existing_roll:
            return {
                "status":"error",
                "message": "Roll number already exists"
            }, 409
        
        try:
            user = User(
                 full_name=data["full_name"],
                 email=data["email"],
                 password=hash_password(data["password"]),
                 phone=data.get("phone"),
                 role=UserRole.STUDENT
            )

            create_user(user)

            db.session.flush()

            student = Student(
                user_id=user.id,
                admission_no=data["admission_no"],
                roll_no=data["roll_no"],
                department=data["department"],
                year=data["year"],
                section=data["section"],
                date_of_birth=data.get("date_of_birth"),
                gender=data.get("gender"),
                blood_group=data.get("blood_group"),
                guardian_name=data.get("guardian_name"),
                guardian_phone=data.get("guardian_phone"),
                address=data.get("address")
            )

            create_student(student)

            db.session.commit()

        except Exception as e:
         db.session.rollback()

        return {
           "status": "error",
           "message": str(e)
        }, 500           

        return {
            "status": "success",
            "message": "Student created successfully",
            "student":{
                "id": str(student.id),
                "user_id": str(user.id),
                "full_name": user.full_name,
                "email": user.email,
                "admission_no": student.admission_no,
                "roll_no": student.roll_no,
                "department": student.department,
                "year": student.year,
                "section": student.section
            }
        }, 201

    