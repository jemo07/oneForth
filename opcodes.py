from __future__ import annotations
from typing import Dict, Callable
from state import InterpretState, CompileState
from llvmlite import ir

Primitives: Dict[str, Dict[str, Callable]] = {}

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

# LLVM IR generation for the plus opcode
def llvm_plus(state: CompileState) -> None:
    # Assuming a basic function signature and integer type for simplicity
    int_type = ir.IntType(32)
    
    # Try to get the function from the module
    function = state.module.get_global_variable_named('add') if 'add' in state.module.globals else None
    
    # If the function doesn't exist, create it
    if function is None:
        function = ir.Function(state.module, ir.FunctionType(int_type, [int_type, int_type]), name="add")
    
    block = function.append_basic_block(name="entry")
    builder = ir.IRBuilder(block)
    result = builder.add(function.args[0], function.args[1], name="result")
    builder.ret(result)

# LLVM IR generation for the minus opcode
def llvm_minus(state: CompileState) -> None:
    int_type = ir.IntType(32)
    function = ir.Function(state.module, ir.FunctionType(int_type, [int_type, int_type]), name="subtract")
    block = function.append_basic_block(name="entry")
    builder = ir.IRBuilder(block)
    result = builder.sub(function.args[0], function.args[1], name="result")
    builder.ret(result)

# Update the Primitives dictionary to use the LLVM IR generation functions for compilation
Primitives["+"]["compile"] = llvm_plus
Primitives["-"]["compile"] = llvm_minus