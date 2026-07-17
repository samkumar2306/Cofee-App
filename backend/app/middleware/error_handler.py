from app.core.responses import error_response
from app.core.exceptions import APIException
from app.core.logger import logger


def register_error_handlers(app):

    @app.errorhandler(APIException)
    def handle_api_exception(error):

        return error_response(
            message=error.message,
            status_code=error.status_code
        )

    @app.errorhandler(Exception)
    def handle_exception(error):

        logger.exception(error)

        return error_response(
            message="Internal Server Error",
            status_code=500
        )