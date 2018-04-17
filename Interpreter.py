from antlr4 import *
from gen.AtestatParser import AtestatParser
from gen.AtestatLexer import AtestatLexer
from typing import List
from help import Help
import math


class Interpreter:

    code_vars = None
    functions = None
    input: FileStream
    i = 0
    last_returned_value = None
    in_len = 0
    echo = None

    def __init__(self, input: InputStream, code_vars, functions, upper_interpreter, print, clean_afterwards=True):
        self.input = input
        self.code_vars = code_vars
        self.functions = functions
        self.i = 0
        self.upper_interpreter = upper_interpreter
        self.echo = print
        lexer = AtestatLexer(input)
        stream = CommonTokenStream(lexer)
        parser = AtestatParser(stream)
        tree = parser.instructions()
        self.in_len = len(tree.fncall())
        varlen = len(code_vars.keys)
        while self.i < self.in_len:
            self.last_returned_value = self.interpret(tree.fncall(self.i))
            self.i += 1
        # removes local variables after use
        if clean_afterwards:
            for i in range(varlen, len(code_vars.keys)):
                code_vars.values.pop(i)
                code_vars.keys.pop(i)

    def get_number(self, number: AtestatParser.Number):
        return float(str(number))

    def analyze_math_expr(self, math_expr: AtestatParser.MathExprContext):
        if math_expr.Number() is not None:
            return self.get_number(math_expr.Number())
        elif math_expr.ID() is not None:
            math_id = str(math_expr.ID())
            if math_id in self.code_vars.get_keys():
                return float(self.code_vars.get(math_id))
            else:
                return 0
        elif math_expr.mathFunction() is not None:
            return self.resolve_math_function(math_expr.mathFunction())
        elif math_expr.LPARAN() is not None:
            return self.analyze_math_expr(math_expr.mathExpr(0))
        else:
            left_op = float(self.analyze_math_expr(math_expr.mathExpr(0)))
            right_op = float(self.analyze_math_expr(math_expr.mathExpr(1)))
            if math_expr.POW() is not None:
                return pow(left_op, right_op)
            elif math_expr.TIMES() is not None:
                return left_op * right_op
            elif math_expr.DIV() is not None:
                return left_op / right_op
            elif math_expr.PLUS() is not None:
                return left_op + right_op
            elif math_expr.MINUS() is not None:
                return left_op - right_op

    def resolve_math_function(self, math_function:  AtestatParser.MathFunctionContext):
        return self.execute_math(str(math_function.ID()), self.analyze_math_expr(math_function.mathExpr()))

    def execute_math(self, mfnid, arg):
        if mfnid == "sin":
            return math.sin(arg)
        elif mfnid == "cos":
            return math.cos(arg)
        elif mfnid == "tg":
            return math.tan(arg)
        elif mfnid == "ctg":
            return 1 / math.tan(arg)
        elif mfnid == "ceil":
            return math.ceil(arg)
        elif mfnid == "floor":
            return math.floor(arg)
        elif mfnid == "round":
            return round(arg)
        elif mfnid == "abs":
            return math.fabs(arg)
        elif mfnid == "arcsin":
            return math.asin(arg)
        elif mfnid == "arccos":
            return math.acos(arg)
        elif mfnid == "arctg":
            return math.atan(arg)
        elif mfnid == "arcctg":
            return math.atan(1/arg)
        elif mfnid == "deg":
            return math.degrees(arg)
        elif mfnid == "rad":
            return math.radians(arg)
        elif mfnid == "ln":
            return math.log(arg)
        elif mfnid == "lg":
            return math.log10(arg)
        elif mfnid == "log":
            return math.log2(arg)
        else:
            return self.functions.execute("math__" + mfnid, [arg], self)

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

    def set_i(self, i):
        self.i = i

    def goto(self, levels_up, line):
        if levels_up == 0:
            # subtract 1 because interpreter will increase by one
            self.set_i(line - 1)
        elif self.upper_interpreter is not None:
            self.set_i(self.in_len)
            self.upper_interpreter.goto(levels_up - 1, line)

    def print_with_indent(self, to_print, indent_level):
        if isinstance(to_print, str):
            self.echo("\t"*indent_level + to_print)
        else:
            for key, value in to_print.items():
                self.echo("\t"*indent_level + key + ":")
                self.print_with_indent(value, indent_level + 1)

    def execute(self, fnid, args):
        args: List[AtestatParser.ArgContext]
        sfnid = str(fnid)
        if sfnid == "help":
            cmd = None
            attr = None
            if len(args) > 0:
                cmd = str(self.resolve_arg(args[0], True))
            if len(args) > 1:
                attr = str(self.resolve_arg(args[0], True))
            to_print = Help.help
            if cmd is not None:
                to_print = to_print[cmd]
            if attr is not None:
                to_print = to_print[attr]
            self.print_with_indent(to_print, 0)
        elif sfnid == "print":
            res_args = []
            for arg in args:
                res_args.append(str(self.resolve_arg(arg)))
            self.echo(" ".join(res_args))
            return None
        elif sfnid == "return":
            self.set_i(self.in_len)
            return self.resolve_arg(args[0])
        elif sfnid == "set_var":
            self.code_vars.set(self.resolve_arg(args[0], True), self.resolve_arg(args[1]))
            return None
        elif sfnid == "unset_var":
            self.code_vars.remove(self.resolve_arg(args[0], True))
            return None
        elif sfnid == "def_func":
            instructions = ""
            for i in range(2, len(args)):
                instructions += self.resolve_arg(args[i], True) + " "
            fn_args = self.resolve_arg(args[1], True)
            fn_id = self.resolve_arg(args[0], True)
            self.functions.add_function(fn_id, fn_args, instructions)
            return None
        elif sfnid == "rem_func":
            fn_id = self.resolve_arg(args[0], True)
            self.functions.rem_function(fn_id)
            return None
        elif sfnid == "cmp":
            x = self.resolve_arg(args[0])
            y = self.resolve_arg(args[1])
            if x > y:
                return 1
            elif x < y:
                return -1
            else:
                return 0
        elif sfnid == "and":
            for arg in args:
                if str(self.resolve_arg(arg)) == "0.0":
                    return 0
            return 1
        elif sfnid == "or":
            for arg in args:
                if str(self.resolve_arg(arg)) != "0.0":
                    return 1
            return 0
        elif sfnid == "not":
            return str(self.resolve_arg(args[0])) == "0.0"
        elif sfnid == "if":
            x = self.resolve_arg(args[0])
            y = self.resolve_arg(args[1])
            ret = None
            if str(x) == str(y):
                instructions = ""
                for i in range(2, len(args)):
                    instructions += self.resolve_arg(args[i], True) + " "
                Interpreter(InputStream(instructions), self.code_vars, self.functions, self, self.echo)
            return ret
        elif sfnid == "goto":
            levels_up = int(self.resolve_arg(args[0]))
            line = int(self.resolve_arg(args[1]))
            self.goto(levels_up, line)
            return None
        elif sfnid == "import":
            filename = str(self.resolve_arg(args[0]))
            Interpreter(FileStream(filename), self.code_vars, self.functions, None, self.echo)
        elif sfnid == "read":
            var_id = self.resolve_arg(args[0], True)
            prompt = "> "
            if len(args) > 1:
                prompt = self.resolve_arg(args[0])
            cont = input(prompt)
            self.code_vars.set(var_id, cont)
        elif sfnid == "def_math_func":
            instructions = ""
            for i in range(1, len(args)):
                instructions += self.resolve_arg(args[i], True) + " "
            fn_id = self.resolve_arg(args[0], True)
            self.functions.add_function("math__" + fn_id, ['__x'], instructions)
            return None
        elif sfnid == "rem_math_func":
            fn_id = self.resolve_arg(args[0], True)
            self.functions.rem_function("math__" + fn_id)
            return None
        elif sfnid == "add_item":
            var = self.resolve_arg(args[0], True)
            index = self.resolve_arg(args[1], False)
            val = self.resolve_arg(args[2], False)
            old_list = self.code_vars.get(var)
            if not isinstance(old_list, list):
                return None
            new_list = old_list[:]
            new_list.insert(int(index), val)
            self.code_vars.set(var, new_list)
            return None
        elif sfnid == "get_item":
            var = self.resolve_arg(args[0], True)
            index = int(self.resolve_arg(args[1], False))
            vals = self.code_vars.get(var)
            if not isinstance(vals, list):
                return None
            if len(vals) <= index:
                return None
            return vals[index]
        elif sfnid == "remove_item":
            pass
        elif sfnid == "comment":
            pass
        elif sfnid == "is_none":
            pass
        else:
            return self.functions.execute(sfnid, args, self)
        return None

    def interpret(self, fncall: AtestatParser.FncallContext):
        return self.execute(fncall.ID(), fncall.arg())
