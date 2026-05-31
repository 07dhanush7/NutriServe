from werkzeug.exceptions import HTTPException

from app.utils.response import error_response


def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(error):
        return error_response(getattr(error, "description", "Bad request"), 400)

    @app.errorhandler(404)
    def not_found(error):
        return error_response("Route not found", 404)

    @app.errorhandler(405)
    def method_not_allowed(error):
        return error_response("Method not allowed", 405)

    @app.errorhandler(500)
    def server_error(error):
        app.logger.exception("Unhandled server error: %s", error)
        return error_response("Internal server error", 500)

    @app.errorhandler(Exception)
    def unhandled_exception(error):
        if isinstance(error, HTTPException):
            return error_response(error.description, error.code)
        app.logger.exception("Unhandled exception: %s", error)
        return error_response("Internal server error", 500)
