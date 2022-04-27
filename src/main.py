import ast
import sys

from translator import translate
from runner import run


def main():
    """
    Main function.
    """
    with open(sys.argv[1], 'r') as f:
        code = f.read()
        fileAst = ast.parse(code)

    print(ast.dump(fileAst))

    module = translate(fileAst)
    print(module)
    run(module)

if __name__ == "__main__":
    main()
