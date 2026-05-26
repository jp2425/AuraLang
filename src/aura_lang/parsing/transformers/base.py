from lark import Transformer, Token
from ..ast_nodes import Var, BinaryOp


class BaseTransformer(Transformer):
    """
    Shared helpers used by all transformer mixins.
    """

    def _is_token_type(self, obj, token_type: str) -> bool:
        return isinstance(obj, Token) and obj.type == token_type

    def _to_name(self, value):
        """
        Converts a variable/name node into a plain Python string.

        Accepts:
            Token('CNAME', 'x') -> "x"
            "x"                 -> "x"
        """
        if isinstance(value, Token):
            return str(value)

        if isinstance(value, str):
            return value

        raise ValueError(f"Expected name, got: {value}")

    def _to_expr(self, value):
        """
        Converts expression-like values into AST expression nodes.

        Important:
        - CNAME tokens / strings become Var(...)
        - non-CNAME tokens become plain strings
        - AST nodes are returned unchanged
        """
        if isinstance(value, Token):
            if value.type == "CNAME":
                return Var(str(value))
            return str(value)

        if isinstance(value, str):
            return Var(value)

        return value

    def _strip_tokens(self, items, ignored):
        """
        Removes structural tokens and None placeholders.
        """
        return [
            x for x in items
            if x is not None and not (isinstance(x, Token) and x.type in ignored)
        ]

    def _single(self, name, items):
        if len(items) != 1:
            raise ValueError(f"{name} expected 1 item, got {items}")
        return items[0]

    def _binary(self, left, op, right):
        """
        Builds a BinaryOp from grammar order:

            left op right

        This is the important fix.
        Previous version received (op, left, right), but grammar gives:
            [left, op, right]
        """
        return BinaryOp(
            op=str(op),
            left=self._to_expr(left),
            right=self._to_expr(right),
        )

    def CNAME(self, token):
        return str(token)

    def NUMBER(self, token):
        return str(token)