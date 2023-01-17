from project_code.abstract_syntax_tree import (
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
from project_code.lexer import Lexer
from project_code.parser_ import Parser


class TestParser:
    def test_empty(self):
        text = """
        """
        lexer = Lexer(text)
        parser = Parser(lexer)
        ast_node = parser.parse()

        assert isinstance(ast_node, ProgramNode)
        assert isinstance(ast_node.statement_list_node, StatementListNode)
        assert isinstance(
            ast_node.statement_list_node.statements[0], EmptyStatementNode
        )

    def test_variable_declaration(self):
        text = """
        var(int) a;
        """
        lexer = Lexer(text)
        parser = Parser(lexer)
        ast_node = parser.parse()

        assert isinstance(ast_node, ProgramNode)
        assert isinstance(ast_node.statement_list_node, StatementListNode)
        assert isinstance(
            ast_node.statement_list_node.statements[0], VarDeclarationStatementNode
        )

        assert isinstance(
            ast_node.statement_list_node.statements[0].var_type_node, VarTypeNode
        )
        assert ast_node.statement_list_node.statements[0].var_type_node.value == "int"

        assert isinstance(
            ast_node.statement_list_node.statements[0].variables[0], VarNode
        )
        assert ast_node.statement_list_node.statements[0].variables[0].value == "a"

    def test_variable_declaration_multiple(self):
        text = """
        var(int) a, b;
        """
        lexer = Lexer(text)
        parser = Parser(lexer)
        ast_node = parser.parse()

        assert isinstance(ast_node, ProgramNode)
        assert isinstance(ast_node.statement_list_node, StatementListNode)
        assert isinstance(
            ast_node.statement_list_node.statements[0], VarDeclarationStatementNode
        )
        assert isinstance(
            ast_node.statement_list_node.statements[0].var_type_node, VarTypeNode
        )
        assert ast_node.statement_list_node.statements[0].var_type_node.value == "int"
        assert isinstance(
            ast_node.statement_list_node.statements[0].variables[0], VarNode
        )
        assert ast_node.statement_list_node.statements[0].variables[0].value == "a"
        assert isinstance(
            ast_node.statement_list_node.statements[0].variables[1], VarNode
        )
        assert ast_node.statement_list_node.statements[0].variables[1].value == "b"

    def test_variable_declaration_with_unary_op(self):
        text = """
        var(int) a = -1;
        """
        lexer = Lexer(text)
        parser = Parser(lexer)
        ast_node = parser.parse()

        assert isinstance(ast_node, ProgramNode)
        assert isinstance(ast_node.statement_list_node, StatementListNode)
        assert isinstance(
            ast_node.statement_list_node.statements[0], VarDeclarationStatementNode
        )
        assert isinstance(
            ast_node.statement_list_node.statements[0].var_type_node, VarTypeNode
        )
        assert ast_node.statement_list_node.statements[0].var_type_node.value == "int"
        assert isinstance(
            ast_node.statement_list_node.statements[0].variables[0], AssignStatementNode
        )
        assert isinstance(
            ast_node.statement_list_node.statements[0].variables[0].left_node,
            VarNode,
        )
        assert (
            ast_node.statement_list_node.statements[0].variables[0].left_node.value
            == "a"
        )
        assert isinstance(
            ast_node.statement_list_node.statements[0].variables[0].right_node,
            UnaryOpNode,
        )
        assert (
            ast_node.statement_list_node.statements[0]
            .variables[0]
            .right_node.op_token.type_
            == "MINUS"
        )
        assert isinstance(
            ast_node.statement_list_node.statements[0]
            .variables[0]
            .right_node.child_node,
            NumberNode,
        )
        assert (
            ast_node.statement_list_node.statements[0]
            .variables[0]
            .right_node.child_node.value
            == 1
        )

    def test_variable_declaration_multiple_with_assign(self):
        text = """
        var( int ) a = 1, b = 2.5;
        """
        lexer = Lexer(text)
        parser = Parser(lexer)
        ast_node = parser.parse()

        assert isinstance(ast_node, ProgramNode)
        assert isinstance(ast_node.statement_list_node, StatementListNode)
        assert isinstance(
            ast_node.statement_list_node.statements[0], VarDeclarationStatementNode
        )
        assert isinstance(
            ast_node.statement_list_node.statements[0].var_type_node, VarTypeNode
        )
        assert ast_node.statement_list_node.statements[0].var_type_node.value == "int"
        assert isinstance(
            ast_node.statement_list_node.statements[0].variables[0], AssignStatementNode
        )
        assert isinstance(
            ast_node.statement_list_node.statements[0].variables[0].left_node,
            VarNode,
        )
        assert (
            ast_node.statement_list_node.statements[0].variables[0].left_node.value
            == "a"
        )
        assert isinstance(
            ast_node.statement_list_node.statements[0].variables[0].right_node,
            NumberNode,
        )
        assert (
            ast_node.statement_list_node.statements[0].variables[0].right_node.value
            == 1
        )
        assert isinstance(
            ast_node.statement_list_node.statements[0].variables[1], AssignStatementNode
        )
        assert isinstance(
            ast_node.statement_list_node.statements[0].variables[1].left_node,
            VarNode,
        )
        assert (
            ast_node.statement_list_node.statements[0].variables[1].left_node.value
            == "b"
        )

        assert isinstance(
            ast_node.statement_list_node.statements[0].variables[1].right_node,
            NumberNode,
        )
        assert (
            ast_node.statement_list_node.statements[0].variables[1].right_node.value
            == 2.5
        )

    def test_assign_statement(self):
        text = """
        a = 1;
        """
        lexer = Lexer(text)
        parser = Parser(lexer)
        ast_node = parser.parse()

        assert isinstance(ast_node, ProgramNode)
        assert isinstance(ast_node.statement_list_node, StatementListNode)
        assert isinstance(
            ast_node.statement_list_node.statements[0], AssignStatementNode
        )
        assert isinstance(ast_node.statement_list_node.statements[0].left_node, VarNode)
        assert ast_node.statement_list_node.statements[0].left_node.value == "a"

        assert isinstance(
            ast_node.statement_list_node.statements[0].right_node, NumberNode
        )
        assert ast_node.statement_list_node.statements[0].right_node.value == 1

    def test_assign_statement_with_operation(self):
        text = """
        a = 1 + 2;
        """
        lexer = Lexer(text)
        parser = Parser(lexer)
        ast_node = parser.parse()

        assert isinstance(ast_node, ProgramNode)
        assert isinstance(ast_node.statement_list_node, StatementListNode)
        assert isinstance(
            ast_node.statement_list_node.statements[0], AssignStatementNode
        )
        assert isinstance(ast_node.statement_list_node.statements[0].left_node, VarNode)
        assert ast_node.statement_list_node.statements[0].left_node.value == "a"

        assert isinstance(
            ast_node.statement_list_node.statements[0].right_node, BinaryOpNode
        )
        assert (
            ast_node.statement_list_node.statements[0].right_node.op_token.value == "+"
        )

        assert isinstance(
            ast_node.statement_list_node.statements[0].right_node.left_node, NumberNode
        )
        assert (
            ast_node.statement_list_node.statements[0].right_node.left_node.value == 1
        )

        assert isinstance(
            ast_node.statement_list_node.statements[0].right_node.right_node,
            NumberNode,
        )
        assert (
            ast_node.statement_list_node.statements[0].right_node.right_node.value == 2
        )

    def test_assign_statement_with_multiple_operations(self):
        text = """
        a = 1 + 2 * 3;
        """
        lexer = Lexer(text)
        parser = Parser(lexer)
        ast_node = parser.parse()

        assert isinstance(ast_node, ProgramNode)
        assert isinstance(ast_node.statement_list_node, StatementListNode)
        assert isinstance(
            ast_node.statement_list_node.statements[0], AssignStatementNode
        )
        assert isinstance(ast_node.statement_list_node.statements[0].left_node, VarNode)
        assert ast_node.statement_list_node.statements[0].left_node.value == "a"

        assert isinstance(
            ast_node.statement_list_node.statements[0].right_node, BinaryOpNode
        )
        assert (
            ast_node.statement_list_node.statements[0].right_node.op_token.value == "+"
        )
        assert isinstance(
            ast_node.statement_list_node.statements[0].right_node.left_node, NumberNode
        )
        assert (
            ast_node.statement_list_node.statements[0].right_node.left_node.value == 1
        )
        assert isinstance(
            ast_node.statement_list_node.statements[0].right_node.right_node,
            BinaryOpNode,
        )
        assert (
            ast_node.statement_list_node.statements[
                0
            ].right_node.right_node.op_token.value
            == "*"
        )
        assert isinstance(
            ast_node.statement_list_node.statements[0].right_node.right_node.left_node,
            NumberNode,
        )
        assert (
            ast_node.statement_list_node.statements[
                0
            ].right_node.right_node.left_node.value
            == 2
        )
        assert isinstance(
            ast_node.statement_list_node.statements[0].right_node.right_node.right_node,
            NumberNode,
        )
        assert (
            ast_node.statement_list_node.statements[
                0
            ].right_node.right_node.right_node.value
            == 3
        )

    def test_int_division_assign_statement(self):
        text = """
        a //= 1;
        """
        lexer = Lexer(text)
        parser = Parser(lexer)
        ast_node = parser.parse()

        assert isinstance(ast_node, ProgramNode)
        assert isinstance(ast_node.statement_list_node, StatementListNode)
        assert isinstance(
            ast_node.statement_list_node.statements[0], AssignStatementNode
        )
        assert isinstance(ast_node.statement_list_node.statements[0].left_node, VarNode)
        assert ast_node.statement_list_node.statements[0].left_node.value == "a"
        assert isinstance(
            ast_node.statement_list_node.statements[0].right_node, BinaryOpNode
        )
        assert isinstance(
            ast_node.statement_list_node.statements[0].right_node.left_node,
            VarNode,
        )
        assert (
            ast_node.statement_list_node.statements[0].right_node.left_node.value == "a"
        )
        assert isinstance(
            ast_node.statement_list_node.statements[0].right_node.right_node, NumberNode
        )
        assert (
            ast_node.statement_list_node.statements[0].right_node.right_node.value == 1
        )
        assert (
            ast_node.statement_list_node.statements[0].right_node.op_token.value == "//"
        )

    def test_statement_with_comment(self):
        text = """
        a = 1; /* this is a comment */
        """
        lexer = Lexer(text)
        parser = Parser(lexer)
        ast_node = parser.parse()

        assert isinstance(ast_node, ProgramNode)
        assert isinstance(ast_node.statement_list_node, StatementListNode)
        assert isinstance(
            ast_node.statement_list_node.statements[0], AssignStatementNode
        )
        assert isinstance(ast_node.statement_list_node.statements[0].left_node, VarNode)
        assert ast_node.statement_list_node.statements[0].left_node.value == "a"
        assert isinstance(
            ast_node.statement_list_node.statements[0].right_node, NumberNode
        )
        assert ast_node.statement_list_node.statements[0].right_node.value == 1
