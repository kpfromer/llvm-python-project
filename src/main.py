import ast
import sys
from helper import get_variables
from flattener import Flattener, flattened_list_to_string, flattened_list_to_python


import llvmlite.binding as llvm
from translator import translate
from runner import run

'''Steps to get to llvm

- parse the file into ast 
- translate the ast into llvm IR
    - must do flattening of the ast
    - vistor pattern
    - returns llvm IR modiule
- run the llvm IR module with llvm lite
    - con

'''
def main():
    """
    Main function.
    """
    with open(sys.argv[1], 'r') as f:
        code = f.read()
        fileAst = ast.parse(code)
        

    # print(ast.dump(fileAst, indent=4))

    # print(get_variables(fileAst))
    out = Flattener().flatten_module(fileAst)

    print(flattened_list_to_string(out))

    module = translate(out)
    print(module)
    print(llvm.get_default_triple())
    run(module)

if __name__ == "__main__":
    main()
