from pathlib import Path
from lark import Lark


def load_grammar(path = "grammar/grammar.lark") -> str:
    project_root = Path(__file__).resolve().parent.parent
    grammar_path = project_root / path

    with open(grammar_path, "r", encoding="utf-8") as f:
        return f.read()


def build_parser(grammar_path: str) -> Lark:
    grammar = load_grammar(grammar_path)

    return Lark(
        grammar,
        start="start",
        parser="earley",
        lexer="dynamic",
    )
