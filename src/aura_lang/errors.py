class AuraError(Exception):
    """
    Classe base para todos os erros da linguagem AURA.
    Serve para poderes apanhar qualquer erro da DSL com:
        except AuraError:
            ...
    """
    pass


class AuraRuntimeError(AuraError):
    """
    Erros que acontecem durante a execução do programa.
    Exemplos:
    - divisão por zero
    - índice fora de limites
    - chamada a função desconhecida
    """
    pass


class AuraTypeError(AuraRuntimeError):
    """
    Erros de tipo em runtime.
    Exemplos:
    - PLUS entre string e número
    - SIZE num valor inválido
    - VIBE_CHECK com algo que não é booleano
    """
    pass


class AuraNameError(AuraRuntimeError):
    """
    Erros relacionados com nomes/variáveis.
    Exemplos:
    - variável não declarada
    - reatribuição de variável inexistente
    """
    pass


class AuraDeclarationError(AuraRuntimeError):
    """
    Erros de declaração.
    Exemplos:
    - variável já declarada no mesmo scope
    - tentativa de redeclaração inválida
    """
    pass


class AuraFunctionError(AuraRuntimeError):
    """
    Erros relacionados com funções/builtins.
    Exemplos:
    - função desconhecida
    - número errado de argumentos
    """
    pass


class AuraIndexError(AuraRuntimeError):
    """
    Erros de acesso por índice.
    Exemplos:
    - SPILL com índice fora dos limites
    - índice negativo (se quiseres proibir)
    """
    pass


class AuraReturnSignal(Exception):
    """
    Sinal interno usado para implementar o comportamento de DROP como return.

    Não é um 'erro' real da linguagem — é um mecanismo interno de controlo
    de fluxo para sair imediatamente da execução de um bloco/programa.
    """
    def __init__(self, value):
        self.value = value