class InvalidUsage(Exception):
    """Custom exception for API errors"""
    status_code = 400
    
    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
    
    def to_dict(self):
        rv = {'error': self.message}
        if self.payload:
            rv['details'] = self.payload
        return rv

class AuthError(InvalidUsage):
    """Authentication error"""
    def __init__(self, message, status_code=401):
        super().__init__(message, status_code)

class NotFoundError(InvalidUsage):
    """Resource not found error"""
    def __init__(self, message, status_code=404):
        super().__init__(message, status_code)

class InvalidOperation(InvalidUsage):
    """Invalid business operation"""
    def __init__(self, message, status_code=400):
        super().__init__(message, status_code)