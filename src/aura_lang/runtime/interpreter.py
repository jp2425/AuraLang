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

from collections import ChainMap


class AuraInterpreter:
    def __init__(self, inputs=None):
        # scope global
        self.env = {}
        self.inputs = inputs or {}

        self.builtins = {}
        ## Intanciate the standard library and others
        StdLib(self.builtins)
        Letters(self.builtins)

    # -------------------------
    # API principal
    # -------------------------
    def run(self, program: Program):
        for name in program.inputs:
            self.env[name] = self.inputs.get(name, None)

        # The main body of the program runs in the global scope
        env = ChainMap(self.env)

        try:
            self.exec_block(program.body, env)
        except ReturnSignal as ret:
            return ret.value

        return None

    # -------------------------
    # Helpers
    # -------------------------
    def declare_var(self, env, name, value):
        """
        The main body of the program declares a variable in the current (local) scope.
        It does not propagate it outside the block.
        """
        if name in env.maps[0]:
            raise AuraRuntimeError(f"The variable '{name}' has already been declared in this block")
        env.maps[0][name] = value

    def assign_var(self, env, name, value):
        """
        Reassigns an existing variable.
        Searches from the innermost scope to the outermost and writes to the first scope where the variable exists.
        This allows changes to outer variables to be reflected outside the block.
        """
        for scope in env.maps:
            if name in scope:
                scope[name] = value
                return
        raise AuraNameError(f"Variável '{name}' não existe")

    def resolve_var(self, env, name):
        """
        Reads a variable while respecting the scope chain.
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
                # MOOD x IS_GIVING ...
                # creates only in the current scope
                self.declare_var(env, stmt.name, value)
                return

            # x IS_GIVING ...
            # Reassign within the scope where x already exists
            self.assign_var(env, stmt.name, value)
            return

        if isinstance(stmt, Call):
            self.eval_call(stmt, env)
            return

        if isinstance(stmt, If):
            condition = self.eval_expr(stmt.condition, env)
            if not isinstance(condition, bool):
                raise AuraTypeError("VIBE_CHECK requires a Boolean expression")

            # Each block within the `if` statement has its own local scope
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

            # Each iteration has its own local scope
            for i in range(count):
                iter_env = env.new_child({stmt.loop_var: i})
                self.exec_block(stmt.body, iter_env)
            return

        if isinstance(stmt, Return):
            value = self.eval_expr(stmt.value, env)
            raise ReturnSignal(value)

        raise AuraRuntimeError(f"Unknown statement: {stmt}")

    # -------------------------
    # Expressions
    # -------------------------
    def eval_expr(self, expr, env):
        if isinstance(expr, Literal):
            return expr.value

        if isinstance(expr, Var):
            return self.resolve_var(env, expr.name)

        if isinstance(expr, Call):
            return self.eval_call(expr, env)

        if isinstance(expr, UnaryOp):
            value = self.eval_expr(expr.expr, env)

            if expr.op == "REKT":
                if not isinstance(value, bool):
                    raise AuraTypeError("REKT demands VIBE")
                return not value

            raise AuraRuntimeError(f"Operator unknown: {expr.op}")

        if isinstance(expr, BinaryOp):
            left = self.eval_expr(expr.left, env)
            right = self.eval_expr(expr.right, env)
            return self.eval_binary(expr.op, left, right)

        if isinstance(expr, str):
            # fallback defensivo
            return self.resolve_var(env, expr)

        return expr

    # -------------------------
    # Binary operators
    # -------------------------
    def eval_binary(self, op, left, right):
        # Aritmética
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

        if op in ("BIG", ">"):
            return left > right

        if op in ("SMALL", "<"):
            return left < right

        # Booleanos
        if op == "AND":
            if not isinstance(left, bool) or not isinstance(right, bool):
                raise AuraTypeError("AND requires two VIBE values")
            return left and right

        if op == "OR":
            if not isinstance(left, bool) or not isinstance(right, bool):
                raise AuraTypeError("OR requires two VIBE values")
            return left or right

        raise AuraRuntimeError(f"Operador desconhecido: {op}")

    def _ensure_number(self, left, right, op):
        if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
            raise AuraTypeError(f"{op} demands NUMBER")

    # -------------------------
    # Functions / Builtins
    # -------------------------
    def eval_call(self, call: Call, env):
        if call.name not in self.builtins:
            raise AuraRuntimeError(f"Unknown function: {call.name}")
        args = [self.eval_expr(arg, env) for arg in call.args]
        return self.builtins[call.name](*args)


