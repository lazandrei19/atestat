grammar Atestat;
ID: [a-zA-Z_][a-zA-Z0-9_]* ;
LPARAN : '(' ;
RPARAN : ')' ;
LSQBRACK : '[' ;
RSQBRACK : ']' ;
COMMA : ',' ;
MATHFSTART : 'f"' ;
DBLQUOTE : '"' ;
PLUS : '+' ;
MINUS : '-' ;
TIMES : '*' ;
DIV : '/' ;
POW : '^' ;
Number : IntLiteral | FloatLiteral ;
StringLiteral : (DBLQUOTE|MATHFSTART) ~('\r' | '\n' | '"')* DBLQUOTE ;
IntLiteral : MINUS? [0-9]+ ;
FloatLiteral : MINUS? [0-9]+ '.' [0-9]+ ;
instructions : fncall+ EOF;
fncall : LPARAN ID arg* RPARAN ;
arg : fncall
    | literal
    | ID ;
literal : StringLiteral
        | Number
        | arrayLiteral ;
arrayLiteral : LSQBRACK (arg COMMA)* arg? RSQBRACK ;
mathFunctionLiteral : MATHFSTART mathExpr DBLQUOTE ;
mathExpr : mathExpr POW mathExpr
         | mathExpr (TIMES | DIV) mathExpr
         | mathExpr (PLUS | MINUS) mathExpr
         | LPARAN mathExpr RPARAN
         | mathFunction
         | Number
         | ID;
mathFunction : ID LPARAN mathExpr RPARAN ;
WS : (' ' | '\n' | '\t' | '\r')+ -> skip;