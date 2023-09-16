class UserAlreadyExistsException(Exception):
    def __init__(self, email: str = None):
        if email:
            self.message = f"User with email: {email} already exists"
        else:
            self.message = "User with the entered email already exists"
        super().__init__(self.message)

class InvalidEmailException(Exception):
    def __init__(self, email: str = None):
        if email:
            self.message = f"The email entered: {email} is invalid"
        else:
            self.message = "The email entered is invalid"
        super().__init__(self.message)

class InvalidPasswordException(Exception):
    def __init__(self, message: str = None):
        if message:
            self.message = message 
        else: 
         self.message = "Password must be longer than 8 characters and contain at least one lowercase, uppercase, digit, and special character"
        super().__init__(self.message)

class UserDoesNotExistException(Exception):
    def __init__(self, message: str = None):
        if not message:
            self.message = "User does not exist"
        else:
            self.message = message
        super().__init__(self.message)

class UrlParamDoesNotExistException(Exception):
    def __init__(self, param_name: str = None):
        if param_name:
            self.message(f"Url Param {param_name} is missing")
        else:
            self.message("Url Param is missing")

class InvalidLoginCredentialsException(Exception):
    def __init__(self):
        self.message = "Invalid Login Credentials"
        super().__init__(self.message)

class MissingInformationException(Exception):
    def __init__(self, info: str):
        if info: 
            self.message = f"Missing information in request body: {info}"
        else:
            self.message = 'Missing information in request body'
        super().__init__(self.message)

class UserDoesNotHaveAnyWordsException(Exception):
    def __init__(self):
        self.message = "User has not created any words"
        super().__init__(self.message)

class WordDoesNotExistException(Exception):
    def __init__(self):
        self.message = "Word does not exist"
        super().__init__(self.message)

class UserHasNoStatsException(Exception):
    def __init__(self):
        self.message = "User does not have stats"
        super().__init__(self.message)

class MissingQueryParamException(Exception):
    def __init__(self, query_param: str = None):
        if query_param: 
            self.message = f"Missing query parameter: {query_param}"
        else: 
            self.message = "Missing query parameter(s)"
        super().__init__(self.message)

class InvalidInformationException(Exception):
    def __init__(self, message: str = None):
        if message: 
            self.message = f"Invalid information: {message}"
        else:
            self.message = "Invalid information was received"
        super().__init__(self.message)

class EmailSendingFailedException(Exception):
    def __init__(self):
        self.message = "Failed to send email (backend)"
        super().__init__(self.message)

class InvalidTokenException(Exception):
    def __init__(self): 
        self.message = "Invalid Token"
        super().__init__(self.message)