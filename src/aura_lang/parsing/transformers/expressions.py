from lark import Token
from ..ast_nodes import BinaryOp, UnaryOp


class ExpressionTransformer:
    # -------------------------
    # Arithmetic
    # -------------------------

    def arith_operand(self, items):
        return self._to_expr(self._single("arith_operand", items))

    def arith_op(self, items):
        return str(self._single("arith_op", items))

    def arithmetic(self, items):
        left, op, right = items
        return self._binary(left, op, right)

    # -------------------------
    # Generic operator wrapper
    # -------------------------

    def operator(self, items):
        return self._single("operator", items)

    # -------------------------
    # ME_TOO / ==
    # -------------------------

    def comparison_left_operator(self, items):
        return self._to_expr(self._single("comparison_left_operator", items))

    def comparison_operator(self, items):
        return str(self._single("comparison_operator", items))

    def comparison_right_operator(self, items):
        return self._to_expr(self._single("comparison_right_operator", items))

    def comparison_operation(self, items):
        left, op, right = items
        return self._binary(left, op, right)

    # -------------------------
    # BIG / >
    # -------------------------

    def big_left_operator(self, items):
        return self._to_expr(self._single("big_left_operator", items))

    def big_operator(self, items):
        return str(self._single("big_operator", items))

    def big_right_operator(self, items):
        return self._to_expr(self._single("big_right_operator", items))

    def big_operation(self, items):
        left, op, right = items
        return self._binary(left, op, right)

    # -------------------------
    # SMALL / <
    # -------------------------

    def small_left_operator(self, items):
        return self._to_expr(self._single("small_left_operator", items))

    def small_operator(self, items):
        return str(self._single("small_operator", items))

    def small_right_operator(self, items):
        return self._to_expr(self._single("small_right_operator", items))

    def small_operation(self, items):
        left, op, right = items
        return self._binary(left, op, right)

    # -------------------------
    # Boolean expressions
    # -------------------------

    def bool_expr(self, items):
        if len(items) == 1:
            return items[0]

        if len(items) == 2:
            first, second = items

            if isinstance(first, Token) and first.type in {"MAXXED", "REKT", "DENY"}:
                return UnaryOp(op=first.type, expr=self._to_expr(second))

        raise ValueError(f"Invalid bool_expr: {items}")

    def and_operator(self, items):
        useful = self._strip_tokens(items, {"AND"})

        if len(useful) != 2:
            raise ValueError(f"Invalid AND expression: {items}")

        left, right = useful
        return BinaryOp(
            op="AND",
            left=self._to_expr(left),
            right=self._to_expr(right),
        )

    def or_operator(self, items):
        useful = self._strip_tokens(items, {"OR"})

        if len(useful) != 2:
            raise ValueError(f"Invalid OR expression: {items}")

        left, right = useful
        return BinaryOp(
            op="OR",
            left=self._to_expr(left),
            right=self._to_expr(right),
        )