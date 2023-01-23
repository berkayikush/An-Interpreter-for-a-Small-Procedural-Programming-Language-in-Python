class AST:
    pass


class VarNode(AST):
    def __init__(self, var_token):
        self.__value = var_token.value

    @property
    def value(self):
        return self.__value


class NumberNode(AST):
    def __init__(self, num_token):
        self.__value = num_token.value

    @property
    def value(self):
        return self.__value


class BoolNode(AST):
    def __init__(self, bool_token):
        self.__value = bool_token.value

    @property
    def value(self):
        return self.__value


class UnaryOpNode(AST):
    def __init__(self, op_token, child_node):
        self.__op_token = op_token
        self.__child_node = child_node

    @property
    def op_token(self):
        return self.__op_token

    @property
    def child_node(self):
        return self.__child_node


class BinaryOpNode(AST):
    def __init__(self, left_node, op_token, right_node):
        self.__left_node = left_node
        self.__op_token = op_token
        self.__right_node = right_node

    @property
    def left_node(self):
        return self.__left_node

    @property
    def op_token(self):
        return self.__op_token

    @property
    def right_node(self):
        return self.__right_node


class EmptyStatementNode(AST):
    pass


class AssignStatementNode(AST):
    def __init__(self, left_node, op_token, right_node):
        self.__left_node = left_node
        self.__op_token = op_token
        self.__right_node = right_node

    @property
    def left_node(self):
        return self.__left_node

    @property
    def op_token(self):
        return self.__op_token

    @property
    def right_node(self):
        return self.__right_node


class ConditionalStatementNode(AST):
    def __init__(self, if_cases, else_case):
        self.__if_cases = if_cases
        self.__else_case = else_case

    @property
    def if_cases(self):
        return self.__if_cases

    @property
    def else_case(self):
        return self.__else_case


class WhileStatementNode(AST):
    def __init__(self, condition, statement_list_node):
        self.__condition = condition
        self.__statement_list_node = statement_list_node

    @property
    def condition(self):
        return self.__condition

    @property
    def statement_list_node(self):
        return self.__statement_list_node


class ForStatementNode(AST):
    def __init__(self, var_node, range_, statement_list_node):
        self.__var_node = var_node
        self.__range = range_
        self.__statement_list_node = statement_list_node


class VarTypeNode(AST):
    def __init__(self, type_token):
        self.__value = type_token.value

    @property
    def value(self):
        return self.__value


class VarDeclStatementNode(AST):
    def __init__(self, var_type_node, variables):
        self.__var_type_node = var_type_node
        self.__variables = variables

    @property
    def var_type_node(self):
        return self.__var_type_node

    @property
    def variables(self):
        return self.__variables


class StatementListNode(AST):
    def __init__(self):
        self.__statements = []

    @property
    def statements(self):
        return self.__statements


class ProgramNode(AST):
    def __init__(self, statement_list_node):
        self.__statement_list_node = statement_list_node

    @property
    def statement_list_node(self):
        return self.__statement_list_node
