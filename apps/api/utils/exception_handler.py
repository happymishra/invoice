"""
Provides API exception handling classes. Exception message of these
classes is sent as an API response, when these exception occur
"""

from rest_framework.exceptions import APIException, ValidationError
from rest_framework.status import HTTP_400_BAD_REQUEST


class BadRequestException(APIException):
    """
    Generic Exception class to handle all the HTTP 400 Bad Request
    exceptions
    """
    status_code = HTTP_400_BAD_REQUEST
    default_detail = "Invalid input. Please enter a valid input"
    default_code = 'invalid'

    def __int__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code


class ServerException(APIException):
    """
    Generic Exception class to handle all the HTTP 500 Internal Server Errors
    """
    default_detail = "An unknown error occurred"


class ValidationException(ValidationError):
    """
    Generic exception class to handle the serializers validation errors
    """
    pass
