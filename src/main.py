import ast
import sys
from flattener import Flattener, flattened_list_to_string 

import llvmlite.binding as llvm
from translator import translate
from generator import generate_binary
from runner import run

def main():
    with open(sys.argv[1], 'r') as f:
        code = f.read()
        fileAst = ast.parse(code)

    filename = None if len(sys.argv) < 3 else sys.argv[2]

    out = Flattener().flatten_module(fileAst)
    module = translate(out)

    if filename is None:
        # run with llvmlite
        # print(flattened_list_to_string(out))
        # print(module)
        # print(llvm.get_default_triple())
        run(module)
    else:
        # otherwise, generate binary
        generate_binary(module, filename)

if __name__ == "__main__":
    main()
