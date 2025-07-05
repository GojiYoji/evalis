from antlr4 import CommonTokenStream, InputStream
from fablex.__gen__.grammar.FablexParser import FablexParser
from fablex.__gen__.grammar.FablexLexer import FablexLexer
from fablex.ast import FablexAstBuilder
from fablex.eval import FablexEval


def main(argv):
    # 2. Create input stream
    input_stream = InputStream(argv[1])
    print(f"Evaluating this expression: {argv[1]}")

    # 3. Create lexer
    lexer = FablexLexer(input_stream)

    # 4. Create token stream
    stream = CommonTokenStream(lexer)

    # 5. Create parser
    parser = FablexParser(stream)

    # 6. Parse using `parse`
    tree = parser.parse()

    if parser.getNumberOfSyntaxErrors() > 0:
        print("syntax errors!!!!")
        exit(1)

    builder = FablexAstBuilder()
    ast = builder.visit(tree)

    evaluator = FablexEval()
    result = evaluator.evaluate(
        ast,
        {
            "count": 5,
            "foo": [{"title": "HELLO"}, {"title": "GOODBYE"}],
            "title_key": "title",
        },
    )

    print(f"The result={result}")
