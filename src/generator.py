import llvmlite.binding as llvm
import os
import sys
import subprocess

def replace_triple(ir):
    return ir.replace("target triple = \"unknown-unknown-unknown\"", "target triple = \"{}\"".format(llvm.get_default_triple()))

def generate_ir(module):
    module_string = str(module)
    module_string = replace_triple(module_string)
    return module_string

def generate_binary(module, filename):
    ir_string = generate_ir(module)
    shared_library_path = os.path.join(os.getcwd(), "shared.so")

    with open("{}.ll".format(filename), "w") as f:
        f.write(ir_string)
    
    # generate binary .s
    subprocess.call(["llc", "-filetype=asm", "{}.ll".format(filename), "-o", "{}.s".format(filename)])
    # link .s to shared library (runtime)
    subprocess.call(["gcc", "{}.s".format(filename), shared_library_path, "-o", "{}.bin".format(filename)])
