from ...errors import AuraTypeError, AuraRuntimeError
from ..library import Library
from ...runtime.formatting import Formatting

class StdLib(Library):

    def __init__(self, registry):
        self._register_public_methods(registry)

    def ghost_buster(self, value):
        if value == "" or value is None or (isinstance(value, (str, dict, list))  and len(value)) == 0 or value == {}:
            return True
        else:
            return False

    def spill(self, squad, n):
        # dict support
        if isinstance(squad, dict):
            if not isinstance(n, str):
                raise AuraTypeError("SPILL expects string key for JASON")

            if n not in squad:
                raise AuraRuntimeError(f"Key '{n}' not found")

            return squad[n]
        # list / str
        if not isinstance(squad, (list, str)):
            raise AuraTypeError("SPILL needs SQUAD or LETTERS")

        if not isinstance(n, int):
            raise AuraTypeError("SPILL needs integer indexes")

        if n >= len(squad):
            raise AuraRuntimeError("SPILL index off bound")

        return squad[n]

    def transmute(self, x, target_type):
        if not isinstance(target_type, str):
            raise AuraTypeError("TRANSMUTE needs a type (LETTERS)")

        target_type = target_type.upper()

        if target_type == "NUMBER":
            if isinstance(x, (int, float)):
                return x
            if isinstance(x, str):
                try:
                    return int(x) if "." not in x else float(x)
                except ValueError:
                    raise AuraTypeError(f"It was not possible to convert '{x}' to NUMBER")
            if isinstance(x, bool):
                return int(x)
            raise AuraTypeError("CAST to NUMBER has failed")

        if target_type == "LETTERS":
            return str(x)

        if target_type == "VIBE":
            if isinstance(x, bool):
                return x
            if isinstance(x, (int, float)):
                return x != 0
            if isinstance(x, str):
                lowered = x.lower()
                if lowered in ("real", "true", "1"):
                    return True
                if lowered in ("fake", "false", "0", ""):
                    return False
            raise AuraTypeError("CAST to VIBE has failed")

        if target_type == "SQUAD":
            if isinstance(x, list):
                return x
            return [x]

        raise AuraTypeError(f"Unknown type: {target_type}")
    def size(self, x):
        if isinstance(x, (list, str, dict)):
            return len(x)
        raise AuraTypeError("SIZE accepts SQUAD, LETTERS or JASON")

    def render(self, obj, template):

        import re

        if not isinstance(obj, dict):
            raise AuraTypeError("RENDER needs JASON as first argument")

        if not isinstance(template, str):
            raise AuraTypeError("RENDER needs LETTERS as second argument")

        pattern = re.compile(r"\{\{([a-zA-Z_][a-zA-Z0-9_]*)\}\}")

        def replace(match):
            key = match.group(1)
            if key not in obj:
                raise AuraRuntimeError(f"Field '{key}' not found in RENDER")
            return Formatting().aura_format(obj[key])

        return pattern.sub(replace, template)

    def scream(self, *args):

        print(*(Formatting().aura_format(arg) for arg in args))
        return None