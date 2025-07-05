grammar Fablex;

parse
    : expr EOF
    ;

expr
    // NOT has the highest precedence among unary ops
    : 'not' expr                              # NotExpr

    // Multiplication and division
    | expr op=('*' | '/') expr               # MulDivExpr

    // Addition and subtraction
    | expr op=('+' | '-') expr               # AddSubExpr

    // Relational (<, >, etc.)
    | expr op=('<' | '<=' | '>' | '>=') expr # RelationalExpr

    // Equality (==, !=)
    | expr op=('==' | '!=') expr             # EqualityExpr

    // AND
    | expr op='and' expr                     # AndExpr

    // OR
    | expr op='or' expr                      # OrExpr

    // Atom: literals, identifiers, parens
    | atom                                   # AtomExpr
    ;

atom
    : literal
    | identifier accessSuffix*
    | '(' expr ')'
    ;

accessSuffix
    : '.' identifier
    | '[' expr ']'
    ;

literal
    : number
    | stringLiteral
    | boolean
    | 'null'
    ;

number
    : INT
    | FLOAT
    ;

boolean
    : 'true'
    | 'false'
    ;

identifier
    : IDENTIFIER
    ;

stringLiteral
    : STRING
    ;

/* Tokens */

IDENTIFIER
    : [a-zA-Z_] [a-zA-Z0-9_]*
    ;

INT
    : [0-9]+
    ;

FLOAT
    : [0-9]+ '.' [0-9]+
    ;

STRING
    : '"' ( ~["\\] | '\\' . )* '"'
    ;

WS
    : [ \t\r\n]+ -> skip
    ;

