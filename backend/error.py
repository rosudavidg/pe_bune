from enum import Enum

class Error(Enum):
    UNKNOWN = 0
    INVALID_INPUT = 1
    INVALID_USERNAME = 2
    INVALID_EMAIL = 3

    def __str__(self):
        return self.name

    @staticmethod
    def new(err):
        message = str(err)
        if 'Duplicate' in message:
            if 'PRIMARY' in message:  
                return Error.INVALID_USERNAME
            if 'email' in message:  
                return Error.INVALID_EMAIL
            
            return Error.UNKNOWN
            
