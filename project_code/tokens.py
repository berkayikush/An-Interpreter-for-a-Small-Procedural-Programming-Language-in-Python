class Token:
    EOF = "EOF"
    IDENTIFIER = "IDENTIFIER"  # An identifier is a combination of letters and numbers that begins with a letter
    # and can be followed by any number of additional letters and numbers.

    SEMI_COLON = "SEMI_COLON"  # ";"
    COMMA = "COMMA"  # ","

    ##############
    # Data Types #
    ##############
    INT = "INT"
    FLOAT = "FLOAT"
    BOOL = "BOOL"

    #########################
    # Arithmetic Operations #
    #########################
    PLUS = "PLUS"  # "+"
    MINUS = "MINUS"  # "-"
    MULTIPLICATION = "MULTIPLICATION"  # "*"
    INT_DIVISION = "INT_DIVISION"  # "//"
    FLOAT_DIVISION = "FLOAT_DIVISION"  # "/"
    MODULO = "MODULO"  # "%"

    #########################
    # Assignment Operations #
    #########################
    ASSIGN = "ASSIGN"  # "="
    PLUS_ASSIGN = "PLUS_ASSIGN"  # "+="
    MINUS_ASSIGN = "MINUS_ASSIGN"  # "-="
    MULTIPLICATION_ASSIGN = "MULTIPLY_ASSIGN"  # "*="
    FLOAT_DIVISION_ASSIGN = "DIVISION_ASSIGN"  # "/="
    INT_DIVISION_ASSIGN = "DIVISION_ASSIGN"  # "//="
    MODULO_ASSIGN = "MODULO_ASSIGN"  # "%="

    #########################
    # Comparison Operations #
    #########################
    EQUALS = "EQUALS"  # "=="
    NOT_EQUALS = "NOT_EQUALS"  # "!="
    LESS_THAN = "LESS_THAN"  # "<"
    LESS_THAN_OR_EQUALS = "LESS_THAN_OR_EQUALS"  # "<="
    GREATER_THAN = "GREATER_THAN"  # ">"
    GREATER_THAN_OR_EQUALS = "GREATER_THAN_OR_EQUALS"  # ">="

    ######################
    # Logical Operations #
    ######################

    ###############
    # Parentheses #
    ###############
    LEFT_PARENTHESIS = "LEFT_PARENTHESIS"  # "("
    RIGHT_PARENTHESIS = "RIGHT_PARENTHESIS"  # ")"

    ###########
    # Wrapper #
    ###########
    LEFT_CURLY_BRACKET = "LEFT_CURLY_BRACKET"  # "{"
    RIGHT_CURLY_BRACKET = "RIGHT_CURLY_BRACKET"  # "}"

    ############
    # KEYWORDS #
    ############
    K_VAR = "K_VAR"
    K_INT = "K_INT"
    K_FLOAT = "K_FLOAT"
    K_BOOL = "K_BOOL"
    K_AND = "K_AND"
    K_OR = "K_OR"
    K_NOT = "K_NOT"
    K_IF = "K_IF"
    K_ELSEIF = "K_ELSEIF"
    K_ELSE = "K_ELSE"

    KEYWORDS = {
        "var": K_VAR,
        "int": K_INT,
        "float": K_FLOAT,
        "bool": K_BOOL,
        "and": K_AND,
        "or": K_OR,
        "not": K_NOT,
        "if": K_IF,
        "elseif": K_ELSEIF,
        "else": K_ELSE,
    }

    ###########
    # COMMENT #
    ###########
    MULTI_LINE_COMMENT = "MULTI_LINE_COMMENT"  # "/* */"

    def __init__(self, _type, value=None):
        self.__type = _type
        self.__value = value

    @property
    def type_(self):
        return self.__type

    @property
    def value(self):
        return self.__value

    def __str__(self):
        return f"Token({self.__type}, {self.__value})"

    def __repr__(self):
        return self.__str__()
