from .tokens import Token
from .abstract_syntax_tree import VarNode
from .visit_ast_node import ASTNodeVisitor
from .scope_symbol_table import (
    ScopeSymbolTable,
    BuiltInTypeSymbol,
    VariableSymbol,
    IfElseIfElseSymbol,
)


class SemanticAnalyzer(ASTNodeVisitor):
    def __init__(self):
        self.__current_scope_symbol_table = ScopeSymbolTable(
            scope_name="global", scope_level=1, outside_scope=None
        )

    def visitVarNode(self, ast_node):
        variable_symbol = self.__current_scope_symbol_table.get_symbol(ast_node.value)

        if variable_symbol is None:
            raise NameError(f"Identifier {ast_node.value} is not defined.")

    def visitNumberNode(self, ast_node):
        pass

    def visitBoolNode(self, ast_node):
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

    def __add_symbols_to_current_scope(self, ast_node, symbol_names):
        for i, (condition, _) in enumerate(ast_node.if_cases):
            self.visit(condition)
            name, type_ = ("if", Token.K_IF) if i == 0 else ("elseif", Token.K_ELSEIF)

            if_elseif_symbol = IfElseIfElseSymbol(name, BuiltInTypeSymbol(type_))
            symbol_names.append(if_elseif_symbol.name)

            self.__current_scope_symbol_table.add_symbol(if_elseif_symbol)

        if ast_node.else_case is not None:
            else_symbol = IfElseIfElseSymbol("else", BuiltInTypeSymbol(Token.K_ELSE))
            symbol_names.append(else_symbol.name)

            self.__current_scope_symbol_table.add_symbol(else_symbol)

    def visitIfStatementNode(self, ast_node):
        symbol_names = []
        self.__add_symbols_to_current_scope(ast_node, symbol_names)

        for i, (_, statement_list) in enumerate(ast_node.if_cases):
            self.__current_scope_symbol_table = ScopeSymbolTable(
                scope_name=symbol_names[i],
                scope_level=self.__current_scope_symbol_table.scope_level + 1,
                outside_scope=self.__current_scope_symbol_table,
            )

            self.visit(statement_list)
            print(self.__current_scope_symbol_table)
            self.__current_scope_symbol_table = (
                self.__current_scope_symbol_table.outside_scope
            )

        if ast_node.else_case is not None:
            self.__current_scope_symbol_table = ScopeSymbolTable(
                scope_name=symbol_names[-1],
                scope_level=self.__current_scope_symbol_table.scope_level + 1,
                outside_scope=self.__current_scope_symbol_table,
            )

            self.visit(ast_node.else_case)
            print(self.__current_scope_symbol_table)
            self.__current_scope_symbol_table = (
                self.__current_scope_symbol_table.outside_scope
            )

    def visitVarDeclStatementNode(self, ast_node):
        type_symbol = self.__current_scope_symbol_table.get_symbol(
            ast_node.var_type_node.value
        )

        for variable in ast_node.variables:
            if isinstance(variable, VarNode):
                variable_name = variable.value
            else:
                self.visit(variable.right_node)
                variable_name = variable.left_node.value

            variable_symbol = VariableSymbol(variable_name, type_symbol)

            if (
                self.__current_scope_symbol_table.get_symbol(
                    variable_name, check_outside_scope=False
                )
                is not None
            ):
                raise NameError(f"Identifier {variable_name} is already defined.")

            self.__current_scope_symbol_table.add_symbol(variable_symbol)

    def visitStatementListNode(self, ast_node):
        for statement in ast_node.statements:
            self.visit(statement)

    def visitProgramNode(self, ast_node):
        global_scope = self.__current_scope_symbol_table
        self.visit(ast_node.statement_list_node)
        self.__current_scope_symbol_table = (
            self.__current_scope_symbol_table.outside_scope
        )
        print(global_scope)
