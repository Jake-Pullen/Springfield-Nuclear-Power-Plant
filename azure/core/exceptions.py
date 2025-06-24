"""Azure SDK exceptions"""


class AzureError(Exception):
    """Base exception for all Azure errors"""
    def __init__(self, message: str, error=None):
        self.message = message
        self.error = error
        super().__init__(self.message)


class HttpResponseError(AzureError):
    """HTTP response error"""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ResourceExistsError(HttpResponseError):
    """Resource already exists error"""
    def __init__(self, message: str):
        super().__init__(message, 409)


class ResourceNotFoundError(HttpResponseError):
    """Resource not found error"""
    def __init__(self, message: str):
        super().__init__(message, 404)


class ClientAuthenticationError(HttpResponseError):
    """Client authentication error"""
    def __init__(self, message: str):
        super().__init__(message, 401)


class ThrottlingError(HttpResponseError):
    """Rate limiting error"""
    def __init__(self, message: str):
        super().__init__(message, 429)
