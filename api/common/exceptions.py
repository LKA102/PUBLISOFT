from fastapi import HTTPException

class BaseException(Exception):
    """Base class for all exceptions in the application."""
    def __init__(self, message: str, error_code: int):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        
class APIHTTPException(HTTPException):
    def __init__(self, status_code: int, exception: BaseException):
        status_code = status_code
        detail = {
            "message": exception.message,
            "error_code": exception.error_code
        }
        super().__init__(status_code=status_code, detail=detail)