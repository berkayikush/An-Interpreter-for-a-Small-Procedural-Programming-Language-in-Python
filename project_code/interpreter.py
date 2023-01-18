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

    def visitBoolNode(self, ast_node):
        if ast_node.value == "true":
            return True

        return False

    def visitUnaryOpNode(self, ast_node):
        match (ast_node.op_token.type_):
            case Token.PLUS:
                return +self.visit(ast_node.child_node)
            case Token.MINUS:
                return -self.visit(ast_node.child_node)
            case Token.K_NOT:
                return not self.visit(ast_node.child_node)

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
            case Token.EQUALS:
                return self.visit(ast_node.left_node) == self.visit(ast_node.right_node)
            case Token.NOT_EQUALS:
                return self.visit(ast_node.left_node) != self.visit(ast_node.right_node)
            case Token.LESS_THAN:
                return self.visit(ast_node.left_node) < self.visit(ast_node.right_node)
            case Token.LESS_THAN_OR_EQUALS:
                return self.visit(ast_node.left_node) <= self.visit(ast_node.right_node)
            case Token.GREATER_THAN:
                return self.visit(ast_node.left_node) > self.visit(ast_node.right_node)
            case Token.GREATER_THAN_OR_EQUALS:
                return self.visit(ast_node.left_node) >= self.visit(ast_node.right_node)
            case Token.K_AND:
                return self.visit(ast_node.left_node) and self.visit(
                    ast_node.right_node
                )
            case Token.K_OR:
                return self.visit(ast_node.left_node) or self.visit(ast_node.right_node)

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

    def visitVarDeclStatementNode(self, ast_node):
        for variable in ast_node.variables:
            if isinstance(variable, AssignStatementNode):
                self.visit(variable)

    def visitStatementListNode(self, ast_node):
        for statement in ast_node.statements:
            self.visit(statement)

    def visitProgramNode(self, ast_node):
        self.visit(ast_node.statement_list_node)
