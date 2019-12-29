from rest_framework.exceptions import APIException, ValidationError
from rest_framework.status import HTTP_400_BAD_REQUEST


class BadRequestException(APIException):
    status_code = HTTP_400_BAD_REQUEST
    default_detail = "Invalid input. Please enter a valid input"
    default_code = 'invalid'

    def __int__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code


class ServerException(APIException):
    default_detail = "An unknown error occurred"


class ValidationException(ValidationError):
    pass
