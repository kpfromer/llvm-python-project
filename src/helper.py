from ast import *

def get_variables(ast):
    if isinstance(ast, Module):
        return set().union(*[get_variables(x) for x in ast.body])
    elif isinstance(ast, Expr):
        return get_variables(ast.value)
    elif isinstance(ast, Call):
        return set().union(*[get_variables(x) for x in ast.args])
    elif isinstance(ast, Name):
        return {ast.id} 
    elif isinstance(ast, Assign):
        return set().union(*[get_variables(x) for x in ast.targets]) | get_variables(ast.value) 
    elif isinstance(ast, BinOp):
        return get_variables(ast.left) | get_variables(ast.right)
    elif isinstance(ast, UnaryOp):
        return get_variables(ast.operand)
    elif isinstance(ast, Constant):
        return set()
    else:
        raise Exception("Unknown ast type: " + str(ast))
    
# def uniquify(ast):
#     pass