from lark import Transformer, Token
from .ast_nodes import (
    Program,
    DeclTarget,
    Assign,
    Var,
    Literal,
    BinaryOp,
    UnaryOp,
    Call,
    If,
    Loop,
    Return,
)


class AuraTransformer(Transformer):
    def _is_token_type(self, obj, token_type: str) -> bool:
        return isinstance(obj, Token) and obj.type == token_type

    def _to_expr(self, value):
        # Only convert identifiers (CNAME) to Var
        if isinstance(value, Token):
            if value.type == "CNAME":
                return Var(str(value))
            else:
                return str(value)  # keep operators as string

        if isinstance(value, str):
            return Var(value)

        return value

    def start(self, items):
        inputs = items[0]
        body = items[1] if len(items) > 1 else []
        return Program(inputs=inputs, body=body)

    def inputs(self, items):
        names = []
        for item in items:
            if isinstance(item, Token) and item.type == "AURA":
                continue
            if isinstance(item, str):
                names.append(item)
        return names

    def block(self, items):
        return list(items)

    def declaration(self, items):
        name = None
        for item in items:
            if isinstance(item, Token) and item.type == "MOOD":
                continue
            if isinstance(item, str):
                name = item
                break

        if name is None:
            raise ValueError(f"Declaração inválida: {items}")

        return DeclTarget(name=name)

    def attribution(self, items):
        useful = []
        for item in items:
            if isinstance(item, Token) and item.type == "IS_GIVING":
                continue
            useful.append(item)

        if len(useful) != 2:
            raise ValueError(f"Unexpected attribution: {items}")

        target, value = useful
        value = self._to_expr(value)

        if isinstance(target, DeclTarget):
            return Assign(name=target.name, value=value, declare=True)

        if isinstance(target, str):
            return Assign(name=target, value=value, declare=False)

        raise ValueError(f"Invalid target in attribution: {target}")

    def arithmetic(self, items):
        left, op, right = items
        return BinaryOp(
            op=str(op),
            left=self._to_expr(left),
            right=self._to_expr(right),
        )

    def arith_operand(self, items):
        if len(items) != 1:
            raise ValueError(f"unexpected arith_operand: {items}")
        return self._to_expr(items[0])

    def arith_op(self, items):
        return str(items[0])

    def operator(self, items):
        return items[0]

    def comparison_operation(self, items):
        left, op, right = items
        return BinaryOp(
            op=str(op),
            left=self._to_expr(left),
            right=self._to_expr(right),
        )

    def big_operation(self, items):
        left, op, right = items
        return BinaryOp(
            op=str(op),
            left=self._to_expr(left),
            right=self._to_expr(right),
        )

    def small_operation(self, items):
        left, op, right = items
        return BinaryOp(
            op=str(op),
            left=self._to_expr(left),
            right=self._to_expr(right),
        )

    def comparison_left_operator(self, items):
        return self._to_expr(items[0])

    def comparison_right_operator(self, items):
        return self._to_expr(items[0])

    def big_left_operator(self, items):
        return self._to_expr(items[0])

    def big_right_operator(self, items):
        return self._to_expr(items[0])

    def small_left_operator(self, items):
        return self._to_expr(items[0])

    def small_right_operator(self, items):
        return self._to_expr(items[0])

    def comparison_operator(self, items):
        return str(items[0])

    def big_operator(self, items):
        return str(items[0])

    def small_operator(self, items):
        return str(items[0])

    def bool_expr(self, items):
        """
        Since `bool_expr` is inline (`?bool_expr`), this method is only useful
        in cases where the alternative generates more than one child,
        especially `REKT bool_expr`.
        """
        if len(items) == 1:
            return items[0]

        if len(items) == 2:
            first, second = items
            if self._is_token_type(first, "REKT"):
                return UnaryOp(op="REKT", expr=self._to_expr(second))

        raise ValueError(f"unexpected bool_expr: {items}")

    def and_operator(self, items):
        useful = [x for x in items if not (isinstance(x, Token) and x.type == "AND")]
        if len(useful) != 2:
            raise ValueError(f"unexpected and_operator: {items}")

        left, right = useful
        return BinaryOp(op="AND", left=self._to_expr(left), right=self._to_expr(right))

    def or_operator(self, items):
        useful = [x for x in items if not (isinstance(x, Token) and x.type == "OR")]
        if len(useful) != 2:
            raise ValueError(f"unexpected or_operator: {items}")

        left, right = useful
        return BinaryOp(op="OR", left=self._to_expr(left), right=self._to_expr(right))

    def repetition_structure(self, items):
        useful = []
        for item in items:
            if isinstance(item, Token) and item.type in {"COOK_FOR", "CHEFF_KISS"}:
                continue
            useful.append(item)

        if len(useful) != 3:
            raise ValueError(f"unexpected Loop: {items}")

        count_expr, loop_var, body = useful

        if not isinstance(loop_var, str):
            raise ValueError(f"invalid Loop var: {loop_var}")

        return Loop(
            count_expr=self._to_expr(count_expr),
            loop_var=loop_var,
            body=body,
        )

    def loop_count(self, items):
        if len(items) != 1:
            raise ValueError(f"unexpected loop_count: {items}")
        return self._to_expr(items[0])

    def loop_iteration_identifier(self, items):
        if len(items) != 1:
            raise ValueError(f"unexpected loop_iteration_identifier: {items}")
        return str(items[0])

    def function_call(self, items):

        if not items:
            raise ValueError("function_call is empty")

        name = str(items[0])
        args = [self._to_expr(arg) for arg in items[1:]]
        return Call(name=name, args=args)

    def function_parameter(self, items):
        if len(items) != 1:
            raise ValueError(f"unexpected function_parameter: {items}")
        return self._to_expr(items[0])

    def conditional_structure(self, items):
        useful = []
        for item in items:
            # ignora tokens estruturais
            if isinstance(item, Token) and item.type in {"VIBE_CHECK", "SLAY", "FLOP"}:
                continue

            # ignora placeholders vazios
            if item is None:
                continue

            useful.append(item)

        if len(useful) == 2:
            condition, true_block = useful
            return If(
                condition=self._to_expr(condition),
                then_body=true_block,
                else_body=None,
            )

        if len(useful) == 3:
            condition, true_block, false_block = useful
            return If(
                condition=self._to_expr(condition),
                then_body=true_block,
                else_body=false_block,
            )

        raise ValueError(f"unexpected conditional : {items}")

    def true_block(self, items):
        for item in items:
            if isinstance(item, list):
                return item
        return []

    def false_block(self, items):
        for item in items:
            if isinstance(item, list):
                return item
        return []

    def literal(self, items):
        return items[0]

    def number(self, items):
        raw = str(items[0])
        if "." in raw:
            return Literal(float(raw))
        return Literal(int(raw))

    def letters(self, items):
        raw = str(items[0])
        # remove aspas
        return Literal(raw[1:-1])

    def vibe_true(self, _items):
        return Literal(True)

    def vibe_false(self, _items):
        return Literal(False)

    def squad(self, items):
        values = []
        for item in items:
            if isinstance(item, Literal):
                values.append(item.value)
            else:
                values.append(self._to_expr(item))
        return Literal(values)

    def json_par(self, items):
        key_node, value_node = items

        if isinstance(key_node, Literal):
            key = key_node.value
        else:
            key = key_node

        if isinstance(value_node, Literal):
            value = value_node.value
        else:
            value = self._to_expr(value_node)

        return (key, value)

    def json_tree(self, items):
        return Literal(dict(items))

    def drop(self, items):
        useful = []
        for item in items:
            if isinstance(item, Token) and item.type == "DROP":
                continue
            useful.append(item)

        if len(useful) != 1:
            raise ValueError(f"Unexpected DROP: {items}")

        value = self._to_expr(useful[0])
        return Return(value)

    def CNAME(self, token):
        return str(token)

    def NUMBER(self, token):
        return str(token)