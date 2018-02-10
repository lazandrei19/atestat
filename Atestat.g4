grammar Atestat;
instructions : fncall+ EOF;
ID: [a-zA-Z_][a-zA-Z0-9_]* ;
LPARAN : '(' ;
RPARAN : ')' ;
LSQBRACK : '[' ;
RSQBRACK : ']' ;
COMMA : ',' ;
fncall : LPARAN ID arg* RPARAN ;
arg : fncall
    | literal
    | ID ;
literal : StringLiteral
        | IntLiteral
        | FloatLiteral
        | arrayLiteral;
StringLiteral : '"' ~('\r' | '\n' | '"')* '"' ;
IntLiteral : '-'? [0-9]+ ;
FloatLiteral : '-'? [0-9]+ '.' [0-9]+ ;
arrayLiteral : LSQBRACK (arg COMMA)* arg? RSQBRACK ;
WS : (' ' | '\n' | '\t' | '\r')+ -> skip;
