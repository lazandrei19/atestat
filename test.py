import sys
from antlr4 import *
from gen.AtestatLexer import AtestatLexer
from gen.AtestatParser import AtestatParser


def main(argv):
    input = FileStream(argv[1])
    lexer = AtestatLexer(input)
    stream = CommonTokenStream(lexer)
    parser = AtestatParser(stream)
    tree = parser.instructions()
    for fncall in tree.fncall():
        print(fncall.ID())


if __name__ == '__main__':
    print(sys.argv)
    main(sys.argv)
