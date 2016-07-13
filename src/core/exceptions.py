
class CoreException(Exception):
    """
    Base class for exceptions raised from core.
    """
    code = "core_exception"

    def __init__(self, message=None):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message or "Internal error"


class InvalidUser(CoreException):
    """
    You have tried to access with a nonexisting user id.
    """
    code = "invalid_user"

    def __init__(self, field_name, field_value):
        self.message = "Cannot find any user with {} {}".format(field_name, field_value)
        super().__init__(self.message)


class Forbidden(CoreException):
    """
    You don't have permission to do this operation.
    """
    code = "forbidden"


class InconsistentData(CoreException):
    """
    You have attempted store inconsistent data.
    """
    code = "inconsistent_data"

