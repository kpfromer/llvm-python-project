"""
This file demonstrates a trivial function "fpadd" returning the sum of
two floating-point numbers.
"""

from __future__ import print_function
from llvmlite import ir
from ctypes import CFUNCTYPE, c_double
import llvmlite.binding as llvm
from ast import *

def visit_constant(const):
    if isinstance(const, Constant):
        return ir.Constant(ir.IntType(32), const.value)
    else:
        raise Exception("Unknown constant type: " + str(const))
    
def visit_binary_op(op, builder):
    if isinstance(op, BinOp):
        op_type = op.op
        if isinstance(op_type, Add):
            return builder.add(visit_constant(op.left), visit_constant(op.right), name="res")
        else:
            raise Exception("Unknown binary operator: " + str(op_type))
    else:
        raise Exception("Unknown binary op type: " + str(op))

def visit_expr(expr, builder):
    if isinstance(expr, BinOp):
        return visit_binary_op(expr, builder)
    else:
        raise Exception("Unknown expression type: " + str(expr))

def translate(fileAst):
    int_type = ir.IntType(32)
    fnty = ir.FunctionType(int_type, ())

    module = ir.Module(name=__file__)
    func = ir.Function(module, fnty, name="test")

    block = func.append_basic_block(name="entry")
    builder = ir.IRBuilder(block)

    expr = fileAst.body[0].value
    
    result = visit_binary_op(expr, builder)
    # result = builder.add(visit_constant(expr.left), visit_constant(expr.right), name="res")
    # result = builder.add(ir.Constant(int_type, 1), ir.Constant(int_type, 2), name="res")

    builder.ret(result)

    return module
