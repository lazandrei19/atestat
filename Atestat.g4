grammar Atestat;
instructions : fncall+ EOF;
X : [xX] ;
ID: [a-zA-Z_][a-zA-Z0-9_]* ;
LPARAN : '(' ;
RPARAN : ')' ;
LSQBRACK : '[' ;
RSQBRACK : ']' ;
COMMA : ',' ;
DBLQUOTE : '"' ;
MINUS : '-' ;
MATHFSTART : 'f"' ;
fncall : LPARAN ID arg* RPARAN ;
arg : fncall
    | literal
    | ID ;
literal : StringLiteral
        | Number
        | arrayLiteral
        | mathFunctionLiteral ;
Number : IntLiteral | FloatLiteral ;
StringLiteral : DBLQUOTE ~('\r' | '\n' | '"')* DBLQUOTE ;
IntLiteral : MINUS? [0-9]+ ;
FloatLiteral : MINUS? [0-9]+ '.' [0-9]+ ;
arrayLiteral : LSQBRACK (arg COMMA)* arg? RSQBRACK ;
mathFunctionLiteral : MATHFSTART mathExpr DBLQUOTE ;
mathExpr : LPARAN mathExpr RPARAN
         | X
         | mathFunction
         | Number mathOp Number
         | Number mathOp mathExpr
         | mathExpr mathOp Number
         | mathExpr mathOp mathExpr ;
mathOp : ('+' | '-' | '*' | '/' | '^') ;
mathFunction : ID LPARAN X RPARAN ;
WS : (' ' | '\n' | '\t' | '\r')+ -> skip;