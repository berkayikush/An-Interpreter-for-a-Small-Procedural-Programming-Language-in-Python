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

    def __str__(self):
        s = "\n".join(repr(frame) for frame in reversed(self.stack))
        s = f"Program Stack\n{s}\n"
        return s

    def __repr__(self):
        return self.__str__()


class StackFrame:
    ###############
    # Frame Types #
    ###############
    GLOBAL = "GLOBAL"
    CONDITIONAL_STATEMENT = "CONDITIONAL_STATEMENT"

    def __init__(self, name, type_, scope_level, outer_scope=None):
        self.__name = name
        self.__type_ = type_

        self.__scope_level = scope_level
        self.__variables = {}
        self.__outer_scope = outer_scope

    @property
    def scope_level(self):
        return self.__scope_level

    @property
    def outer_scope(self):
        return self.__outer_scope

    def __getitem__(self, key):
        return self.__variables[key]

    def get(self, key, default=None):
        if self.check_variable(key):
            return self.__variables[key]

        if self.__outer_scope is not None:
            return self.__outer_scope.get(key)

        return default

    def check_variable(self, variable):
        return variable in self.__variables

    def set(self, key, value):
        if self.check_variable(key):
            self.__variables[key] = value
            return

        self.__outer_scope.set(key, value)

    def __setitem__(self, key, value):
        self.__variables[key] = value

    def __str__(self):
        lines = [f"{self.__scope_level} {self.__type_} {self.__name}"]

        for key, value in self.__variables.items():
            lines.append(f"\t{key:<20} = {value}")

        s = "\n".join(lines)
        return s

    def __repr__(self):
        return self.__str__()
