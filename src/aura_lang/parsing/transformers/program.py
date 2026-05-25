from lark import Token
from ..ast_nodes import Program


class ProgramTransformer:
    def start(self, items):
        inputs = items[0]
        body = items[1] if len(items) > 1 else []
        return Program(inputs=inputs, body=body)

    def inputs(self, items):
        names = []

        for item in items:
            if isinstance(item, Token) and item.type == "AURA":
                continue

            if isinstance(item, Token) and item.type == "CNAME":
                names.append(str(item))
                continue

            if isinstance(item, str):
                names.append(item)

        return names

    def block(self, items):
        return list(items)