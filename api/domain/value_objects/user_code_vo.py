class UserCodeVO:
    def __init__(self, codigo: str):
        if len(codigo) != 8 or not codigo.isdigit():
            raise ValueError(
                "User code must be 8 characters long and contain only numbers"
            )
        self.codigo = codigo

    def __str__(self):
        return self.codigo
