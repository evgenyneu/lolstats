"""Custom exceptions."""


class MyError(Exception):
    """Base class for exceptions in this module."""


class HttpError(MyError):
    """Exception raised for HTTP request errors.

    Attributes:
        message -- explanation of the error
        status_code -- HTTP status code associated with the error
    """

    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code
