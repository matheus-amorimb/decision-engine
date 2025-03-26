from typing import List

from src.domains.policies.schemas import FlowValidationError


class BaseAppException(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code
        super().__init__(self.error)


class ResourceNotFoundException(BaseAppException):
    def __init__(self, error='Not found', status_code=404):
        super().__init__(error, status_code)


class ValidationException(BaseAppException):
    def __init__(self, error='Bad request', status_code=400):
        super().__init__(error, status_code)


class ConflictException(BaseAppException):
    def __init__(
        self, error: str = 'Resource already exists', status_code=409
    ):
        super().__init__(error, status_code)


class PolicyFlowValidationException(BaseAppException):
    def __init__(self, errors: List[FlowValidationError], status_code=400):
        error = [
            {'code': err.code(), 'message': err.message()} for err in errors
        ]
        super().__init__(error, status_code)
