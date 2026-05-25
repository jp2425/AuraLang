from pathlib import Path

from lark import Lark, UnexpectedInput

from .parsing.transformer import AuraTransformer
from .parsing.parser import load_grammar
from .runtime.interpreter import AuraInterpreter, AuraRuntimeError


class AuraLang:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent
        self.default_grammar_path = self.base_dir / "grammar" / "grammar.lark"

    def _build_parser(self, grammar_path: str) -> Lark:
        """
        Builds the parser
        :param grammar_path: grammar of AuraLang
        :return:
        """
        grammar = load_grammar(grammar_path)

        return Lark(
            grammar,
            start="start",
            parser="earley",
            lexer="dynamic",
        )

    def run_program(self, program: str, **kwargs):
        """
        Function that is used to run a AuraLang program
        :param program: text with the program
        :return: return value of the program
        """

        parser = self._build_parser(str(self.default_grammar_path))

        try:
            tree = parser.parse(program)
        except UnexpectedInput as e:
            print("=== PARSE ERROR ===")
            return str(e)

        transformer = AuraTransformer()
        ast = transformer.transform(tree)



        interpreter = AuraInterpreter(inputs=kwargs)

        try:
            result = interpreter.run(ast)
        except AuraRuntimeError as e:
            print("=== Execution Error ===")
            return str(e)


        return result
