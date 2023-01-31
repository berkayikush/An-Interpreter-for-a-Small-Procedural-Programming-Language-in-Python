class Error(Exception):
    def __init__(self, error_message=None):
        self.__message = f"{self.__class__.__name__}: {error_message}"

    @property
    def message(self):
        return self.__message


class LexerError(Error):
    pass


class ParserError(Error):
    UNEXPECTED_TOKEN = "Unexpected token"
    NO_SEMICOLON = "No semicolon at the end of statement"


class SemnaticError(Error):
    INVALID_OPERATION = "Invalid operation"
    INVALID_ASSIGNMENT = "Invalid assignment"


class InterpreterError(Error):
    DIVISION_BY_ZERO = "Division by zero detected"
    MODULO_BY_ZERO = "Modulo by zero detected"
