class ExistingEmailError(Exception):
    def __init__(self, *args: object, **kwargs) -> None:
        self.message = {"error": "User already exists."}
        super().__init__(self.message)


class TypeConflictError(Exception):
    def __init__(self, *args: object, **kwargs) -> None:
        self.message = {"msg": "Data with incorrect type sent"}
        super().__init__(self.message)


class EmailError(Exception):
    ...


class NameError(Exception):
    ...
