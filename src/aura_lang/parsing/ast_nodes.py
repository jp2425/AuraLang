from dataclasses import dataclass
from typing import Any, List, Optional


@dataclass
class Program:
    inputs: List[str]
    body: List[Any]


@dataclass
class DeclTarget:
    name: str


@dataclass
class Assign:
    name: str
    value: Any
    declare: bool = False


@dataclass
class Var:
    name: str


@dataclass
class Literal:
    value: Any


@dataclass
class BinaryOp:
    op: str
    left: Any
    right: Any


@dataclass
class UnaryOp:
    op: str
    expr: Any


@dataclass
class Call:
    name: str
    args: List[Any]


@dataclass
class If:
    condition: Any
    then_body: List[Any]
    else_body: Optional[List[Any]] = None


@dataclass
class Loop:
    count_expr: Any
    loop_var: str
    body: List[Any]


@dataclass
class Return:
    value: Any