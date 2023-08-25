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
    def __init__(self):
        self.message = "Password must be longer than 8 characters and contain at least one lowercase, uppercase, digit, and special character"
        super().__init__(self.message)

class UserDoesNotExistException(Exception):
    def __init__(self, table_name: str = None):
        if not table_name:
            self.message = "User does not exist in database"
        else:
            self.message = f"User does not exist in {table_name} table"
        super().__init__(self.message)

class UrlParamDoesNotExistException(Exception):
    def __init__(self, param_name: str = None):
        if param_name:
            self.message(f"Url Param {param_name} is missing")
        else:
            self.message("Url Param is missing")

class InvalidLoginCredentialsException(Exception):
    def __init__(self):
        self.message = "Invald Login Credentials"
        super().__init__(self.message)