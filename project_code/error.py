class Error(Exception):
    IDENTIFIER_NOT_FOUND = "Identifier not found"
    IDENTIFIER_ALREADY_DEFINED = "Identifier is already defined"

    UNEXPECTED_TOKEN = "Unexpected token"

    def __init__(self, error_message=None, value=None):
        self.__error_message = f"{self.__class__.__name__}: {error_message}"
        self.__value = value


class LexerError(Error):
    pass


class ParserError(Error):
    pass


class SemanticAnalysisError(Error):
    pass
