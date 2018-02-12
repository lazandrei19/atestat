from antlr4 import *
from gen.AtestatParser import AtestatParser

class Interpreter:
    def interpret (self, fncall: AtestatParser.FncallContext):
        print(fncall.ID())