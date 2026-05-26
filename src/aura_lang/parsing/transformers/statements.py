from lark import Token
from ..ast_nodes import Assign, If, Loop, Return, DeclTarget


class StatementTransformer:
    # -------------------------
    # Declarations / assignment
    # -------------------------

    def declaration(self, items):
        for item in items:
            if isinstance(item, Token) and item.type == "MOOD":
                continue

            if isinstance(item, Token) and item.type == "CNAME":
                return DeclTarget(name=str(item))

            if isinstance(item, str):
                return DeclTarget(name=item)

        raise ValueError(f"Invalid declaration: {items}")

    def attribution(self, items):
        useful = self._strip_tokens(items, {"IS_GIVING"})

        if len(useful) != 2:
            raise ValueError(f"Invalid attribution: {items}")

        target, value = useful
        value = self._to_expr(value)

        if isinstance(target, DeclTarget):
            return Assign(
                name=target.name,
                value=value,
                declare=True,
            )

        target_name = self._to_name(target)

        return Assign(
            name=target_name,
            value=value,
            declare=False,
        )

    # -------------------------
    # Conditionals
    # -------------------------

    def conditional_structure(self, items):
        useful = self._strip_tokens(items, {"VIBE_CHECK", "SLAY", "FLOP"})

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

        raise ValueError(f"Invalid conditional: {items}")

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

    # -------------------------
    # Loop
    # -------------------------

    def repetition_structure(self, items):
        useful = self._strip_tokens(items, {"COOK_FOR", "CHEFF_KISS"})

        if len(useful) != 3:
            raise ValueError(f"Invalid loop: {items}")

        count, var, body = useful

        return Loop(
            count_expr=self._to_expr(count),
            loop_var=self._to_name(var),
            body=body,
        )

    def loop_count(self, items):
        return self._to_expr(self._single("loop_count", items))

    def loop_iteration_identifier(self, items):
        return self._to_name(self._single("loop_iteration_identifier", items))

    # -------------------------
    # DROP / return
    # -------------------------

    def drop(self, items):
        useful = self._strip_tokens(items, {"DROP"})

        if len(useful) != 1:
            raise ValueError(f"Invalid DROP: {items}")

        return Return(self._to_expr(useful[0]))