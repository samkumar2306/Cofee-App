import re
from flask_jwt_extended import create_access_token
from app.utils.password import verify_password

from app.models.user import User
from app.repositories.user_repository import (
    get_user_by_email,
    get_user_by_id,
    update_user,
    create_user
)
from app.utils.password import hash_password
from app.utils.enums import UserRole


class AuthService:

    @staticmethod
    def register(data):

        # Request body validation
        if not data:
            return {
                "status": "error",
                "message": "Request body is required"
            }, 400

        # Required fields
        required_fields = [
            "full_name",
            "email",
            "password",
            "role"
        ]

        for field in required_fields:
            if not data.get(field):
                return {
                    "status": "error",
                    "message": f"{field} is required"
                }, 400

        # Email validation
        email = data.get("email")

        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        if not re.match(email_pattern, email):
            return {
                "status": "error",
                "message": "Invalid email format"
            }, 400

        # Password validation
        if len(data["password"]) < 8:
            return {
                "status": "error",
                "message": "Password must be at least 8 characters"
            }, 400

        # Role validation
        try:
            role = UserRole[data["role"]]
        except KeyError:
            return {
                "status": "error",
                "message": "Invalid role"
            }, 400

        # Check duplicate email
        existing_user = get_user_by_email(email)

        if existing_user:
            return {
                "status": "error",
                "message": "Email already exists"
            }, 409

        # Hash password
        hashed_password = hash_password(data["password"])

        # Create user object
        user = User(
            full_name=data["full_name"],
            email=email,
            password=hashed_password,
            phone=data.get("phone"),
            role=role
        )

        # Save user
        create_user(user)

        return {
            "status": "success",
            "message": "User registered successfully"
        }, 201
    

    @staticmethod
    def login(data):

        if not data:
            return {
               "status": "error",
               "message": "Request body is required"
            }, 400
        
        email = data.get("email")
        password = data.get("password")


        if not email or not password:
            return {
               "status": "error",
               "message": "Email and Password are required"
            }, 400

        user = get_user_by_email(email)

        if not user:
            return {
               "status": "error",
               "message": "Invalid email or password"
            }, 401

        if not verify_password(password, user.password):
            return {
               "status": "error",
               "message": "Invalid email or password"
            }, 401

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={
                "role": user.role.name
            }
        )

        return {
            "status": "success",
            "message": "Login Successful",
            "access_token": access_token,
            "user": {
                "id": str(user.id),
                "full_name": user.full_name,
                "email": user.email,
                "role": user.role.name
            }
        }, 200
    

    @staticmethod
    def me(user_id):
        
        user = get_user_by_id(user_id)

        if not user:
                return {
                   "status": "error",
                   "message": "User not found"
                }, 404

        return {
            "status": "success",
            "user": {
                "id": str(user.id),
                "full_name": user.full_name,
                "email": user.email,
                "phone": user.phone,
                "role": user.role.name
            }
        }, 200
    
    @staticmethod
    def update_profile(user_id, data):

        user = get_user_by_id(user_id)

        if not user:
           return {
             "status": "error",
             "message": "User not found"
            }, 404

        if "full_name" in data:
           user.full_name = data["full_name"]

        if "phone" in data:
           user.phone = data["phone"]
           
           update_user()
           
        return {
          "status": "success",
          "message": "Profile updated successfully",
          "user": {
              "id": str(user.id),
              "full_name": user.full_name,
              "email": user.email,
              "phone": user.phone,
              "role": user.role.name
            }
        }, 200
    

    @staticmethod
    def change_password(user_id, data):

       user = get_user_by_id(user_id)

       if not user:
           return {
              "status": "error",
              "message": "User not found"
            }, 404

       old_password = data.get("old_password")
       new_password = data.get("new_password")

       if not old_password or not new_password:
           return {
              "status": "error",
              "message": "Old password and new password are required"
            }, 400

       if not verify_password(old_password, user.password):
           return {
              "status": "error",
              "message": "Old password is incorrect"
            }, 401

       if len(new_password) < 8:
           return {
              "status": "error",
              "message": "New password must be at least 8 characters"
            }, 400

       user.password = hash_password(new_password)

       update_user()

       return {
          "status": "success",
          "message": "Password changed successfully"
        }, 200