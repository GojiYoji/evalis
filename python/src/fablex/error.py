from typing import Iterable

from fablex.types import FablexSyntaxMessage


CODE_UNKNOWN = "UNKNOWN"
CODE_SYNTAX_ERROR = "SYNTAX_ERROR"


class FablexError(Exception):
    def __init__(self, message: str, code: str | None = None):
        code = code or CODE_UNKNOWN

        super().__init__(message, code)
        self._message = message
        self._code = code

    @property
    def message(self) -> str:
        return self._message

    @property
    def code(self) -> str:
        return self._code

    def __str__(self):
        return f"[Fablex::{self.code}] {self.message}"


def syntax_error(errors: Iterable[FablexSyntaxMessage]) -> FablexError:
    message = f"""Syntax errors found while tring to evaluate the expression:
{"\n".join((f"{x.line}:{x.column}: {x.message}" for x in errors))}
"""
    return FablexError(message=message, code=CODE_SYNTAX_ERROR)
