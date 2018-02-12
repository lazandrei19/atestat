import sys
from antlr4 import *
from gen.AtestatLexer import AtestatLexer
from gen.AtestatParser import AtestatParser
from Interpreter import Interpreter

def main(argv):
    input = FileStream(argv[1])
    lexer = AtestatLexer(input)
    stream = CommonTokenStream(lexer)
    parser = AtestatParser(stream)
    tree = parser.instructions()
    interpreter = Interpreter()
    for fncall in tree.fncall():
        interpreter.interpret(fncall)


if __name__ == '__main__':
    print(sys.argv)
    main(sys.argv)
