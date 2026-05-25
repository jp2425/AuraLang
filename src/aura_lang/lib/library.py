from abc import ABC

class Library(ABC):
    def _register_public_methods(self, registry: dict):
        for name in dir(self):
            # ignora métodos privados/internos
            if name.startswith("_"):
                continue

            attr = getattr(self, name)

            if not callable(attr):
                continue

            builtin_name = name.upper()

            if builtin_name in registry:
                raise RuntimeError(f"Builtin '{builtin_name}' already registered")

            registry[builtin_name] = attr
