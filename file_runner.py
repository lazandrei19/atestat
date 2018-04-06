import sys
from antlr4 import *
from gen.AtestatLexer import AtestatLexer
from gen.AtestatParser import AtestatParser
from Interpreter import Interpreter
from VariableCtx import VariableCTX
from FunctionCtx import FunctionCTX


def main(argv):
    input = FileStream(argv[1])
    code_vars = VariableCTX()
    functions = FunctionCTX(code_vars)
    Interpreter(input, code_vars, functions)


if __name__ == '__main__':
    main(sys.argv)
