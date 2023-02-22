class Token:
    EOF = "EOF"
    IDENTIFIER = "IDENTIFIER"  # An identifier is a combination of letters and numbers that begins with a letter
    # and can be followed by any number of additional letters and numbers.

    SEMICOLON = "SEMICOLON"  # ";"
    COLON = "COLON"  # ":"
    COMMA = "COMMA"  # ","

    ##############
    # Data Types #
    ##############
    INT = "INT"
    FLOAT = "FLOAT"
    BOOL = "BOOL"
    STR = "STR"

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

    ###############
    # Parentheses #
    ###############
    LEFT_PARENTHESIS = "LEFT_PARENTHESIS"  # "("
    RIGHT_PARENTHESIS = "RIGHT_PARENTHESIS"  # ")"

    ############
    # Brackets #
    ############
    LEFT_SQUARE_BRACKET = "LEFT_SQUARE_BRACKET"  # "["
    RIGHT_SQUARE_BRACKET = "RIGHT_SQUARE_BRACKET"  # "]"

    ###########
    # Wrapper #
    ###########
    LEFT_CURLY_BRACKET = "LEFT_CURLY_BRACKET"  # "{"
    RIGHT_CURLY_BRACKET = "RIGHT_CURLY_BRACKET"  # "}"

    ############
    # KEYWORDS #
    ############
    K_VAR = "var"
    K_INT = "int"
    K_FLOAT = "float"
    K_BOOL = "bool"
    K_STR = "str"
    K_AND = "and"
    K_OR = "or"
    K_NOT = "not"
    K_IF = "if"
    K_ELSEIF = "elseif"
    K_ELSE = "else"
    K_WHILE = "while"
    K_FOR = "for"
    K_FROM = "from"
    K_TO = "to"
    K_STEP = "step"
    K_CONTINUE = "continue"
    K_BREAK = "break"
    K_FUNC = "func"
    K_VOID = "void"
    K_RETURN = "return"

    KEYWORDS = (
        K_VAR,
        K_INT,
        K_FLOAT,
        K_BOOL,
        K_STR,
        K_AND,
        K_OR,
        K_NOT,
        K_IF,
        K_ELSEIF,
        K_ELSE,
        K_WHILE,
        K_FOR,
        K_FROM,
        K_TO,
        K_STEP,
        K_CONTINUE,
        K_BREAK,
        K_FUNC,
        K_VOID,
        K_RETURN,
    )

    ###########
    # COMMENT #
    ###########
    MULTI_LINE_COMMENT = "MULTI_LINE_COMMENT"  # "/* */"

    def __init__(self, _type, val=None, line=None, col=None):
        self.__type = _type
        self.__val = val

        self.__line = line
        self.__col = col

    @property
    def type_(self):
        return self.__type

    @property
    def val(self):
        return self.__val

    @property
    def line(self):
        return self.__line

    @property
    def col(self):
        return self.__col
