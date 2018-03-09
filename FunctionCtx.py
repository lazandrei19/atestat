from antlr4 import *
from gen.AtestatParser import AtestatParser
from gen.AtestatLexer import AtestatLexer
from VariableCtx import VariableCTX

class FunctionCTX:
    fnids = []
    args_lists = []
    instrunctions = []

    ctx = None

    def __init__(self, varctx):
        self.ctx = varctx

    def add_function(self, fnid, args, instr):
        print(fnid)
        self.fnids.append(fnid)
        self.args_lists.append(args)
        self.instrunctions.append(instr)

    def execute(self, fnid, args, interpreter):
        #FIXME this is where the project breaks :'(

        fnidi = self.fnids.index(fnid)
        if fnidi == -1:
            return None
        self.ctx: VariableCTX
        for i in range(len(args)):
            self.ctx.init(self.args_lists[fnidi][i], args[i])
        lexer = AtestatLexer(InputStream(self.instrunctions[fnidi]))
        stream = CommonTokenStream(lexer)
        parser = AtestatParser(stream)
        tree = parser.instructions()
        ret = None
        for fncall in tree.fncall():
            ret = interpreter.interpret(fncall)
        for arg in args:
            self.ctx.remove(arg)
        return ret

