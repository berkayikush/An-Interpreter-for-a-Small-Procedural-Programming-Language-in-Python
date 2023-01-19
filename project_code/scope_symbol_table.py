from .tokens import Token


class ScopeSymbolTable:
    def __init__(self, scope_name, scope_level, outside_scope=None):
        self.__scope_name = scope_name
        self.__scope_level = scope_level
        self.__outside_scope = outside_scope

        self.__symbols = {
            "int": BuiltInTypeSymbol(Token.K_INT),
            "float": BuiltInTypeSymbol(Token.K_FLOAT),
            "bool": BuiltInTypeSymbol(Token.K_BOOL),
            "if": BuiltInTypeSymbol(Token.K_IF),
            "elseif": BuiltInTypeSymbol(Token.K_ELSEIF),
            "else": BuiltInTypeSymbol(Token.K_ELSE),
        }

    @property
    def scope_name(self):
        return self.__scope_name

    @property
    def scope_level(self):
        return self.__scope_level

    @property
    def outside_scope(self):
        return self.__outside_scope

    def add_symbol(self, symbol):
        self.__symbols[symbol.name] = symbol

    def get_symbol(self, name, check_outside_scope=True):
        if self.__check_symbol(name):
            return self.__symbols[name]

        if not check_outside_scope:
            return None

        if self.__outside_scope is not None:
            return self.__outside_scope.get_symbol(name)

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


class VariableSymbol(Symbol):
    """
    Used to make sure that we assign the correct type to a variable.
    Also used to make sure that a variable is declared before it is used.
    """

    def __init__(self, name, type_):
        super().__init__(name, type_)


class IfElseIfElseSymbol(Symbol):
    def __init__(self, name, type_):
        super().__init__(name=f"{name}_{id(self)}", type_=type_)
