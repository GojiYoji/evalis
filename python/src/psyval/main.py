from antlr4 import CommonTokenStream, InputStream
from psyval.__gen__.grammar.PsyvalParser import PsyvalParser
from psyval.__gen__.grammar.PsyvalLexer import PsyvalLexer
from psyval.ast import PsyvalAstBuilder
from psyval.eval import PsyvalEval


def main(argv):
    # 2. Create input stream
    input_stream = InputStream(argv[1])
    print(f"Evaluating this expression: {argv[1]}")

    # 3. Create lexer
    lexer = PsyvalLexer(input_stream)

    # 4. Create token stream
    stream = CommonTokenStream(lexer)

    # 5. Create parser
    parser = PsyvalParser(stream)

    # 6. Parse using `parse`
    tree = parser.parse()

    if parser.getNumberOfSyntaxErrors() > 0:
        print("syntax errors!!!!")
        exit(1)

    builder = PsyvalAstBuilder()
    ast = builder.visit(tree)

    evaluator = PsyvalEval()
    result = evaluator.evaluate(
        ast,
        {
            "count": 5,
            "foo": [{"title": "HELLO"}, {"title": "GOODBYE"}],
            "title_key": "title",
        },
    )

    print(f"The result={result}")
