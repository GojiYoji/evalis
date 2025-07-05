from dataclasses import dataclass


@dataclass(frozen=True)
class FablexEvalOptions:
    should_null_on_bad_access: bool = False


@dataclass(frozen=True)
class FablexSyntaxMessage:
    line: int
    column: int
    message: str
