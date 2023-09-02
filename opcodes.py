from __future__ import annotations
from typing import Dict, Callable
from state import InterpretState, CompileState
from llvmlite import ir, binding as llvm
from ctypes import CFUNCTYPE, c_int32

Primitives: Dict[str, Dict[str, Callable]] = {}

# Initialize LLVM
llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

# Create a target machine for JIT
target = llvm.Target.from_default_triple()
target_machine = target.create_target_machine()
backend = llvm.PyGCLoweringBackend(target_machine)

def primitive(func) -> None:
    docstring = func.__doc__
    specialCompile: bool = docstring.find(" | (Function Implements Special Compile-Time Behavior)") != -1
    word = docstring[docstring.find("Word: ") + 6:].split()[0].strip()
    funcs = Primitives.get(word, {"compile": None, "execute": None})
    if specialCompile:
        funcs["compile"] = func
    else:
        defaultCompile: Callable[[CompileState], None] = lambda state: state.codes.append(word)
        funcs["compile"] = defaultCompile
        funcs["execute"] = func
    Primitives[word] = funcs

@primitive
def plus(state: InterpretState) -> None:
    """Word: +"""
    a, b = state.dataStack.pop(), state.dataStack.pop()
    state.dataStack.append(a + b)
    state.pos += 1

@primitive
def minus(state: InterpretState) -> None:
    """Word: -"""
    a, b = state.dataStack.pop(), state.dataStack.pop()
    state.dataStack.append(b - a)
    state.pos += 1

@primitive
def dot(state: InterpretState) -> None:
    """Word: ."""
    if state.dataStack:
        print(state.dataStack.pop())

@primitive
def dot_s(state: InterpretState) -> None:
    """Word: .S"""
    print("<top of stack>", end=" ")
    for item in reversed(state.dataStack):
        print(item, end=" ")
    print("<bottom of stack>")

# LLVM IR generation and execution for the plus opcode
def llvm_plus(state: CompileState) -> None:
    int_type = ir.IntType(32)
    function = state.module.get_global_variable_named('add') if 'add' in state.module.globals else None
    if function is None:
        function = ir.Function(state.module, ir.FunctionType(int_type, [int_type, int_type]), name="add")
    block = function.append_basic_block(name="entry")
    builder = ir.IRBuilder(block)
    result = builder.add(function.args[0], function.args[1], name="result")
    builder.ret(result)

    # Compile and execute the LLVM IR
    llvm_module = llvm.parse_assembly(str(state.module))
    llvm_module.verify()
    engine = llvm.create_mcjit_compiler(llvm_module, target_machine)
    add_func_ptr = engine.get_function_address("add")
    cfunc_type = CFUNCTYPE(c_int32, c_int32, c_int32)
    add_func = cfunc_type(add_func_ptr)
    a, b = state.dataStack.pop(), state.dataStack.pop()
    result_value = add_func(a, b)
    state.dataStack.append(result_value)

# LLVM IR generation and execution for the minus opcode
def llvm_minus(state: CompileState) -> None:
    int_type = ir.IntType(32)
    function = state.module.get_global_variable_named('subtract') if 'subtract' in state.module.globals else None
    if function is None:
        function = ir.Function(state.module, ir.FunctionType(int_type, [int_type, int_type]), name="subtract")
    block = function.append_basic_block(name="entry")
    builder = ir.IRBuilder(block)
    result = builder.sub(function.args[0], function.args[1], name="result")
    builder.ret(result)

    # Compile and execute the LLVM IR
    llvm_module = llvm.parse_assembly(str(state.module))
    llvm_module.verify()
    engine = llvm.create_mcjit_compiler(llvm_module, target_machine)
    subtract_func_ptr = engine.get_function_address("subtract")
    cfunc_type = CFUNCTYPE(c_int32, c_int32, c_int32)
    subtract_func = cfunc_type(subtract_func_ptr)
    a, b = state.dataStack.pop(), state.dataStack.pop()
    result_value = subtract_func(a, b)
    state.dataStack.append(result_value)

# Update the Primitives dictionary to use the LLVM IR generation functions for compilation
Primitives["+"]["compile"] = llvm_plus
Primitives["-"]["compile"] = llvm_minus