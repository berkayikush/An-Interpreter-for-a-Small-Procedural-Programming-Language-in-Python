from .tokens import Token
from .abstract_syntax_tree import (
    VarNode,
    AccessNode,
    NumberNode,
    BoolNode,
    StrNode,
    UnaryOpNode,
    BinaryOpNode,
    EmptyStatementNode,
    AssignmentStatementNode,
    FuncCallStatementNode,
    ConditionalStatementNode,
    WhileStatementNode,
    RangeExprNode,
    ForStatementNode,
    VarTypeNode,
    VarDeclStatementNode,
    ReturnTypeNode,
    FuncParamNode,
    FuncDeclStatementNode,
    StatementListNode,
    ProgramNode,
)
from .error import ParserError


class Parser:
    def __init__(self, lexer):
        self.__lexer = lexer
        self.__curr_token = self.__lexer.get_next_token()

    def parse(self):
        ast_node = self.__program()

        if self.__curr_token.type_ != Token.EOF:
            self.__error()

        return ast_node

    def __eat(self, token_type):
        """
        Verify that the current token matches the passed token type.
        If it does, then "eat" the current token and assign the next.
        """
        if self.__curr_token.type_ == token_type:
            self.__curr_token = self.__lexer.get_next_token()
            return

        self.__error(token_type=token_type)

    def __error(self, token_type=None):
        error_message = (
            f"{ParserError.NO_SEMICOLON}"
            if token_type == Token.SEMI_COLON
            else f'{ParserError.UNEXPECTED_TOKEN} "{self.__curr_token.val}"'
        )

        raise ParserError(
            error_message
            + f" on line: {self.__curr_token.line}, column: {self.__curr_token.col}",
        )

    def __var_name(self):
        """
        var_name: IDENTIFIER
        """
        token = self.__curr_token
        self.__eat(Token.IDENTIFIER)

        return VarNode(var_token=token)

    def __accessor(self):
        """
        accessor: (STR | var_name) LEFT_SQUARE_BRACKET logical_expr (COLON logical_expr)? RIGHT_SQUARE_BRACKET
        """
        accessor_token = self.__curr_token

        if accessor_token.type_ == Token.STR:
            self.__eat(Token.STR)
            accessor_node = StrNode(str_token=accessor_token)
        else:
            accessor_node = self.__var_name()

        self.__eat(Token.LEFT_SQUARE_BRACKET)
        start_index = self.__logical_expr()

        if self.__curr_token.type_ == Token.COLON:
            self.__eat(Token.COLON)
            end_index = self.__logical_expr()
        else:
            end_index = None

        self.__eat(Token.RIGHT_SQUARE_BRACKET)
        return AccessNode(accessor_node, start_index, end_index)

    def __factor(self):
        """
        factor: (INT | FLOAT | BOOL | STR)
                | LEFT_PARENTHESIS logical_expr RIGHT_PARENTHESIS
                | (PLUS | MINUS) factor
                | accessor
                | var_name
        """
        token = self.__curr_token

        if self.__lexer.check_curr_char() == "[":
            return self.__accessor()

        if token.type_ in (Token.INT, Token.FLOAT):
            self.__eat(token.type_)
            return NumberNode(num_token=token)

        if token.type_ == Token.BOOL:
            self.__eat(token.type_)
            return BoolNode(bool_token=token)

        if token.type_ == Token.STR:
            self.__eat(token.type_)
            return StrNode(str_token=token)

        if token.type_ in (Token.PLUS, Token.MINUS):
            self.__eat(token.type_)
            return UnaryOpNode(op_token=token, child_node=self.__factor())

        if token.type_ == Token.LEFT_PARENTHESIS:
            self.__eat(Token.LEFT_PARENTHESIS)
            ast_node = self.__logical_expr()

            self.__eat(Token.RIGHT_PARENTHESIS)
            return ast_node

        return self.__var_name()

    def __binary_op(self, func, operations):
        left_node = func()

        while self.__curr_token.type_ in operations:
            op_token = self.__curr_token
            self.__eat(op_token.type_)

            left_node = BinaryOpNode(left_node, op_token, right_node=func())

        return left_node

    def __term(self):
        """
        term: factor((MULTIPLICATION | INT_DIVISION | FLOAT_DIVISION | MODULO) factor)*
        """
        return self.__binary_op(
            self.__factor,
            (
                Token.MULTIPLICATION,
                Token.INT_DIVISION,
                Token.FLOAT_DIVISION,
                Token.MODULO,
            ),
        )

    def __arithmetic_expr(self):
        """
        arithmetic_expr: term((PLUS | MINUS) term)*
        """
        return self.__binary_op(self.__term, (Token.PLUS, Token.MINUS))

    def __comparison_expr(self):
        """
        comparison_expr: K_NOT comparison_expr |
                         arithmetic_expr ((EQUALS | NOT_EQUALS | LESS_THAN
                                                  | LESS_THAN_OR_EQUALS
                                                  | GREATER_THAN
                                                  | GREATER_THAN_OR_EQUALS) arithmetic_expr)*
        """
        if self.__curr_token.type_ == Token.K_NOT:
            op_token = self.__curr_token
            self.__eat(Token.K_NOT)

            return UnaryOpNode(op_token, self.__comparison_expr())

        return self.__binary_op(
            self.__arithmetic_expr,
            (
                Token.EQUALS,
                Token.NOT_EQUALS,
                Token.LESS_THAN,
                Token.LESS_THAN_OR_EQUALS,
                Token.GREATER_THAN,
                Token.GREATER_THAN_OR_EQUALS,
            ),
        )

    def __logical_expr(self):
        """
        logical_expr: comparison_expr ((K_AND | K_OR) comparison_expr)*
        """
        return self.__binary_op(
            self.__comparison_expr,
            (Token.K_AND, Token.K_OR),
        )

    def __empty_statement(self):
        """
        empty_statement:
        Indicates that the statement list is ended.
        """
        return EmptyStatementNode()

    def __assign_statement(self):
        """
        assign_statement: var_name (ASSIGN | PLUS_ASSIGN | MINUS_ASSIGN | MULTIPLICATION_ASSIGN
                                    | FLOAT_DIVISION_ASSIGN | INT_DIVISION_ASSIGN | MODULO_ASSIGN) expr
        """
        left_node = self.__var_name()
        op_token = self.__curr_token

        match (op_token.type_):
            case Token.PLUS_ASSIGN:
                self.__eat(Token.PLUS_ASSIGN)
                right_node = BinaryOpNode(
                    left_node, Token(Token.PLUS, "+"), self.__logical_expr()
                )

            case Token.MINUS_ASSIGN:
                self.__eat(Token.MINUS_ASSIGN)
                right_node = BinaryOpNode(
                    left_node, Token(Token.MINUS, "-"), self.__logical_expr()
                )

            case Token.MULTIPLICATION_ASSIGN:
                self.__eat(Token.MULTIPLICATION_ASSIGN)
                right_node = BinaryOpNode(
                    left_node, Token(Token.MULTIPLICATION, "*"), self.__logical_expr()
                )

            case Token.INT_DIVISION_ASSIGN:
                self.__eat(Token.INT_DIVISION_ASSIGN)
                right_node = BinaryOpNode(
                    left_node, Token(Token.INT_DIVISION, "//"), self.__logical_expr()
                )

            case Token.FLOAT_DIVISION_ASSIGN:
                self.__eat(Token.FLOAT_DIVISION_ASSIGN)
                right_node = BinaryOpNode(
                    left_node, Token(Token.FLOAT_DIVISION, "/"), self.__logical_expr()
                )

            case Token.MODULO_ASSIGN:
                self.__eat(Token.MODULO_ASSIGN)
                right_node = BinaryOpNode(
                    left_node, Token(Token.MODULO, "%"), self.__logical_expr()
                )

            case _:
                self.__eat(Token.ASSIGN)
                right_node = self.__logical_expr()

        return AssignmentStatementNode(left_node, op_token, right_node)

    def __func_call_statement(self):
        """
        func_call_statement: IDENTIFIER LEFT_PARENTHESIS (logical_expr (COMMA logical_expr)*)? RIGHT_PARENTHESIS
        """
        func_token = self.__curr_token
        func_name = self.__curr_token.val

        self.__eat(Token.IDENTIFIER)
        self.__eat(Token.LEFT_PARENTHESIS)

        args = []

        if self.__curr_token.type_ != Token.RIGHT_PARENTHESIS:
            args.append(self.__logical_expr())

            while self.__curr_token.type_ == Token.COMMA:
                self.__eat(Token.COMMA)
                args.append(self.__logical_expr())

        self.__eat(Token.RIGHT_PARENTHESIS)

        return FuncCallStatementNode(func_name, args, func_token)

    def __conditional_statement(self):
        """
        conditional_statement: K_IF LEFT_PARENTHESIS logical_expr RIGHT_PARENTHESIS LEFT_CURLY_BRACKET statement_list RIGHT_CURLY_BRACKET
                               (K_ELSEIF LEFT_PARENTHESIS logical_expr RIGHT_PARENTHESIS LEFT_CURLY_BRACKET statement_list RIGHT_CURLY_BRACKET)*
                               (K_ELSE LEFT_CURLY_BRACKET statement_list RIGHT_CURLY_BRACKET)?
        """
        if_cases = []
        else_case = None

        self.__eat(Token.K_IF)
        self.__eat(Token.LEFT_PARENTHESIS)

        condition_node = self.__logical_expr()
        self.__eat(Token.RIGHT_PARENTHESIS)

        self.__eat(Token.LEFT_CURLY_BRACKET)
        if_cases.append((condition_node, self.__statement_list()))
        self.__eat(Token.RIGHT_CURLY_BRACKET)

        while self.__curr_token.type_ == Token.K_ELSEIF:
            self.__eat(Token.K_ELSEIF)
            self.__eat(Token.LEFT_PARENTHESIS)

            condition_node = self.__logical_expr()
            self.__eat(Token.RIGHT_PARENTHESIS)

            self.__eat(Token.LEFT_CURLY_BRACKET)
            if_cases.append((condition_node, self.__statement_list()))
            self.__eat(Token.RIGHT_CURLY_BRACKET)

        if self.__curr_token.type_ == Token.K_ELSE:
            self.__eat(Token.K_ELSE)

            self.__eat(Token.LEFT_CURLY_BRACKET)
            else_case = self.__statement_list()
            self.__eat(Token.RIGHT_CURLY_BRACKET)

        return ConditionalStatementNode(
            if_cases,
            else_case,
        )

    def __while_statement(self):
        """
        while_statement: K_WHILE LEFT_PARENTHESIS logical_expr RIGHT_PARENTHESIS
                         LEFT_CURLY_BRACKET statement_list RIGHT_CURLY_BRACKET
        """
        self.__eat(Token.K_WHILE)
        self.__eat(Token.LEFT_PARENTHESIS)

        condition_node = self.__logical_expr()
        self.__eat(Token.RIGHT_PARENTHESIS)

        self.__eat(Token.LEFT_CURLY_BRACKET)
        statement_list = self.__statement_list()
        self.__eat(Token.RIGHT_CURLY_BRACKET)

        return WhileStatementNode(condition_node, statement_list)

    def __range_expr(self):
        """
        range_expr: K_RANGE LEFT_PARENTHESIS logical_expr COMMA logical_expr (COMMA logical_expr)? RIGHT_PARENTHESIS
        """
        self.__eat(Token.K_RANGE)
        self.__eat(Token.LEFT_PARENTHESIS)

        start_node = self.__logical_expr()
        self.__eat(Token.COMMA)

        end_node = self.__logical_expr()
        step_node = None

        if self.__curr_token.type_ == Token.COMMA:
            self.__eat(Token.COMMA)
            step_node = self.__logical_expr()

        self.__eat(Token.RIGHT_PARENTHESIS)
        return RangeExprNode(start_node, end_node, step_node)

    def __for_statement(self):
        """
        for_statement: K_FOR LEFT_PARENTHESIS K_VAR LEFT_PARENTHESIS var_type RIGHT_PARENTHESIS var_name
                       K_FROM (range_expr | logical_expr) RIGHT_PARENTHESIS
                       LEFT_CURLY_BRACKET statement_list RIGHT_CURLY_BRACKET
        """
        self.__eat(Token.K_FOR)
        self.__eat(Token.LEFT_PARENTHESIS)

        self.__eat(Token.K_VAR)
        self.__eat(Token.LEFT_PARENTHESIS)

        type_node = self.__var_type()
        self.__eat(Token.RIGHT_PARENTHESIS)

        var_node = self.__var_name()
        var_decl = VarDeclStatementNode(type_node, [var_node])
        self.__eat(Token.K_FROM)

        iterable = (
            self.__range_expr()
            if self.__curr_token.type_ == Token.K_RANGE
            else self.__logical_expr()
        )
        self.__eat(Token.RIGHT_PARENTHESIS)

        self.__eat(Token.LEFT_CURLY_BRACKET)
        statement_list = self.__statement_list()
        self.__eat(Token.RIGHT_CURLY_BRACKET)

        return ForStatementNode(var_decl, iterable, statement_list)

    def __var_type(self):
        """
        var_type: K_INT | K_FLOAT | K_BOOL | K_STR
        """
        token = self.__curr_token

        match token.type_:
            case Token.K_INT:
                self.__eat(Token.K_INT)
                return VarTypeNode(token)

            case Token.K_FLOAT:
                self.__eat(Token.K_FLOAT)
                return VarTypeNode(token)

            case Token.K_BOOL:
                self.__eat(Token.K_BOOL)
                return VarTypeNode(token)

            case _:
                self.__eat(Token.K_STR)
                return VarTypeNode(token)

    def __var_decl_statement(self):
        """
        var_decl_statement: K_VAR LEFT_PARENTHESIS var_type RIGHT_PARENTHESIS
                            var_name (ASSIGN expr)? (COMMA var_name (ASSIGN expr)?)*
        """
        self.__eat(Token.K_VAR)
        self.__eat(Token.LEFT_PARENTHESIS)
        type_node = self.__var_type()
        var_decl_statement_node = VarDeclStatementNode(type_node, [])
        self.__eat(Token.RIGHT_PARENTHESIS)

        variable = self.__var_name()

        if self.__curr_token.type_ == Token.ASSIGN:
            op_token = self.__curr_token
            self.__eat(Token.ASSIGN)

            right_node = self.__logical_expr()
            var_decl_statement_node.variables.append(
                AssignmentStatementNode(variable, op_token, right_node)
            )
        else:
            var_decl_statement_node.variables.append(variable)

        while self.__curr_token.type_ == Token.COMMA:
            self.__eat(Token.COMMA)
            variable = self.__var_name()

            if self.__curr_token.type_ == Token.ASSIGN:
                op_token = self.__curr_token
                self.__eat(Token.ASSIGN)

                right_node = self.__logical_expr()
                var_decl_statement_node.variables.append(
                    AssignmentStatementNode(variable, op_token, right_node)
                )
            else:
                var_decl_statement_node.variables.append(variable)

        return var_decl_statement_node

    def __return_type(self):
        """
        return_type: K_INT | K_FLOAT | K_BOOL | K_STR | K_VOID
        """
        token = self.__curr_token

        if token.type_ == Token.K_VOID:
            self.__eat(Token.K_VOID)
            return ReturnTypeNode(token)

        return ReturnTypeNode(self.__var_type().token)

    def __func_param(self):
        """
        func_param = K_VAR LEFT_PARENTHESIS var_type RIGHT_PARENTHESIS var_name (ASSIGN expr)?
        """
        self.__eat(Token.K_VAR)
        self.__eat(Token.LEFT_PARENTHESIS)

        type_node = self.__var_type()
        self.__eat(Token.RIGHT_PARENTHESIS)

        var_node = self.__var_name()

        if self.__curr_token.type_ == Token.ASSIGN:
            op_token = self.__curr_token
            self.__eat(Token.ASSIGN)

            right_node = self.__logical_expr()
            return FuncParamNode(
                type_node, AssignmentStatementNode(var_node, op_token, right_node)
            )

        return FuncParamNode(type_node, var_node)

    def __func_params(self):
        """
        func_params: func_param (COMMA func_param)*
        """
        func_params = [self.__func_param()]

        while self.__curr_token.type_ == Token.COMMA:
            self.__eat(Token.COMMA)
            func_params.append(self.__func_param())

        return func_params

    def __func_decl_statement(self):
        """
        func_decl_statement: K_FUNC LEFT_PARENTHESIS return_type RIGHT_PARENTHESIS IDENTIFIER
                             LEFT_PARENTHESIS (func_params)? RIGHT_PARENTHESIS
                             LEFT_CURLY_BRACKET statement_list RIGHT_CURLY_BRACKET
        """
        self.__eat(Token.K_FUNC)
        self.__eat(Token.LEFT_PARENTHESIS)

        return_type = self.__return_type()
        self.__eat(Token.RIGHT_PARENTHESIS)

        func_name = self.__curr_token.val
        self.__eat(Token.IDENTIFIER)

        self.__eat(Token.LEFT_PARENTHESIS)
        func_params = (
            self.__func_params()
            if self.__curr_token.type_ != Token.RIGHT_PARENTHESIS
            else []
        )
        self.__eat(Token.RIGHT_PARENTHESIS)

        self.__eat(Token.LEFT_CURLY_BRACKET)
        statement_list = self.__statement_list()
        self.__eat(Token.RIGHT_CURLY_BRACKET)

        return FuncDeclStatementNode(
            return_type, func_name, func_params, statement_list
        )

    def __statement(self):
        """
        statement: func_decl_statement | var_decl_statement SEMI_COLON |
                   for_statement | while_loop_statement | conditional_statement |
                   func_call_statement SEMI_COLON | assignment_statement SEMI_COLON | empty_statement
        """
        if self.__curr_token.type_ == Token.K_FUNC:
            return self.__func_decl_statement()

        if self.__curr_token.type_ == Token.K_VAR:
            curr_statement = self.__var_decl_statement()
            self.__eat(Token.SEMI_COLON)
            return curr_statement

        if self.__curr_token.type_ == Token.K_FOR:
            return self.__for_statement()

        if self.__curr_token.type_ == Token.K_WHILE:
            return self.__while_statement()

        if self.__curr_token.type_ == Token.K_IF:
            return self.__conditional_statement()

        if (
            self.__curr_token.type_ == Token.IDENTIFIER
            and self.__lexer.curr_char == "("
        ):
            curr_statement = self.__func_call_statement()
            self.__eat(Token.SEMI_COLON)
            return curr_statement

        if self.__curr_token.type_ == Token.IDENTIFIER:
            curr_statement = self.__assign_statement()
            self.__eat(Token.SEMI_COLON)
            return curr_statement

        return self.__empty_statement()

    def __statement_list(self):
        """
        statement_list: statement statement_list | empty_statement
        """
        statment_list_node = StatementListNode()
        curr_statement = self.__statement()
        statment_list_node.statements.append(curr_statement)

        while not isinstance(curr_statement, EmptyStatementNode):
            curr_statement = self.__statement()
            statment_list_node.statements.append(curr_statement)

        return statment_list_node

    def __program(self):
        """
        program: statement_list
        """
        return ProgramNode(self.__statement_list())
