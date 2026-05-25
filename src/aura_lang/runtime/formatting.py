class Formatting:
    def aura_format(self, value):
        """
        Converts Python runtime values back into AURA language values.

        Python True  -> "real"
        Python False -> "fake"
        lists/dicts are formatted recursively
        """

        # Important: check bool before int.
        # In Python, bool is a subclass of int.
        if type(value) is bool:
            return "real" if value else "fake"

        if isinstance(value, str):
            return value

        if isinstance(value, (int, float)):
            return str(value)

        if value is None:
            return "nothing"

        if isinstance(value, list):
            inner = ", ".join(self.aura_format(v) for v in value)
            return f"[{inner}]"

        if isinstance(value, dict):
            inner = ", ".join(
                f'"{k}": {self.aura_format(v)}'
                for k, v in value.items()
            )
            return "{" + inner + "}"

        return str(value)