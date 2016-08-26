
class ApiException(Exception):
    """
    Base class for exceptions raised from web api.
    """
    code = "api_exception"

    def __init__(self, message=None):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message or "Internal error"


class NotFound(ApiException):
    """
    The resource you are searching for does not exist (404).
    """
    code = "not_found"


class Forbidden(ApiException):
    """
    You don't have permission to do this operation (403).
    """
    code = "forbidden"


class BadRequest(ApiException):
    """
    You have given incorrect parameters (400).
    """
    code = "bad_request"

