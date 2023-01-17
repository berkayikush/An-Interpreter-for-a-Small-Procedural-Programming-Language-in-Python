from .tokens import Token
from .abstract_syntax_tree import (
    VarNode,
    NumberNode,
    UnaryOpNode,
    BinaryOpNode,
    EmptyStatementNode,
    AssignStatementNode,
    VarTypeNode,
    VarDeclarationStatementNode,
    StatementListNode,
    ProgramNode,
)


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
        raise Exception("Invalid syntax")

    def __variable_name(self):
        """
        variable_name: IDENTIFIER
        """
        token = self.__current_token
        self.__eat(Token.IDENTIFIER)
        return VarNode(var_token=token)

    def __factor(self):
        """
        factor : (INT | FLOAT) | LEFT_PARENTHESIS expr RIGHT_PARENTHESIS | (PLUS | MINUS) factor | variable_name
        """
        token = self.__current_token

        if token.type_ in (Token.INT, Token.FLOAT):
            self.__eat(token.type_)
            return NumberNode(num_token=token)

        if token.type_ in (Token.PLUS, Token.MINUS):
            self.__eat(token.type_)
            return UnaryOpNode(op_token=token, child_node=self.__factor())

        if token.type_ == Token.LEFT_PARENTHESIS:
            self.__eat(Token.LEFT_PARENTHESIS)
            ast_node = self.__expr()

            self.__eat(Token.RIGHT_PARENTHESIS)
            return ast_node

        return self.__variable_name()

    def __binary_operation(self, func, operations):
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
        return self.__binary_operation(
            self.__factor,
            (
                Token.MULTIPLICATION,
                Token.INT_DIVISION,
                Token.FLOAT_DIVISION,
                Token.MODULO,
            ),
        )

    def __expr(self):
        """
        expr: term((PLUS | MINUS) term)*
        """
        return self.__binary_operation(self.__term, (Token.PLUS, Token.MINUS))

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
                    left_node, Token(Token.PLUS, "+"), self.__expr()
                )

            case Token.MINUS_ASSIGN:
                self.__eat(Token.MINUS_ASSIGN)
                right_node = BinaryOpNode(
                    left_node, Token(Token.MINUS, "-"), self.__expr()
                )

            case Token.MULTIPLICATION_ASSIGN:
                self.__eat(Token.MULTIPLICATION_ASSIGN)
                right_node = BinaryOpNode(
                    left_node, Token(Token.MULTIPLICATION, "*"), self.__expr()
                )

            case Token.INT_DIVISION_ASSIGN:
                self.__eat(Token.INT_DIVISION_ASSIGN)
                right_node = BinaryOpNode(
                    left_node, Token(Token.INT_DIVISION, "//"), self.__expr()
                )

            case Token.FLOAT_DIVISION_ASSIGN:
                self.__eat(Token.FLOAT_DIVISION_ASSIGN)
                right_node = BinaryOpNode(
                    left_node, Token(Token.FLOAT_DIVISION, "/"), self.__expr()
                )

            case Token.MODULO_ASSIGN:
                self.__eat(Token.MODULO_ASSIGN)
                right_node = BinaryOpNode(
                    left_node, Token(Token.MODULO, "%"), self.__expr()
                )

            case _:
                self.__eat(Token.ASSIGN)
                right_node = self.__expr()

        return AssignStatementNode(left_node, op_token, right_node)

    def __variable_type(self):
        """
        variable_type: K_INT | K_FLOAT
        """
        token = self.__current_token

        match token.type_:
            case Token.K_INT:
                self.__eat(Token.K_INT)
                return VarTypeNode(token)

            case _:
                self.__eat(Token.K_FLOAT)
                return VarTypeNode(token)

    def __variable_declaration_statement(self):
        """
        variable_declaration_statement: K_VAR LEFT_PARENTHESIS variable_type RIGHT_PARENTHESIS
                                        variable_name (ASSIGN expr)? (COMMA variable_name (ASSIGN expr)?)*
        """
        self.__eat(Token.K_VAR)
        self.__eat(Token.LEFT_PARENTHESIS)
        type_node = self.__variable_type()
        variable_declaration_statement_node = VarDeclarationStatementNode(type_node, [])
        self.__eat(Token.RIGHT_PARENTHESIS)

        variable = self.__variable_name()

        if self.__current_token.type_ == Token.ASSIGN:
            op_token = self.__current_token
            self.__eat(Token.ASSIGN)

            right_node = self.__expr()
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

                right_node = self.__expr()
                variable_declaration_statement_node.variables.append(
                    AssignStatementNode(variable, op_token, right_node)
                )
            else:
                variable_declaration_statement_node.variables.append(variable)

        return variable_declaration_statement_node

    def __statement(self):
        """
        statement: statement: variable_declaration_statement | assignment_statement | empty_statement
        """
        if self.__current_token.type_ == Token.K_VAR:
            return self.__variable_declaration_statement()

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
