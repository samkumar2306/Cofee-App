from functools import wraps

from flask_jwt_extended import (
    get_jwt,
    verify_jwt_in_request
)

from app.core.responses import error_response


def roles_required(*roles):

    def decorator(fn):

        @wraps(fn)
        def wrapper(*args, **kwargs):

            verify_jwt_in_request()

            claims = get_jwt()

            current_role = claims.get("role")

            allowed_roles = [
                role.name
                for role in roles
            ]

            if current_role not in allowed_roles:

                return error_response(
                    message="Access denied",
                    status_code=403
                )

            return fn(*args, **kwargs)

        return wrapper

    return decorator