from antlr4 import *
from gen.AtestatParser import AtestatParser
from VariableCtx import VariableCTX


class Interpreter:

    code_vars = VariableCTX()

    def get_number(self, number: AtestatParser.Number):
        return float(str(number))

    def analyze_math_expr(self, math_expr: AtestatParser.MathExprContext):
        if math_expr.Number() is not None:
            return self.get_number(math_expr.Number())
        elif math_expr.ID() is not None:
            math_id = str(math_expr.ID())
            if math_id in self.code_vars.keys():
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

    def resolve_literal(self, literal: AtestatParser.LiteralContext):
        if literal.arrayLiteral() is not None:
            array: AtestatParser.ArrayLiteralContext
            array = literal.arrayLiteral()
            return self.resolve_args(array.arg())
        elif literal.mathFunctionLiteral() is not None:
            math_function: AtestatParser.MathFunctionLiteralContext
            math_function = literal.mathFunctionLiteral()
            return self.analyze_math_expr(math_function.mathExpr())
        elif literal.StringLiteral() is not None:
            return str(literal.StringLiteral())
        elif literal.Number() is not None:
            return self.get_number(literal.Number())

    def resolve_args(self, args):
        resolved_args = []
        for arg in args:
            arg: AtestatParser.ArgContext
            if arg.fncall() is not None:
                resolved_args.append(self.interpret(arg.fncall()))
            elif arg.literal() is not None:
                resolved_args.append(self.resolve_literal(arg.literal()))
            elif arg.ID() is not None:
                resolved_args.append(self.code_vars.get(arg.ID()))
        return resolved_args

    def execute(self, fnid, args):
        pass

    def interpret(self, fncall: AtestatParser.FncallContext):
        args = self.resolve_args(fncall.arg())
        return self.execute(fncall.ID(), args)
