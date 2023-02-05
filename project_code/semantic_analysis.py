from .tokens import Token
from .abstract_syntax_tree import AssignmentStatementNode, VarNode
from .visit_ast_node import ASTNodeVisitor
from .scope_symbol_table import (
    ScopeSymbolTable,
    BuiltInTypeSymbol,
    VarSymbol,
    ConditionalSymbol,
    LoopSymbol,
    FuncSymbol,
)
from .type_checking import TypeChecker
from .error import SemnaticError


class SemanticAnalyzer(ASTNodeVisitor):
    def __init__(self):
        self.__curr_scope_symbol_table = ScopeSymbolTable(
            scope_name="global", scope_level=1, outer_scope=None
        )
        self.__curr_scope_symbol_table.add_built_in_symbols()

    def visitVarNode(self, ast_node):
        var_name = ast_node.val
        variable_symbol = self.__curr_scope_symbol_table.get_symbol(var_name)

        if variable_symbol is None:
            self.__error(f'Identifier "{var_name}" not found', ast_node.token)

        return variable_symbol.type_

    def visitNumberNode(self, ast_node):
        if isinstance(ast_node.val, int):
            return BuiltInTypeSymbol(Token.K_INT)

        return BuiltInTypeSymbol(Token.K_FLOAT)

    def visitBoolNode(self, ast_node):
        return BuiltInTypeSymbol(Token.K_BOOL)

    def visitStrNode(self, ast_node):
        return BuiltInTypeSymbol(Token.K_STR)

    def visitUnaryOpNode(self, ast_node):
        return TypeChecker.check_unary_op(
            ast_node.op_token,
            child_node_type=self.visit(ast_node.child_node).name,
        )

    def visitBinaryOpNode(self, ast_node):
        return TypeChecker.check_binary_op(
            ast_node.op_token,
            left_node_type=self.visit(ast_node.left_node).name,
            right_node_type=self.visit(ast_node.right_node).name,
        )

    def visitEmptyStatementNode(self, ast_node):
        pass

    def visitAssignmentStatementNode(self, ast_node):
        TypeChecker.check_assignment_statement(
            var_type=self.visit(ast_node.left_node).name,
            var_val_type=self.visit(ast_node.right_node).name,
            var_val_token=ast_node.right_node.token,
        )

    def visitFuncCallStatementNode(self, ast_node):
        func_symbol = self.__curr_scope_symbol_table.get_symbol(
            f"func_{ast_node.func_name}"
        )

        if func_symbol is None:
            self.__error(f'Function "{ast_node.func_name}" not found', ast_node.token)

        num_args = len(ast_node.args)
        num_params = len(func_symbol.params)

        num_default_params = len(
            [
                filter(
                    lambda param: isinstance(param, AssignmentStatementNode),
                    func_symbol.params,
                )
            ]
        )
        num_non_default_params = num_params - num_default_params

        if num_args not in (num_non_default_params, num_params):
            self.__error(
                f'Function "{ast_node.func_name}" takes from {num_default_params} '
                f"to {num_params} positional arguments but {num_args} were given",
                ast_node.token,
            )

        for i, arg in enumerate(ast_node.args):
            TypeChecker.check_func_call_statement(
                param_type=func_symbol.params[i].type_.name,
                arg_type=self.visit(arg).name,
                func_call_token=arg.token,
            )

    def visitConditionalStatementNode(self, ast_node):
        symbol_names = []
        self.__add_conditional_symbols_to_current_scope(ast_node, symbol_names)

        for i, (_, statement_list_node) in enumerate(ast_node.if_cases):
            self.__curr_scope_symbol_table = ScopeSymbolTable(
                scope_name=symbol_names[i],
                scope_level=self.__curr_scope_symbol_table.scope_level + 1,
                outer_scope=self.__curr_scope_symbol_table,
            )

            self.visit(statement_list_node)
            self.__curr_scope_symbol_table = self.__curr_scope_symbol_table.outer_scope

        if ast_node.else_case is not None:
            self.__curr_scope_symbol_table = ScopeSymbolTable(
                scope_name=symbol_names[-1],
                scope_level=self.__curr_scope_symbol_table.scope_level + 1,
                outer_scope=self.__curr_scope_symbol_table,
            )

            self.visit(ast_node.else_case)
            self.__curr_scope_symbol_table = self.__curr_scope_symbol_table.outer_scope

    def __add_conditional_symbols_to_current_scope(self, ast_node, symbol_names):
        for i, (condition, _) in enumerate(ast_node.if_cases):
            self.visit(condition)
            name = "if" if i == 0 else "elseif"

            if_elseif_symbol = ConditionalSymbol(name)
            symbol_names.append(if_elseif_symbol.name)

            self.__curr_scope_symbol_table.add_symbol(if_elseif_symbol)

        if ast_node.else_case is not None:
            else_symbol = ConditionalSymbol("else")
            symbol_names.append(else_symbol.name)

            self.__curr_scope_symbol_table.add_symbol(else_symbol)

    def visitWhileStatementNode(self, ast_node):
        self.visit(ast_node.condition)

        while_symbol = LoopSymbol("while")
        self.__curr_scope_symbol_table.add_symbol(while_symbol)

        self.__curr_scope_symbol_table = ScopeSymbolTable(
            scope_name=while_symbol.name,
            scope_level=self.__curr_scope_symbol_table.scope_level + 1,
            outer_scope=self.__curr_scope_symbol_table,
        )

        self.visit(ast_node.statement_list_node)
        self.__curr_scope_symbol_table = self.__curr_scope_symbol_table.outer_scope

    def visitRangeExprNode(self, ast_node):
        return TypeChecker.check_range_expr(
            start_type=self.visit(ast_node.start_node).name,
            end_type=self.visit(ast_node.end_node).name,
            step_type=self.visit(ast_node.step_node).name
            if ast_node.step_node
            else None,
            range_token=ast_node.token,
        )

    def visitForStatementNode(self, ast_node):
        iterable_type = self.visit(ast_node.iterable).name
        TypeChecker.check_iterable(iterable_type, ast_node.iterable.token)

        for_symbol = LoopSymbol("for")
        self.__curr_scope_symbol_table.add_symbol(for_symbol)

        self.__curr_scope_symbol_table = ScopeSymbolTable(
            scope_name=for_symbol.name,
            scope_level=self.__curr_scope_symbol_table.scope_level + 1,
            outer_scope=self.__curr_scope_symbol_table,
        )

        self.visit(ast_node.var_decl_statement_node)
        TypeChecker.check_assignment_statement(
            var_type=self.visit(ast_node.var_decl_statement_node.variables[0]).name,
            var_val_type=(
                self.visit(ast_node.iterable.start_node).name
                if iterable_type == Token.K_RANGE
                else iterable_type
            ),
            var_val_token=ast_node.iterable.token,
        )

        self.visit(ast_node.statement_list_node)
        self.__curr_scope_symbol_table = self.__curr_scope_symbol_table.outer_scope

    def visitVarDeclStatementNode(self, ast_node):
        type_symbol = self.__curr_scope_symbol_table.get_symbol(
            ast_node.var_type_node.val
        )

        for variable in ast_node.variables:
            if isinstance(variable, VarNode):
                var_name = variable.val
                var_token = variable.token
            else:
                TypeChecker.check_assignment_statement(
                    var_type=type_symbol.name,
                    var_val_type=self.visit(variable.right_node).name,
                    var_val_token=variable.right_node.token,
                )
                var_name = variable.left_node.val
                var_token = variable.left_node.token

            variable_symbol = VarSymbol(var_name, type_symbol)

            if (
                self.__curr_scope_symbol_table.get_symbol(
                    var_name, check_outer_scope=False
                )
                is not None
            ):
                self.__error(
                    f'Variable "{var_name}" is declared again',
                    var_token,
                )

            self.__curr_scope_symbol_table.add_symbol(variable_symbol)

    def visitFuncDeclStatementNode(self, ast_node):
        func_symbol = FuncSymbol(ast_node.name)
        self.__curr_scope_symbol_table.add_symbol(func_symbol)

        self.__curr_scope_symbol_table = ScopeSymbolTable(
            scope_name=func_symbol.name,
            scope_level=self.__curr_scope_symbol_table.scope_level + 1,
            outer_scope=self.__curr_scope_symbol_table,
        )
        prev_param = None

        for param in ast_node.params:
            param_type_symbol = self.__curr_scope_symbol_table.get_symbol(
                param.var_type_node.val
            )

            if isinstance(param.var_node, VarNode):
                if isinstance(prev_param, AssignmentStatementNode):
                    self.__error(
                        "Non-default argument follows default argument",
                        param.var_node.token,
                    )

                param_name = param.var_node.val
            else:
                TypeChecker.check_assignment_statement(
                    var_type=param_type_symbol.name,
                    var_val_type=self.visit(param.var_node.right_node).name,
                    var_val_token=param.var_node.right_node.token,
                )
                param_name = param.var_node.left_node.val

            param_symbol = VarSymbol(param_name, param_type_symbol)
            self.__curr_scope_symbol_table.add_symbol(param_symbol)

            func_symbol.params.append(param_symbol)
            prev_param = param.var_node

        self.visit(ast_node.body)
        self.__curr_scope_symbol_table = self.__curr_scope_symbol_table.outer_scope

    def visitStatementListNode(self, ast_node):
        for statement in ast_node.statements:
            self.visit(statement)

    def visitProgramNode(self, ast_node):
        self.visit(ast_node.statement_list_node)
        self.__curr_scope_symbol_table = self.__curr_scope_symbol_table.outer_scope

    def __error(self, error_message, token):
        raise SemnaticError(
            error_message + f" on line: {token.line}, column: {token.col}",
        )
