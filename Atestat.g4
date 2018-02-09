grammar Atestat;
instructions : fncall+ EOF;
ID: [a-zA-Z_][a-zA-Z0-9_]* ;
LPARAN : '(' ;
RPARAN : ')' ;
fncall : LPARAN ID arg* RPARAN ;
arg : fncall
    | Literal
    | ID ;
Literal : StringLiteral
        | IntLiteral
        | FloatLiteral ;
StringLiteral : '"' ~('\r' | '\n' | '"')* '"' ;
IntLiteral : '-'? [0-9]+ ;
FloatLiteral : '-'? [0-9]+ '.' [0-9]+ ;
WS : (' ' | '\n' | '\t' | '\r')+ -> skip;