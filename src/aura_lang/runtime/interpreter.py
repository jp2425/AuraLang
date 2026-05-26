from collections import ChainMap

from ..parsing.ast_nodes import (
    Program,
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

from ..lib.std.stdlib import StdLib
from ..lib.std.letters import Letters


class AuraRuntimeError(Exception):
    pass


class AuraNameError(AuraRuntimeError):
    pass


class AuraTypeError(AuraRuntimeError):
    pass


class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value


class AuraInterpreter:
    def __init__(self, inputs=None):
        # Global scope
        self.env = {}
        self.inputs = inputs or {}

        self.builtins = {}

        # Instantiate standard libraries
        StdLib(self.builtins)
        Letters(self.builtins)

    # -------------------------
    # Public API
    # -------------------------
    def run(self, program: Program):
        for name in program.inputs:
            self.env[name] = self.inputs.get(name, None)

        # Main program body runs in the global scope
        env = ChainMap(self.env)

        try:
            self.exec_block(program.body, env)
        except ReturnSignal as ret:
            return ret.value

        return None

    # -------------------------
    # Scope helpers
    # -------------------------
    def declare_var(self, env, name, value):
        """
        Declares a variable in the current local scope.
        New variables declared inside blocks do not leak outside.
        """
        if name in env.maps[0]:
            raise AuraRuntimeError(
                f"The variable '{name}' has already been declared in this block"
            )

        env.maps[0][name] = value

    def assign_var(self, env, name, value):
        """
        Reassigns an existing variable.

        Searches from the innermost scope to the outermost scope and writes
        into the first scope where the variable exists.
        """
        for scope in env.maps:
            if name in scope:
                scope[name] = value
                return

        raise AuraNameError(f"Variable '{name}' does not exist")

    def resolve_var(self, env, name):
        """
        Resolves a variable using the scope chain.
        """
        for scope in env.maps:
            if name in scope:
                return scope[name]

        raise AuraNameError(f"Variable '{name}' is not defined")

    # -------------------------
    # Statements
    # -------------------------
    def exec_block(self, body, env):
        for stmt in body:
            self.exec_stmt(stmt, env)

    def exec_stmt(self, stmt, env):
        if isinstance(stmt, Assign):
            value = self.eval_expr(stmt.value, env)

            if stmt.declare:
                self.declare_var(env, stmt.name, value)
                return

            self.assign_var(env, stmt.name, value)
            return

        if isinstance(stmt, Call):
            self.eval_call(stmt, env)
            return

        if isinstance(stmt, If):
            condition = self.eval_expr(stmt.condition, env)

            if type(condition) is not bool:
                raise AuraTypeError("VIBE_CHECK requires a VIBE expression")

            if condition:
                child_env = env.new_child()
                self.exec_block(stmt.then_body, child_env)

            elif stmt.else_body is not None:
                child_env = env.new_child()
                self.exec_block(stmt.else_body, child_env)

            return

        if isinstance(stmt, Loop):
            count = self.eval_expr(stmt.count_expr, env)

            if not isinstance(count, int):
                raise AuraTypeError("COOK_FOR requires an integer loop_count")

            if count < 0:
                raise AuraRuntimeError("COOK_FOR does not accept negative counts")

            for i in range(count):
                iter_env = env.new_child({stmt.loop_var: i})
                self.exec_block(stmt.body, iter_env)

            return

        if isinstance(stmt, Return):
            value = self.eval_expr(stmt.value, env)
            raise ReturnSignal(value)

        raise AuraRuntimeError(f"Unknown statement: {stmt}")

    # -------------------------
    # Literal resolution
    # -------------------------
    def _resolve_literal(self, value, env):
        """
        Resolves dynamic values inside Literal containers.

        Example:
            Literal({
                "action": "debug",
                "meta": Var("j3")
            })

        becomes:
            {
                "action": "debug",
                "meta": value_of_j3
            }

        This is important because JSON/JASON literals may now contain
        variables, function calls, arithmetic expressions, etc.
        """
        if isinstance(value, dict):
            return {
                key: self._resolve_literal(inner_value, env)
                for key, inner_value in value.items()
            }

        if isinstance(value, list):
            return [
                self._resolve_literal(item, env)
                for item in value
            ]

        # If the value is an AST expression, evaluate it.
        if isinstance(value, (Var, Literal, BinaryOp, UnaryOp, Call)):
            return self.eval_expr(value, env)

        # Primitive values stay as they are.
        # Important: strings here are string literals, not variable names.
        return value

    # -------------------------
    # Expressions
    # -------------------------
    def eval_expr(self, expr, env):
        if isinstance(expr, Literal):
            return self._resolve_literal(expr.value, env)

        if isinstance(expr, Var):
            return self.resolve_var(env, expr.name)

        if isinstance(expr, Call):
            return self.eval_call(expr, env)

        if isinstance(expr, UnaryOp):
            value = self.eval_expr(expr.expr, env)

            if expr.op == "REKT":
                if type(value) is not bool:
                    raise AuraTypeError("REKT requires VIBE")
                return not value

            raise AuraRuntimeError(f"Unknown unary operator: {expr.op}")

        if isinstance(expr, BinaryOp):
            left = self.eval_expr(expr.left, env)
            right = self.eval_expr(expr.right, env)
            return self.eval_binary(expr.op, left, right)

        # Important:
        # Do NOT resolve raw strings as variables here.
        # Variables must be represented as Var(...).
        # Raw strings are literal values.
        return expr

    # -------------------------
    # Binary operators
    # -------------------------
    def eval_binary(self, op, left, right):
        # Arithmetic
        if op == "PLUS":
            self._ensure_number(left, right, op)
            return left + right

        if op == "MINUS":
            self._ensure_number(left, right, op)
            return left - right

        if op == "TIMES":
            self._ensure_number(left, right, op)
            return left * right

        if op == "DIVIDED":
            self._ensure_number(left, right, op)

            if right == 0:
                raise AuraRuntimeError("zero division")

            return left / right

        # Comparisons
        if op in ("ME_TOO", "=="):
            return left == right

        if op in ("BIG", ">", "&gt;"):
            return left > right

        if op in ("SMALL", "<", "&lt;"):
            return left < right

        # Boolean logic
        if op == "AND":
            if type(left) is not bool or type(right) is not bool:
                raise AuraTypeError("AND requires two VIBE values")
            return left and right

        if op == "OR":
            if type(left) is not bool or type(right) is not bool:
                raise AuraTypeError("OR requires two VIBE values")
            return left or right

        raise AuraRuntimeError(f"Unknown binary operator: {op}")

    def _ensure_number(self, left, right, op):
        if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
            raise AuraTypeError(f"{op} requires NUMBER")

    # -------------------------
    # Functions / Builtins
    # -------------------------
    def eval_call(self, call: Call, env):
        if call.name not in self.builtins:
            raise AuraRuntimeError(f"Unknown function: {call.name}")

        args = [
            self.eval_expr(arg, env)
            for arg in call.args
        ]

        return self.builtins[call.name](*args)