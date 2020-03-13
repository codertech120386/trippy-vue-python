from rest_framework import status


class TripyException(Exception):
    """
    Base class to identify custom exceptions
    Each class inheriting this should have
    a code, a http_code and a message
    """
    pass


class InternalServerError(TripyException):
    code = "E000"
    http_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "An internal server error occured"


class EmailAlreadyRegistered(TripyException):
    code = "E001"
    http_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = "This email is already registered"


class InputValidationError(TripyException):
    code = "E002"
    http_code = status.HTTP_422_UNPROCESSABLE_ENTITY

    def __init__(self, message):
        self.message = message


class IncorrectPassword(TripyException):
    code = "E003"
    http_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = "Your password is not correct"


class EmailNotRegistered(TripyException):
    code = "E004"
    http_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = "This email is not registered"


class InvalidToken(TripyException):
    code = "E005"
    http_code = status.HTTP_401_UNAUTHORIZED
    message = "Your token has expired. Please login again"


class PermissionDenied(TripyException):
    code = "E006"
    http_code = status.HTTP_403_FORBIDDEN
    message = "You don't have permissions to perform this request"


class InvalidTripId(TripyException):
    code = "E007"
    http_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = "This Trip ID does not exist"


class InvalidUserId(TripyException):
    code = "E008"
    http_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = "This User ID does not exist"


MAPPED_EXCEPTIONS = {
    "PermissionDenied": PermissionDenied
}


def map_unknown_exception(exc):
    exception_type = exc.__class__.__name__
    return MAPPED_EXCEPTIONS.get(exception_type, InternalServerError)
