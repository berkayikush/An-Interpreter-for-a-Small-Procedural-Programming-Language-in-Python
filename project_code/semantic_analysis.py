from .abstract_syntax_tree import VarNode
from .visit_ast_node import ASTNodeVisitor
from .scope_symbol_table import ScopeSymbolTable, VariableSymbol


class SemanticAnalyzer(ASTNodeVisitor):
    def __init__(self):
        self.__scope_symbol_table = ScopeSymbolTable(scope_name="global", scope_level=1)

    def visitVarNode(self, ast_node):
        variable_symbol = self.__scope_symbol_table.get_symbol(ast_node.value)

        if variable_symbol is None:
            raise NameError(f"Identifier {ast_node.value} is not defined.")

    def visitNumberNode(self, ast_node):
        pass

    def visitUnaryOpNode(self, ast_node):
        self.visit(ast_node.child_node)

    def visitBinaryOpNode(self, ast_node):
        self.visit(ast_node.left_node)
        self.visit(ast_node.right_node)

    def visitEmptyStatementNode(self, ast_node):
        pass

    def visitAssignStatementNode(self, ast_node):
        self.visit(ast_node.right_node)
        self.visit(ast_node.left_node)

    def visitVarDeclarationStatementNode(self, ast_node):
        type_symbol = self.__scope_symbol_table.get_symbol(ast_node.var_type_node.value)

        for variable in ast_node.variables:
            if isinstance(variable, VarNode):
                variable_name = variable.value
            else:
                variable_name = variable.left_node.value

            variable_symbol = VariableSymbol(variable_name, type_symbol)

            if self.__scope_symbol_table.get_symbol(variable_name) is not None:
                raise NameError(f"Identifier {variable_name} is already defined.")

            self.__scope_symbol_table.add_symbol(variable_symbol)

    def visitStatementListNode(self, ast_node):
        for statement in ast_node.statements:
            self.visit(statement)

    def visitProgramNode(self, ast_node):
        self.visit(ast_node.statement_list_node)
