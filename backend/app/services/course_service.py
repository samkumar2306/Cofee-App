from app.extensions import db

from app.models.course import Course

from app.repositories.course_repository import (
    create_course,
    get_all_courses,
    get_course_by_id,
    get_course_by_code,
    update_course,
    delete_course
)


class CourseService:

    @staticmethod
    def create(data):

        if not data:
            return {
                "status": "error",
                "message": "Request body is required"
            }, 400

        required_fields = [
            "course_code",
            "course_name",
            "department",
            "duration",
            "semester_count"
        ]

        for field in required_fields:
            if not data.get(field):
                return {
                    "status": "error",
                    "message": f"{field} is required"
                }, 400

        existing_course = get_course_by_code(
            data["course_code"]
        )

        if existing_course:
            return {
                "status": "error",
                "message": "Course code already exists"
            }, 409

        try:

            course = Course(
                course_code=data["course_code"],
                course_name=data["course_name"],
                department=data["department"],
                duration=data["duration"],
                semester_count=data["semester_count"],
                description=data.get("description")
            )

            create_course(course)

            db.session.commit()

            return {
                "status": "success",
                "message": "Course created successfully",
                "course": {
                    "id": str(course.id),
                    "course_code": course.course_code,
                    "course_name": course.course_name,
                    "department": course.department,
                    "duration": course.duration,
                    "semester_count": course.semester_count,
                    "description": course.description
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

        courses = get_all_courses()

        data = []

        for course in courses:
            data.append({
                "id": str(course.id),
                "course_code": course.course_code,
                "course_name": course.course_name,
                "department": course.department,
                "duration": course.duration,
                "semester_count": course.semester_count,
                "description": course.description
            })

        return {
            "status": "success",
            "count": len(data),
            "courses": data
        }, 200    
    
    @staticmethod
    def get_by_id(course_id):

        course = get_course_by_id(course_id)

        if not course:
            return {
                "status": "error",
                "message": "Course not found"
            }, 404

        return {
            "status": "success",
            "course": {
                "id": str(course.id),
                "course_code": course.course_code,
                "course_name": course.course_name,
                "department": course.department,
                "duration": course.duration,
                "semester_count": course.semester_count,
                "description": course.description
            }
        }, 200
    
    @staticmethod
    def update(course_id, data):

        course = get_course_by_id(course_id)

        if not course:
            return {
                "status": "error",
                "message": "Course not found"
            }, 404

        if "course_name" in data:
            course.course_name = data["course_name"]

        if "department" in data:
            course.department = data["department"]

        if "duration" in data:
            course.duration = data["duration"]

        if "semester_count" in data:
            course.semester_count = data["semester_count"]

        if "description" in data:
            course.description = data["description"]

        try:

            update_course()

            return {
                "status": "success",
                "message": "Course updated successfully"
            }, 200

        except Exception as e:

            db.session.rollback()

            return {
                "status": "error",
                "message": str(e)
            }, 500
        

    @staticmethod
    def delete(course_id):

        course = get_course_by_id(course_id)

        if not course:
            return {
                "status": "error",
                "message": "Course not found"
            }, 404

        try:

            delete_course(course)

            db.session.commit()

            return {
                "status": "success",
                "message": "Course deleted successfully"
            }, 200

        except Exception as e:

            db.session.rollback()

            return {
                "status": "error",
                "message": str(e)
            }, 500
        
        