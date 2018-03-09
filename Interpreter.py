from antlr4 import *
from gen.AtestatParser import AtestatParser
from VariableCtx import VariableCTX
from FunctionCtx import FunctionCTX
from typing import List


class Interpreter:

    code_vars = VariableCTX()
    functions = FunctionCTX(code_vars)
    input: FileStream

    def __init__(self, input: FileStream):
        self.input = input

    def get_number(self, number: AtestatParser.Number):
        return float(str(number))

    def analyze_math_expr(self, math_expr: AtestatParser.MathExprContext):
        if math_expr.Number() is not None:
            return self.get_number(math_expr.Number())
        elif math_expr.ID() is not None:
            math_id = str(math_expr.ID())
            if math_id in self.code_vars.get_keys():
                return self.code_vars.get(math_id)
            else:
                return 0
        elif math_expr.mathFunction() is not None:
            return self.resolve_math_function(math_expr.mathFunction())
        elif math_expr.POW() is not None:
            return pow(self.analyze_math_expr(math_expr.mathExpr(0)), self.analyze_math_expr(math_expr.mathExpr(1)))
        elif math_expr.TIMES() is not None or math_expr.DIV() is not None:
            if math_expr.TIMES() is not None:
                return self.analyze_math_expr(math_expr.mathExpr(0)) * self.analyze_math_expr(math_expr.mathExpr(1))
            else:
                return self.analyze_math_expr(math_expr.mathExpr(0)) / self.analyze_math_expr(math_expr.mathExpr(1))
        elif math_expr.PLUS() is not None or math_expr.MINUS() is not None:
            if math_expr.PLUS() is not None:
                return self.analyze_math_expr(math_expr.mathExpr(0)) + self.analyze_math_expr(math_expr.mathExpr(1))
            else:
                return self.analyze_math_expr(math_expr.mathExpr(0)) - self.analyze_math_expr(math_expr.mathExpr(1))

    def resolve_math_function(self, math_function:  AtestatParser.MathFunctionContext):
        return self.execute_math(math_function.ID(), self.analyze_math_expr(math_function.mathExpr()))

    def execute_math(self, mfnid, arg):
        pass

    def resolve_literal(self, literal: AtestatParser.LiteralContext, return_string=False):
        if literal.arrayLiteral() is not None:
            array: AtestatParser.ArrayLiteralContext
            array = literal.arrayLiteral()
            result = []
            for arg in array.arg():
                result.append(self.resolve_arg(arg, return_string))
            return result
        elif literal.mathFunctionLiteral() is not None:
            math_function: AtestatParser.MathFunctionLiteralContext
            math_function = literal.mathFunctionLiteral()
            if return_string:
                return str(math_function.mathExpr())
            return self.analyze_math_expr(math_function.mathExpr())
        elif literal.StringLiteral() is not None:
            return str(literal.StringLiteral())[1:-1]
        elif literal.Number() is not None:
            return self.get_number(literal.Number())

    def resolve_arg(self, arg, return_string=False):
        resolved_arg = None
        arg: AtestatParser.ArgContext
        if arg.fncall() is not None:
            if return_string:
                x: AtestatParser.FncallContext
                x = arg.fncall()
                return self.input.getText(x.start.start, x.stop.stop)
            resolved_arg = self.interpret(arg.fncall())
        elif arg.literal() is not None:
            resolved_arg = self.resolve_literal(arg.literal(), return_string)
        elif arg.ID() is not None:
            if return_string:
                return str(arg.ID())
            resolved_arg = self.code_vars.get(str(arg.ID()))
        return resolved_arg

    def execute(self, fnid, args):
        args: List[AtestatParser.ArgContext]
        sfnid = str(fnid)
        if sfnid == "print":
            res_args = []
            for arg in args:
                res_args.append(str(self.resolve_arg(arg)))
            print(" ".join(res_args))
            return None
        elif sfnid == "return":
            return self.resolve_arg(args[0])
        elif sfnid == "define_var":
            self.code_vars.init(self.resolve_arg(args[0], False), self.resolve_arg(args[1]))
        elif sfnid == "set_var":
            self.code_vars.set(self.resolve_arg(args[0], False), self.resolve_arg(args[1]))
        elif sfnid == "unset_var":
            self.code_vars.remove(self.resolve_arg(args[0], False))
        elif sfnid == "define_func":
            instructions = ""
            for i in range(2, len(args)):
                instructions += self.resolve_arg(args[i], True) + " "
            fn_args = self.resolve_arg(args[1], True)
            fn_id = self.resolve_arg(args[0], True)
            self.functions.add_function(fn_id, fn_args, instructions)
        else:
            return self.functions.execute(sfnid, args, self)
        return None

    def interpret(self, fncall: AtestatParser.FncallContext):
        return self.execute(fncall.ID(), fncall.arg())
