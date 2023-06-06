import copy


class ProgramStack:
    def __init__(self):
        self.stack = []

    def push(self, frame):
        self.stack.append(frame)

    def pop(self):
        return self.stack.pop()

    def peek(self):
        return self.stack[-1]

    def size(self):
        return len(self.stack)


class StackFrame:
    ###############
    # Frame Types #
    ###############
    GLOBAL = "GLOBAL"
    CONDITIONAL_STATEMENT = "CONDITIONAL_STATEMENT"
    WHILE_STATEMENT = "WHILE_STATEMENT"
    FOR_STATEMENT = "FOR_STATEMENT"
    FUNC = "FUNC"

    def __init__(self, name, type_, scope_level, outer_scope=None):
        self.__name = name
        self.__type_ = type_

        self.__scope_level = scope_level
        self.__outer_scope = outer_scope

        self.__variables = {}
        self.__functions = {}

    @property
    def scope_level(self):
        return self.__scope_level

    @property
    def outer_scope(self):
        return self.__outer_scope

    @property
    def variables(self):
        return self.__variables

    @property
    def functions(self):
        return self.__functions

    def get_var(self, key, default=None):
        if self.__check_var(key):
            return self.__variables[key]

        if self.__outer_scope is not None:
            return self.__outer_scope.get_var(key)

        return default

    def get_func(self, key, default=None):
        if self.__check_func(key):
            return (
                self.__functions[key]["stack frame"],
                self.__functions[key]["param names"],
                self.__functions[key]["body"],
            )

        if self.__outer_scope is not None:
            return self.__outer_scope.get_func(key)

        return default

    def set_var(self, key, val):
        if self.__check_var(key):
            self.__variables[key] = val
            return

        self.__outer_scope.set_var(key, val)

    def __check_var(self, variable):
        return variable in self.__variables

    def __check_func(self, function):
        return function in self.__functions
