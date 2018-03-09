from antlr4 import *
from gen.AtestatParser import AtestatParser
from gen.AtestatLexer import AtestatLexer
from VariableCtx import VariableCTX
from Interpreter import Interpreter

class FunctionCTX:
    fnids = []
    args_lists = []
    instructions = []

    ctx = None

    def __init__(self, varctx):
        self.ctx = varctx

    def add_function(self, fnid, args, instr):
        self.fnids.append(fnid)
        self.args_lists.append(args)
        self.instructions.append(instr)

    def execute(self, fnid, args, interpreter):
        fnidi = self.fnids.index(fnid)
        if fnidi == -1:
            return None
        self.ctx: VariableCTX
        for i in range(len(args)):
            self.ctx.init(self.args_lists[fnidi][i], interpreter.resolve_arg(args[i]))
        interpreter = Interpreter(InputStream(self.instructions[fnidi]), self.ctx, self)
        for i in range(len(args)):
            self.ctx.remove(self.args_lists[fnidi][i])
        return interpreter.last_returned_value

