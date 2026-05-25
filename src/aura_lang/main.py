import json
import sys
from pathlib import Path
from .AuraLang import AuraLang
from .parsing.transformers.base import BaseTransformer
from .parsing.transformers.literals import LiteralTransformer
from .parsing.transformers.expressions import ExpressionTransformer
from .parsing.transformers.functions import FunctionTransformer
from .parsing.transformers.statements import StatementTransformer
from .parsing.transformers.program import ProgramTransformer


class AuraTransformer(
    BaseTransformer,
    LiteralTransformer,
    ExpressionTransformer,
    FunctionTransformer,
    StatementTransformer,
    ProgramTransformer
):
    pass


def main():
    if len(sys.argv) < 2:
        print("aura file.aura [parameter=value1 parameter2=value2]")
        sys.exit(1)

    path = Path(sys.argv[1])

    if not path.exists():
        print(f"Error:'{path}' not found.")
        sys.exit(1)

    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading file {e}")
        sys.exit(1)
    input_kwargs = {}
    for arg in sys.argv[2:]:
        if "=" in arg:
            key, value = arg.split("=", 1)
            value = value.strip()

            # Try to parse complex types (arrays, dicts) or booleans/numbers via JSON
            try:
                # json.loads handles: [1,2,3], {"a":1}, true/false, numbers, and quoted strings
                parsed_value = json.loads(value)
                input_kwargs[key] = parsed_value
                print(parsed_value, "  ", type(parsed_value))
            except json.JSONDecodeError:
                # Fallback to raw string if it's not valid JSON syntax
                print(value, "  ", type(value))
                input_kwargs[key] = value
        else:
            print(f"Warning '{arg}' was ignored since it does not follow the convention - key=value")
    lang = AuraLang()
    result = lang.run_program(content,input_kwargs)

    if result is not None:
        print("======== OUTPUT ========")
        print(result)



if __name__ == "__main__":
    main()