import copy

from .abstract_syntax_tree import VarNode, AccessNode, AssignmentStatementNode
from .error import SemanticError
from .scope_symbol_table import (
    ScopeSymbolTable,
    BuiltInTypeSymbol,
    BuiltInFuncSymbol,
    VarSymbol,
    ConditionalSymbol,
    LoopSymbol,
    FuncSymbol,
)
from .tokens import Token
from .type_checking import TypeChecker
from .visit_ast_node import ASTNodeVisitor


class SemanticAnalyzer(ASTNodeVisitor):
    def __init__(self):
        self.__curr_scope_symbol_table = ScopeSymbolTable(
            scope_name="global", scope_level=1, outer_scope=None
        )
        self.__curr_scope_symbol_table.add_built_in_symbols()

        self.__return_flag = False
        self.is_func_call_statement = False

    def visitVarNode(self, ast_node):
        var_name = ast_node.val
        variable_symbol = self.__curr_scope_symbol_table.get_symbol(var_name)

        if variable_symbol is None:
            self.__error(f'Identifier "{var_name}" not found', ast_node.token)

        return variable_symbol.type_

    def visitFuncCallNode(self, ast_node):
        func_name = ast_node.func_name
        func_token = ast_node.token
        func_args = ast_node.args
        func_symbol = self.__curr_scope_symbol_table.get_symbol(f"func_{func_name}")

        if func_symbol is None:
            self.__error(f'Function "{func_name}" not found', func_token)

        if isinstance(func_symbol, BuiltInFuncSymbol):
            self.__handle_built_in_funcs(func_name, func_args, func_token)
            return func_symbol.type_

        num_args = len(func_args)
        num_params = len(func_symbol.params)

        num_default_params = func_symbol.num_default_params
        num_non_default_params = num_params - num_default_params

        if (num_args < num_non_default_params) or (num_args > num_params):
            self.__error(
                f'Function "{func_name}" takes {num_non_default_params}'
                f'{"" if num_params in (0, num_non_default_params) else " to " + str(num_params)} '
                f"positional arguments but {num_args} were given",
                func_token,
            )

        for i, arg in enumerate(func_args):
            TypeChecker.check_assignment_statement(
                func_symbol.params[i].type_.name,
                self.visit(arg).name,
                arg.token,
            )

        if func_symbol.type_ is None and not ast_node.is_statement:
            self.__error(
                f'"void" function "{func_name}" not allowed here',
                func_token,
            )

        return func_symbol.type_

    def __handle_built_in_funcs(self, func_name, func_args, func_token):
        if func_name == "input" and len(func_args) not in (0, 1):
            self.__error(
                f'Function "{func_name}" must take 0 or 1 argument', func_token
            )

        if (
            func_name
            in ("reverse", "len", "typeof", "toint", "tofloat", "tobool", "tostr")
            and len(func_args) != 1
        ):
            self.__error(f'Function "{func_name}" must take 1 argument', func_token)

        if func_name == "pow" and len(func_args) != 2:
            self.__error(f'Function "{func_name}" must take 2 arguments', func_token)

        func_arg_types = [self.visit(arg).name for arg in func_args]
        TypeChecker.check_built_in_func_call(func_name, func_arg_types, func_token)

    def visitAccessNode(self, ast_node):
        accessor_type = self.visit(ast_node.accessor_node).name
        TypeChecker.check_accessor(accessor_type, ast_node.accessor_node.token)

        start_index_type = self.visit(ast_node.start_index_node).name
        TypeChecker.check_index(start_index_type, ast_node.start_index_node.token)

        end_index = ast_node.end_index_node

        if end_index is not None:
            end_index_type = self.visit(end_index).name
            TypeChecker.check_index(end_index_type, end_index.token)

        return BuiltInTypeSymbol(Token.K_STR)

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
        left_node = ast_node.left_node

        if isinstance(left_node, AccessNode):
            TypeChecker.check_accessor_assignment_statement(
                self.visit(left_node.accessor_node).name, left_node.accessor_node.token
            )

        TypeChecker.check_assignment_statement(
            var_type=self.visit(left_node).name,
            var_val_type=self.visit(ast_node.right_node).name,
            var_val_token=ast_node.right_node.token,
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
            TypeChecker.check_condition(self.visit(condition).name, condition.token)
            name = "if" if i == 0 else "elseif"

            if_elseif_symbol = ConditionalSymbol(name)
            symbol_names.append(if_elseif_symbol.name)

            self.__curr_scope_symbol_table.add_symbol(if_elseif_symbol)

        if ast_node.else_case is not None:
            else_symbol = ConditionalSymbol("else")
            symbol_names.append(else_symbol.name)

            self.__curr_scope_symbol_table.add_symbol(else_symbol)

    def visitWhileStatementNode(self, ast_node):
        TypeChecker.check_condition(
            self.visit(ast_node.condition).name, ast_node.condition.token
        )

        while_symbol = LoopSymbol("while")
        self.__curr_scope_symbol_table.add_symbol(while_symbol)

        self.__curr_scope_symbol_table = ScopeSymbolTable(
            scope_name=while_symbol.name,
            scope_level=self.__curr_scope_symbol_table.scope_level + 1,
            outer_scope=self.__curr_scope_symbol_table,
        )

        self.visit(ast_node.statement_list_node)
        self.__curr_scope_symbol_table = self.__curr_scope_symbol_table.outer_scope

    def visitBreakStatementNode(self, ast_node):
        if not self.__is_in_loop():
            self.__error("Break statement outside of loop", ast_node.token)

    def visitContinueStatementNode(self, ast_node):
        if not self.__is_in_loop():
            self.__error("Continue statement outside of loop", ast_node.token)

    def __is_in_loop(self):
        curr_scope_symbol_table_cpy = copy.copy(self.__curr_scope_symbol_table)

        while curr_scope_symbol_table_cpy.scope_name != "global":
            if curr_scope_symbol_table_cpy.scope_name.startswith(
                "for"
            ) or curr_scope_symbol_table_cpy.scope_name.startswith("while"):
                return True

            curr_scope_symbol_table_cpy = curr_scope_symbol_table_cpy.outer_scope

        return False

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
                if iterable_type.startswith("range")
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

    def visitReturnStatementNode(self, ast_node):
        return_type = self.visit(ast_node.expr_node) if ast_node.expr_node else None
        curr_scope_symbol_table_cpy = copy.copy(self.__curr_scope_symbol_table)

        while curr_scope_symbol_table_cpy.scope_name != "global":
            if curr_scope_symbol_table_cpy.scope_name.startswith("func"):
                func_symbol = curr_scope_symbol_table_cpy.outer_scope.get_symbol(
                    curr_scope_symbol_table_cpy.scope_name, check_outer_scope=False
                )

                TypeChecker.check_return_statement(
                    func_symbol, return_type, ast_node.token
                )

                self.__return_flag = True
                return

            curr_scope_symbol_table_cpy = curr_scope_symbol_table_cpy.outer_scope

        self.__error("Return statement outside function", ast_node.token)

    def visitFuncDeclStatementNode(self, ast_node):
        if self.__curr_scope_symbol_table.get_symbol("func_" + ast_node.name):
            self.__error(
                f'Function "{ast_node.name}" is declared again', ast_node.token
            )

        return_type_symbol = self.__curr_scope_symbol_table.get_symbol(
            ast_node.return_type_node.val
        )
        func_symbol = FuncSymbol(ast_node.name, return_type_symbol)

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
                        "Non-default parameter follows default parameter",
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
                func_symbol.add_default_param()

            param_symbol = VarSymbol(param_name, param_type_symbol)
            self.__curr_scope_symbol_table.add_symbol(param_symbol)

            func_symbol.params.append(param_symbol)
            prev_param = param.var_node

        self.visit(ast_node.body)

        if return_type_symbol is not None and not self.__return_flag:
            self.__error(
                f'Missing return statement for the function "{ast_node.name}"',
                ast_node.token,
            )
        else:
            self.__return_flag = False

        self.__curr_scope_symbol_table = self.__curr_scope_symbol_table.outer_scope

    def visitStatementListNode(self, ast_node):
        for statement in ast_node.statements:
            self.visit(statement)

    def visitProgramNode(self, ast_node):
        self.visit(ast_node.statement_list_node)
        self.__curr_scope_symbol_table = self.__curr_scope_symbol_table.outer_scope

    def __error(self, error_message, token):
        raise SemanticError(
            error_message + f" in line: {token.line}, column: {token.col}",
        )
