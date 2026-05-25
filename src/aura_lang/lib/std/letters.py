from ..library import Library

class Letters(Library):
    def __init__(self, registry):
        self._register_public_methods(registry)

    def calm_down(self, value: str):
        return value.lower()

    def enormify(self, value: str):
        return value.upper()

    def burn_the_fat(self, value: str):
        return value.strip()

