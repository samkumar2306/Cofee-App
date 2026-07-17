class APIException(Exception):

    def __init__(
        self,
        message,
        status_code=400
    ):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class NotFoundException(APIException):

    def __init__(self, message="Resource not found"):
        super().__init__(message, 404)


class UnauthorizedException(APIException):

    def __init__(self, message="Unauthorized"):
        super().__init__(message, 401)


class ForbiddenException(APIException):

    def __init__(self, message="Forbidden"):
        super().__init__(message, 403)


class BadRequestException(APIException):

    def __init__(self, message="Bad Request"):
        super().__init__(message, 400)


class ConflictException(APIException):

    def __init__(self, message="Conflict"):
        super().__init__(message, 409)