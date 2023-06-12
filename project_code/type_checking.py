from .tokens import Token
from .symbol_table import BuiltInTypeSymbol, RangeSymbol
from .error import SemanticError


class TypeChecker:
    """
    Used the type rules from the programming language Java.
    """

    @staticmethod
    def check_accessor(accessor_type, accessor_token):
        if accessor_type != Token.K_STR:
            TypeChecker.__error(
                f'"{accessor_type}" type cannot be an accessor',
                accessor_token,
            )

    @staticmethod
    def check_index(index_type, index_token):
        if index_type != Token.K_INT:
            TypeChecker.__error(
                f'Index of type "{index_type}" is not allowed',
                index_token,
            )

    @staticmethod
    def check_built_in_func_call(func_name, func_arg_types, func_token):
        match func_name:
            case "input":
                if func_arg_types[0] != Token.K_STR:
                    TypeChecker.__error(
                        f'The function named "{func_name}" can only accept a string argument',
                        func_token,
                    )

            case "reverse" | "len":
                if func_arg_types[0] != Token.K_STR:
                    TypeChecker.__error(
                        f'The function named "{func_name}" can only accept a string argument',
                        func_token,
                    )

            case "pow":
                if func_arg_types[0] not in (
                    Token.K_FLOAT,
                    Token.K_INT,
                ) or func_arg_types[1] not in (Token.K_FLOAT, Token.K_INT):
                    TypeChecker.__error(
                        f'The function named "{func_name}" can only accept integer or float values as arguments',
                        func_token,
                    )

    @staticmethod
    def check_unary_op(op_token, child_node_type):
        if op_token.type_ == Token.K_NOT:
            if child_node_type != Token.K_BOOL:
                TypeChecker.__error(
                    f'The operator "{op_token.val}" cannot be used with the type "{child_node_type}"',
                    op_token,
                )

            return BuiltInTypeSymbol(Token.K_BOOL)

        if op_token.type_ in (Token.MINUS, Token.PLUS):
            match child_node_type:
                case Token.K_STR | Token.K_BOOL:
                    TypeChecker.__error(
                        f'The operator "{op_token.val}" cannot be used with the type "{child_node_type}"',
                        op_token,
                    )

                case Token.K_FLOAT:
                    return BuiltInTypeSymbol(Token.K_FLOAT)

                case Token.K_INT:
                    return BuiltInTypeSymbol(Token.K_INT)

    @staticmethod
    def check_binary_op(op_token, left_node_type, right_node_type):
        if op_token.type_ in (
            Token.PLUS,
            Token.MINUS,
            Token.MULTIPLICATION,
            Token.FLOAT_DIVISION,
            Token.INT_DIVISION,
            Token.MODULO,
        ):
            return TypeChecker.__check_arithmetic_op(
                op_token, left_node_type, right_node_type
            )

        if op_token.type_ in (Token.EQUALS, Token.NOT_EQUALS):
            if left_node_type != right_node_type:
                TypeChecker.__error(
                    f'The types of "{left_node_type}" and "{right_node_type}" cannot be compared',
                    op_token,
                )

            return BuiltInTypeSymbol(Token.K_BOOL)

        if op_token.type_ in (
            Token.LESS_THAN,
            Token.LESS_THAN_OR_EQUALS,
            Token.GREATER_THAN,
            Token.GREATER_THAN_OR_EQUALS,
        ):
            return TypeChecker.__check_comparison_op(
                op_token, left_node_type, right_node_type
            )

        if op_token.type_ in (Token.K_AND, Token.K_OR):
            if Token.K_BOOL not in (left_node_type, right_node_type):
                TypeChecker.__error(
                    f'"{op_token.val}" operator cannot be used with "{left_node_type}" and "{right_node_type}"',
                    op_token,
                )

            return BuiltInTypeSymbol(Token.K_BOOL)

    @staticmethod
    def check_assignment_statement(var_type, var_val_type, var_val_token):
        if var_type != var_val_type:
            TypeChecker.__error(
                f'Cannot assign "{var_val_type}" to "{var_type}"', var_val_token
            )

    @staticmethod
    def check_accessor_assignment_statement(accessor_type, accessor_token):
        if accessor_type == Token.K_STR:
            TypeChecker.__error(
                "Strings are immutable",
                accessor_token,
            )

    @staticmethod
    def check_condition(condition_type, condition_token):
        if condition_type != Token.K_BOOL:
            TypeChecker.__error(
                f'The Condition must evaluate to "bool", not "{condition_type}"',
                condition_token,
            )

    @staticmethod
    def check_range_expr(start_type, end_type, step_type, range_token):
        if (start_type != Token.K_INT) or (end_type != Token.K_INT):
            TypeChecker.__error(
                'The start and the end of the range must be "int"', range_token
            )

        if step_type is not None and step_type != Token.K_INT:
            TypeChecker.__error('"step" of the range must be "int"', range_token)

        return RangeSymbol()

    @staticmethod
    def check_iterable(iterable_type, iterable_token):
        if not iterable_type.startswith("range") and iterable_type != Token.K_STR:
            TypeChecker.__error(
                f'Cannot iterate over "{iterable_type}"', iterable_token
            )

    @staticmethod
    def check_return_statement(func_symbol, curr_returned, return_token):
        if func_symbol.type_ != curr_returned:
            TypeChecker.__error(
                f'Function "{func_symbol.name[5:]}" returns "{"nothing" if curr_returned is None else curr_returned.name}" '
                f'but should return "{"nothing" if func_symbol.type_ is None else func_symbol.type_.name}"',
                return_token,
            )

    @staticmethod
    def __check_arithmetic_op(op_token, left_node_type, right_node_type):
        match (left_node_type, right_node_type):
            case (Token.K_STR, _) | (_, Token.K_STR):
                if op_token.type_ == Token.PLUS:
                    return BuiltInTypeSymbol(Token.K_STR)

                if op_token.type_ in Token.MULTIPLICATION and Token.K_INT in (
                    left_node_type,
                    right_node_type,
                ):
                    return BuiltInTypeSymbol(Token.K_STR)

                TypeChecker.__error(
                    f'"{op_token.val}" operator cannot be used with "{left_node_type}" and "{right_node_type}"',
                    op_token,
                )

            case (Token.K_BOOL, _) | (_, Token.K_BOOL):
                TypeChecker.__error(
                    f'"{op_token.val}" operator cannot be used with "{left_node_type}" and "{right_node_type}"',
                    op_token,
                )

            case (Token.K_FLOAT, _) | (_, Token.K_FLOAT):
                if op_token.type_ in Token.INT_DIVISION:
                    return BuiltInTypeSymbol(Token.K_INT)

                return BuiltInTypeSymbol(Token.K_FLOAT)

            case (_, _):
                return BuiltInTypeSymbol(Token.K_INT)

    @staticmethod
    def __check_comparison_op(op_token, left_node_type, right_node_type):
        match (left_node_type, right_node_type):
            case (Token.K_STR, Token.K_STR):
                return BuiltInTypeSymbol(Token.K_BOOL)

            case (Token.K_STR, _) | (_, Token.K_STR) | (Token.K_BOOL, _) | (
                _,
                Token.K_BOOL,
            ):
                TypeChecker.__error(
                    f'"{op_token.val}" operator cannot be used with "{left_node_type}" and "{right_node_type}"',
                    op_token,
                )

            case (_, _):
                return BuiltInTypeSymbol(Token.K_BOOL)

    @staticmethod
    def __error(error_message, token):
        raise SemanticError(
            error_message + f" in line: {token.line}, column: {token.col}",
        )
