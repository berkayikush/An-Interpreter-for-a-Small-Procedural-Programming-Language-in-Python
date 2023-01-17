from .abstract_syntax_tree import AssignStatementNode
from .tokens import Token
from .visit_ast_node import ASTNodeVisitor


class Interpreter(ASTNodeVisitor):
    GLOBAL_MEMORY = {}

    def __init__(self, ast):
        self.__ast = ast

    def interpret(self):
        if self.__ast is None:
            return ""

        return self.visit(self.__ast)

    def visitVarNode(self, ast_node):
        return Interpreter.GLOBAL_MEMORY.get(ast_node.value)

    def visitNumberNode(self, ast_node):
        return ast_node.value

    def visitUnaryOpNode(self, ast_node):
        match (ast_node.op_token.type_):
            case Token.PLUS:
                return +self.visit(ast_node.child_node)
            case Token.MINUS:
                return -self.visit(ast_node.child_node)

    def visitBinaryOpNode(self, ast_node):
        match (ast_node.op_token.type_):
            case Token.PLUS:
                return self.visit(ast_node.left_node) + self.visit(ast_node.right_node)
            case Token.MINUS:
                return self.visit(ast_node.left_node) - self.visit(ast_node.right_node)
            case Token.MULTIPLICATION:
                return self.visit(ast_node.left_node) * self.visit(ast_node.right_node)
            case Token.INT_DIVISION:
                return self.visit(ast_node.left_node) // self.visit(ast_node.right_node)
            case Token.FLOAT_DIVISION:
                return self.visit(ast_node.left_node) / self.visit(ast_node.right_node)
            case Token.MODULO:
                return self.visit(ast_node.left_node) % self.visit(ast_node.right_node)

    def visitEmptyStatementNode(self, ast_node):
        pass

    def visitAssignStatementNode(self, ast_node):
        """
        Create a dictionary in the GLOBAL_SCOPE of the parser and assign the value of the right node to the left node.
        So that we can keep track of the variables and their values.
        """
        Interpreter.GLOBAL_MEMORY[ast_node.left_node.value] = self.visit(
            ast_node.right_node
        )

    def visitVarTypeNode(self, ast_node):
        pass

    def visitVarDeclarationStatementNode(self, ast_node):
        for variable in ast_node.variables:
            if isinstance(variable, AssignStatementNode):
                self.visit(variable)

    def visitStatementListNode(self, ast_node):
        for statement in ast_node.statements:
            self.visit(statement)

    def visitProgramNode(self, ast_node):
        self.visit(ast_node.statement_list_node)
