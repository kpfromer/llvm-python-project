from ast import *
from copy import deepcopy as cp
from textwrap import indent

class Flattener:
    def __init__(self) -> None:
        self.variable_count = 0
        self.statements = []

    def create_tmp_var(self, value):
        var = "flatten_" + str(self.variable_count)
        self.variable_count += 1

        var_node = Name(id=var, ctx=Store())

        self.statements.append(Assign(targets=[var_node], value=value))

        return var_node

    def flatten_constant(self, constant):
        return constant
    
    def flatten_name(self, name):
        return name

    def flatten_unary_op(self, op):
        operand = self.flatten_expr(op.operand)
        return self.create_tmp_var(UnaryOp(op.op, operand))

    def flatten_binary_op(self, op):
        left = self.flatten_expr(op.left)
        right = self.flatten_expr(op.right)
        return self.create_tmp_var(BinOp(left, op.op, right))

    def flatten_function_call(self, call):
        flattened_args = [self.create_tmp_var(self.flatten_expr(arg)) for arg in call.args]
        if call.func.id == "print":
            self.statements.append(Call(func=call.func, args=flattened_args, keywords=[]))
        elif call.func.id == "input":
            return self.create_tmp_var(Call(func=call.func, args=flattened_args, keywords=[]))
        else:
            raise Exception("Unknown function call: " + str(call))
    
    def flatten_expr(self, expr):
        if isinstance(expr, BinOp):
            return self.flatten_binary_op(expr)
        elif isinstance(expr, UnaryOp):
            return self.flatten_unary_op(expr)
        elif isinstance(expr, Call):
            return self.flatten_function_call(expr)
        elif isinstance(expr, Constant):
            return self.flatten_constant(expr)
        elif isinstance(expr, Name):
            return self.flatten_name(expr)
        else:
            raise Exception("Unknown expr type: " + str(expr))

    def flatten_expr_statement(self, expr_statement):
        out = self.flatten_expr(expr_statement.value)
        if out is not None: # if expr_statement.value is not a print statement
            self.statements.append(Expr(value=self.flatten_expr(expr_statement.value)))

    def flatten_assignment(self, assignment):
        value = self.create_tmp_var(self.flatten_expr(assignment.value))
        self.statements.append(Assign(targets=[assignment.targets[0]], value=value))

    def flatten_statement(self, statement):
        if isinstance(statement, Expr):
            self.flatten_expr_statement(statement)
        elif isinstance(statement, Assign):
            self.flatten_assignment(statement)
        else:
            raise Exception("Unknown statement type: " + str(statement))

    def flatten_module(self, module):
        for statement in cp(module.body):
            self.flatten_statement(statement)

        return self.statements

def flattened_list_to_string(flattened_list):
    return "\n".join([dump(x, indent=4) for x in flattened_list])

def flattened_list_to_python(flattened_list):
    data = []
    for x in flattened_list:
        fix_missing_locations(x)
        data.append(unparse(x))
    return "\n".join(data)