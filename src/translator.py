"""
This file demonstrates a trivial function "fpadd" returning the sum of
two floating-point numbers.
"""

from __future__ import print_function
from llvmlite import ir
from ctypes import CFUNCTYPE, c_double
import llvmlite.binding as llvm
from ast import *

class Translator:
    def __init__(self) -> None:
        self.var_count = 0
        self.print_fn = None
        self.input_fn = None
        # TODO:
        self.mappings = dict() # variable -> latest instruction
    
    def get_tmp_var(self):
        var = "tmp_" + str(self.var_count)
        self.var_count += 1
        return var

    def translate(self, ast_body):
        mod = ir.Module(name="test")

        print_fn_type = ir.FunctionType(ir.VoidType(), [ir.IntType(32)])
        self.print_fn = ir.Function(mod, print_fn_type, name="print")

        input_fn_type = ir.FunctionType(ir.IntType(32), [])
        self.input_fn = ir.Function(mod, input_fn_type, name="input")

        func_type = ir.FunctionType(ir.IntType(32), ())
        func = ir.Function(mod, func_type, name="test")
        block = func.append_basic_block(name="entry")
        builder = ir.IRBuilder(block)
        for statement in ast_body:
            self.visit_statement(statement, builder)

        builder.ret(ir.Constant(ir.IntType(32), 0))

        return mod

    def visit_constant(self, const):
        if isinstance(const, Constant):
            return ir.Constant(ir.IntType(32), const.value)
        else:
            raise Exception("Unknown constant type: " + str(const))
    
    def visit_name(self, name):
        if isinstance(name, Name):
            return self.mappings[name.id]
        else:
            raise Exception("Unknown name type: " + str(name))
    
    def visit_leaf(self, leaf):
        if isinstance(leaf, Constant):
            return self.visit_constant(leaf)
        elif isinstance(leaf, Name):
            return self.visit_name(leaf)
        else:
            raise Exception("Unknown leaf type: " + str(leaf))
        
    def visit_binary_op(self, op, builder):
        if isinstance(op, BinOp):
            op_type = op.op
            if isinstance(op_type, Add):
                return builder.add(self.visit_leaf(op.left), self.visit_leaf(op.right), name=self.get_tmp_var())
            else:
                raise Exception("Unknown binary operator: " + str(op_type))
        else:
            raise Exception("Unknown binary op type: " + str(op))

    def visit_unary_op(self, op, builder):
        if isinstance(op, UnaryOp):
            op_type = op.op
            if isinstance(op_type, UAdd):
                return self.visit_leaf(op.operand)
            elif isinstance(op_type, USub):
                print("Unary minus")
                print(dump(op))
                return builder.sub(ir.Constant(ir.IntType(32), 0), self.visit_leaf(op.operand), name=self.get_tmp_var())
            else:
                raise Exception("Unknown unary operator: " + str(op_type))
        else:
            raise Exception("Unknown unary operator: " + str(op_type))

    def visit_expr(self, expr, builder):
        if isinstance(expr, (Constant, Name)):
            return self.visit_leaf(expr)
        elif isinstance(expr, BinOp):
            return self.visit_binary_op(expr, builder)
        elif isinstance(expr, UnaryOp):
            return self.visit_unary_op(expr, builder)
        elif isinstance(expr, Call):
            return self.visit_function_call(expr, builder)
        else:
            raise Exception("Unknown expr type: " + str(expr))
    
    def visit_function_call(self, call, builder: ir.IRBuilder):
        if isinstance(call, Call):
            if isinstance(call.func, Name):
                if call.func.id == "print":
                    raise Exception("print() is not supported from this function")
                    # return builder.call(self.print_fn, [self.visit_constant(call.args[0])])
                elif call.func.id == "input":
                    return builder.call(self.input_fn, [], name=self.get_tmp_var())
                else:
                    raise Exception("Unknown function call: " + str(call.func.id))
            else:
                raise Exception("Unknown function call: " + str(call.func))
        else:
            raise Exception("Unknown function call: " + str(call))
    
    def visit_assign_statement(self, assign, builder):
        if isinstance(assign, Assign):
            if isinstance(assign.targets[0], Name):
                var = assign.targets[0].id

                value = self.visit_expr(assign.value, builder) 
                assign = builder.add(ir.Constant(ir.IntType(32), 0), value, name=var)
                self.mappings[var] = assign
            else:
                raise Exception("Unknown assign target type: " + str(assign.targets[0]))
        else:
            raise Exception("Unknown assign statement type: " + str(assign))

    def visit_print_statement(self, print_statement, builder):
        if isinstance(print_statement, Call):
            assert len(print_statement.args) == 1, "Print statement should have exactly one argument"
            builder.call(self.print_fn, [self.visit_expr(print_statement.args[0], builder)])
        else:
            raise Exception("Unknown print statement type: " + str(print_statement))

    def visit_statement(self, statement, builder):
        if isinstance(statement, Assign):
            self.visit_assign_statement(statement, builder)
        # print statement
        elif isinstance(statement, Call):
            self.visit_print_statement(statement, builder)
        else:
            raise Exception("Unknown statement type: " + str(statement))

def translate(fileAst: Module):
    return Translator().translate(fileAst)
