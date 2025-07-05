from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener

from fablex.__gen__.FablexParser import FablexParser
from fablex.__gen__.FablexLexer import FablexLexer

from fablex.error import syntax_error
from fablex.types import FablexSyntaxMessage


class SyntaxErrorCollector(ErrorListener):
    errors: list[FablexSyntaxMessage]

    def __init__(self):
        super(SyntaxErrorCollector, self).__init__()
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        # TODO: What other info can we collect from here?
        error = FablexSyntaxMessage(line=line, column=column, message=msg)
        self.errors.append(error)


def parse_expression_tree(expression: str) -> FablexParser.ParseContext:
    input_stream = InputStream(expression)
    lexer = FablexLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = FablexParser(stream)

    error_collector = SyntaxErrorCollector()
    parser.removeErrorListeners()
    parser.addErrorListener(error_collector)
    tree = parser.parse()

    if error_collector.errors:
        raise syntax_error(error_collector.errors)

    return tree
