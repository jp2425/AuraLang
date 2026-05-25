from ..ast_nodes import Call


class FunctionTransformer:
    def function_call(self, items):
        if not items:
            raise ValueError("Empty function call")

        name = self._to_name(items[0])
        args = [self._to_expr(arg) for arg in items[1:]]

        return Call(name=name, args=args)

    def function_parameter(self, items):
        return self._to_expr(self._single("function_parameter", items))