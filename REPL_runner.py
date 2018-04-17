import sys
from antlr4 import *
from gen.AtestatLexer import AtestatLexer
from gen.AtestatParser import AtestatParser
from Interpreter import Interpreter
from VariableCtx import VariableCTX
from FunctionCtx import FunctionCTX

code_vars = VariableCTX()
functions = FunctionCTX(code_vars)


def check_input(input):
    check = 0
    for c in input:
        if c == '(':
            check += 1
        elif c == ')':
            check -= 1
    return check == 0


def main():
    while True:
        line = input(">>> ")
        if line == "-1":
            break
        while not check_input(line):
            add_line = input("  ... ")
            line += add_line
        result = Interpreter(InputStream(line), code_vars, functions, None, print, False)
        print("<<< {}".format(result.last_returned_value))


if __name__ == '__main__':
    main()
