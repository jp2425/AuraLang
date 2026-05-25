from ..ast_nodes import Literal


class LiteralTransformer:
    def literal(self, items):
        return self._single("literal", items)

    def number(self, items):
        raw = str(self._single("number", items))
        return Literal(float(raw)) if "." in raw else Literal(int(raw))

    def letters(self, items):
        raw = str(self._single("letters", items))
        return Literal(raw[1:-1])

    def vibe_true(self, _):
        return Literal(True)

    def vibe_false(self, _):
        return Literal(False)

    def squad(self, items):
        values = []

        for item in items:
            # Empty [] may produce None because of optional grammar parts.
            # We ignore it so [] becomes Literal([]), not Literal([None]).
            if item is None:
                continue

            if isinstance(item, Literal):
                values.append(item.value)
            else:
                values.append(self._to_expr(item))

        return Literal(values)

    def json_par(self, items):
        key_node, value_node = items

        key = key_node.value if isinstance(key_node, Literal) else self._to_name(key_node)
        value = value_node.value if isinstance(value_node, Literal) else self._to_expr(value_node)

        return key, value

    def json_tree(self, items):
        return Literal(dict(items))