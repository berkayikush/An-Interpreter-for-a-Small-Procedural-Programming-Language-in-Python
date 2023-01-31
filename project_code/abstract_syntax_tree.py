class AST:
    pass


class VarNode(AST):
    def __init__(self, var_token):
        self.__token = var_token
        self.__val = var_token.val

    @property
    def token(self):
        return self.__token

    @property
    def val(self):
        return self.__val


class NumberNode(AST):
    def __init__(self, num_token):
        self.__token = num_token
        self.__val = num_token.val

    @property
    def token(self):
        return self.__token

    @property
    def val(self):
        return self.__val


class BoolNode(AST):
    def __init__(self, bool_token):
        self.__token = bool_token
        self.__val = bool_token.val

    @property
    def token(self):
        return self.__token

    @property
    def val(self):
        return self.__val


class StrNode(AST):
    def __init__(self, str_token):
        self.__token = str_token
        self.__val = str_token.val

    @property
    def token(self):
        return self.__token

    @property
    def val(self):
        return self.__val


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

    @property
    def token(self):
        return self.__child_node.token


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

    @property
    def token(self):
        return self.__left_node.token


class EmptyStatementNode(AST):
    pass


class AssignmentStatementNode(AST):
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


class RangeExprNode(AST):
    def __init__(self, start_node, end_node, step_node):
        self.__start_node = start_node
        self.__end_node = end_node
        self.__step_node = step_node

    @property
    def start_node(self):
        return self.__start_node

    @property
    def end_node(self):
        return self.__end_node

    @property
    def step_node(self):
        return self.__step_node

    @property
    def token(self):
        return self.__start_node.token


class ForStatementNode(AST):
    def __init__(self, var_decl_statement_node, iterable, statement_list_node):
        self.__var_decl_statement_node = var_decl_statement_node
        self.__iterable = iterable
        self.__statement_list_node = statement_list_node

    @property
    def var_decl_statement_node(self):
        return self.__var_decl_statement_node

    @property
    def iterable(self):
        return self.__iterable

    @property
    def statement_list_node(self):
        return self.__statement_list_node


class VarTypeNode(AST):
    def __init__(self, type_token):
        self.__token = type_token
        self.__val = type_token.val

    @property
    def token(self):
        return self.__token

    @property
    def val(self):
        return self.__val


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


class ReturnTypeNode(AST):
    def __init__(self, return_type_token):
        self.__val = return_type_token.val

    @property
    def val(self):
        return self.__val


class FuncParamNode(AST):
    def __init__(self, var_type_node, var_node):
        self.__var_type_node = var_type_node
        self.__var_node = var_node

    @property
    def var_type_node(self):
        return self.__var_type_node

    @property
    def var_node(self):
        return self.__var_node


class FuncDeclStatementNode(AST):
    def __init__(self, return_type_node, func_name, func_params, func_body):
        self.__return_type_node = return_type_node
        self.__name = func_name
        self.__params = func_params
        self.__body = func_body

    @property
    def return_type_node(self):
        return self.__return_type_node

    @property
    def name(self):
        return self.__name

    @property
    def params(self):
        return self.__params

    @property
    def body(self):
        return self.__body


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
