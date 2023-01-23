from .tokens import Token
from .abstract_syntax_tree import (
    VarNode,
    NumberNode,
    BoolNode,
    UnaryOpNode,
    BinaryOpNode,
    EmptyStatementNode,
    AssignStatementNode,
    ConditionalStatementNode,
    WhileStatementNode,
    ForStatementNode,
    VarTypeNode,
    VarDeclStatementNode,
    StatementListNode,
    ProgramNode,
)
from .error import ParserError


class Parser:
    def __init__(self, lexer):
        self.__lexer = lexer
        self.__current_token = self.__lexer.get_next_token()

    def parse(self):
        ast_node = self.__program()

        if self.__current_token.type_ != Token.EOF:
            self.__error()

        return ast_node

    def __eat(self, token_type):
        """
        Verify that the current token matches the passed token type.
        If it does, then "eat" the current token and assign the next.
        """
        if self.__current_token.type_ == token_type:
            self.__current_token = self.__lexer.get_next_token()
            return

        self.__error()

    def __error(self):
        raise ParserError(
            error_message=f"{ParserError.UNEXPECTED_TOKEN}: {self.__current_token}",
            value=self.__current_token,
        )

    def __variable_name(self):
        """
        variable_name: IDENTIFIER
        """
        token = self.__current_token
        self.__eat(Token.IDENTIFIER)
        return VarNode(var_token=token)

    def __factor(self):
        """
        factor : (INT | FLOAT)
                 | BOOL
                 | LEFT_PARENTHESIS logical_expr RIGHT_PARENTHESIS
                 | (PLUS | MINUS) factor
                 | variable_name
        """
        token = self.__current_token

        if token.type_ in (Token.INT, Token.FLOAT):
            self.__eat(token.type_)
            return NumberNode(num_token=token)

        if token.type_ == Token.BOOL:
            self.__eat(token.type_)
            return BoolNode(bool_token=token)

        if token.type_ in (Token.PLUS, Token.MINUS):
            self.__eat(token.type_)
            return UnaryOpNode(op_token=token, child_node=self.__factor())

        if token.type_ == Token.LEFT_PARENTHESIS:
            self.__eat(Token.LEFT_PARENTHESIS)
            ast_node = self.__logical_expr()

            self.__eat(Token.RIGHT_PARENTHESIS)
            return ast_node

        return self.__variable_name()

    def __binary_op(self, func, operations):
        left_node = func()

        while self.__current_token.type_ in operations:
            op_token = self.__current_token
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
        if self.__current_token.type_ == Token.K_NOT:
            op_token = self.__current_token
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
        States that the statement list is ended.
        """
        return EmptyStatementNode()

    def __assign_statement(self):
        """
        assign_statement: variable_name (ASSIGN | PLUS_ASSIGN | MINUS_ASSIGN | MULTIPLICATION_ASSIGN | FLOAT_DIVISION_ASSIGN
                                                | INT_DIVISION_ASSIGN
                                                | MODULO_ASSIGN) expr
        """
        left_node = self.__variable_name()
        op_token = self.__current_token

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

        return AssignStatementNode(left_node, op_token, right_node)

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

        while self.__current_token.type_ == Token.K_ELSEIF:
            self.__eat(Token.K_ELSEIF)
            self.__eat(Token.LEFT_PARENTHESIS)

            condition_node = self.__logical_expr()
            self.__eat(Token.RIGHT_PARENTHESIS)

            self.__eat(Token.LEFT_CURLY_BRACKET)
            if_cases.append((condition_node, self.__statement_list()))
            self.__eat(Token.RIGHT_CURLY_BRACKET)

        if self.__current_token.type_ == Token.K_ELSE:
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

    def __for_statement(self):
        """
        for_statement: K_FOR LEFT_PARENTHESIS K_VAR LEFT_PARENTHESIS variable_type RIGHT_PARENTHESIS variable_name
                       K_FROM INT K_TO INT (K_STEP INT)? RIGHT_PARENTHESIS
                       LEFT_CURLY_BRACKET statement_list RIGHT_CURLY_BRACKET
        """
        pass

    def __variable_type(self):
        """
        variable_type: K_INT | K_FLOAT | K_BOOL
        """
        token = self.__current_token

        match token.type_:
            case Token.K_INT:
                self.__eat(Token.K_INT)
                return VarTypeNode(token)

            case Token.K_FLOAT:
                self.__eat(Token.K_FLOAT)
                return VarTypeNode(token)

            case _:
                self.__eat(Token.K_BOOL)
                return VarTypeNode(token)

    def __variable_declaration_statement(self):
        """
        variable_declaration_statement: K_VAR LEFT_PARENTHESIS variable_type RIGHT_PARENTHESIS
                                        variable_name (ASSIGN expr)? (COMMA variable_name (ASSIGN expr)?)*
        """
        self.__eat(Token.K_VAR)
        self.__eat(Token.LEFT_PARENTHESIS)
        type_node = self.__variable_type()
        variable_declaration_statement_node = VarDeclStatementNode(type_node, [])
        self.__eat(Token.RIGHT_PARENTHESIS)

        variable = self.__variable_name()

        if self.__current_token.type_ == Token.ASSIGN:
            op_token = self.__current_token
            self.__eat(Token.ASSIGN)

            right_node = self.__logical_expr()
            variable_declaration_statement_node.variables.append(
                AssignStatementNode(variable, op_token, right_node)
            )
        else:
            variable_declaration_statement_node.variables.append(variable)

        while self.__current_token.type_ == Token.COMMA:
            self.__eat(Token.COMMA)
            variable = self.__variable_name()

            if self.__current_token.type_ == Token.ASSIGN:
                op_token = self.__current_token
                self.__eat(Token.ASSIGN)

                right_node = self.__logical_expr()
                variable_declaration_statement_node.variables.append(
                    AssignStatementNode(variable, op_token, right_node)
                )
            else:
                variable_declaration_statement_node.variables.append(variable)

        return variable_declaration_statement_node

    def __statement(self):
        """
        statement: variable_declaration_statement | while_loop_statement | conditional_statement |
                   assignment_statement | empty_statement
        """
        if self.__current_token.type_ == Token.K_VAR:
            return self.__variable_declaration_statement()

        if self.__current_token.type_ == Token.K_FOR:
            return self.__for_statement()

        if self.__current_token.type_ == Token.K_WHILE:
            return self.__while_statement()

        if self.__current_token.type_ == Token.K_IF:
            return self.__conditional_statement()

        if self.__current_token.type_ == Token.IDENTIFIER:
            return self.__assign_statement()

        return self.__empty_statement()

    def __statement_list(self):
        """
        statement_list: statement | statement SEMI_COLON statement_list
        """
        statment_list_node = StatementListNode()
        statment_list_node.statements.append(self.__statement())

        while self.__current_token.type_ == Token.SEMI_COLON:
            self.__eat(Token.SEMI_COLON)
            statment_list_node.statements.append(self.__statement())

        return statment_list_node

    def __program(self):
        """
        program: statement_list
        """
        return ProgramNode(self.__statement_list())
