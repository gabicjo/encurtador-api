class URLInvalido(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class SemURL(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class CodigoInvalido(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)