from .tokens import Token


class SymbolTable:
    def __init__(self, scope_name, scope_level, outer_scope=None):
        self.__scope_name = scope_name
        self.__scope_level = scope_level

        self.__outer_scope = outer_scope
        self.__symbols = {}

    @property
    def scope_name(self):
        return self.__scope_name

    @property
    def scope_level(self):
        return self.__scope_level

    @property
    def outer_scope(self):
        return self.__outer_scope

    def add_built_in_symbols(self):
        self.__symbols = {
            "int": BuiltInTypeSymbol(Token.K_INT),
            "float": BuiltInTypeSymbol(Token.K_FLOAT),
            "bool": BuiltInTypeSymbol(Token.K_BOOL),
            "str": BuiltInTypeSymbol(Token.K_STR),

            "func_print": BuiltInFuncSymbol("print"),
            "func_println": BuiltInFuncSymbol("println"),
            "func_input": BuiltInFuncSymbol("input", BuiltInTypeSymbol(Token.K_STR)),
            "func_reverse": BuiltInFuncSymbol("reverse", BuiltInTypeSymbol(Token.K_STR)),

            "func_len": BuiltInFuncSymbol("len", BuiltInTypeSymbol(Token.K_INT)),
            "func_pow": BuiltInFuncSymbol("pow", BuiltInTypeSymbol(Token.K_FLOAT)),
            "func_typeof": BuiltInFuncSymbol("typeof", BuiltInTypeSymbol(Token.K_STR)),
            "func_toint": BuiltInFuncSymbol("toint", BuiltInTypeSymbol(Token.K_INT)),

            "func_tofloat": BuiltInFuncSymbol("tofloat", BuiltInTypeSymbol(Token.K_FLOAT)),
            "func_tobool": BuiltInFuncSymbol("tobool", BuiltInTypeSymbol(Token.K_BOOL)),
            "func_tostr": BuiltInFuncSymbol("tostr", BuiltInTypeSymbol(Token.K_STR)),
        }

    def add_symbol(self, symbol):
        self.__symbols[symbol.name] = symbol

    def get_symbol(self, name, check_outer_scope=True):
        if self.__check_symbol(name):
            return self.__symbols[name]

        if (not check_outer_scope) and (
            not (
                self.__scope_name.startswith("if")
                or self.__scope_name.startswith("elseif")
                or self.__scope_name.startswith("else")
                or self.__scope_name.startswith("while")
                or self.__scope_name.startswith("for")
            )
        ):
            return None

        if self.__outer_scope is not None:
            return self.__outer_scope.get_symbol(name, check_outer_scope)

    def __check_symbol(self, name):
        return name in self.__symbols


class Symbol:
    def __init__(self, name, type_=None):
        self._name = name
        self._type_ = type_

    @property
    def name(self):
        return self._name

    @property
    def type_(self):
        return self._type_


class BuiltInTypeSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name)

    def __eq__(self, other):
        if not isinstance(other, BuiltInTypeSymbol):
            return False

        return self.name == other.name


class BuiltInFuncSymbol(Symbol):
    def __init__(self, name, type_=None):
        super().__init__(f"func_{name}", type_)


class VarSymbol(Symbol):
    """
    Used to make sure that a variable is declared before it is used.
    """

    def __init__(self, name, type_):
        super().__init__(name, type_)


class ConditionalSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name=f"{name}_{id(self)}")


class RangeSymbol(Symbol):
    def __init__(self, name="range"):
        super().__init__(name=f"{name}_{id(self)}")


class LoopSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name=f"{name}_{id(self)}")


class FuncSymbol(Symbol):
    def __init__(self, name, type_=None, params=None):
        super().__init__(f"func_{name}", type_)
        self.__params = params if params is not None else []
        self.__num_default_params = 0  # Used to check if params number is correct.

    @property
    def params(self):
        return self.__params

    @property
    def num_default_params(self):
        return self.__num_default_params

    def add_default_param(self):
        self.__num_default_params += 1
