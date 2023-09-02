import opcodes
from state import InterpretState, CompileState
import llvmlite.binding as llvm

llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

def main():
    interpret_state = InterpretState()
    compile_state = CompileState()

    while True:
        # Read input from the user
        token = input("ok> ").strip()

        # Exit the REPL if the user types 'bye'
        if token == "bye":
            break

        # If the token is a number, push it onto the data stack
        elif token.lstrip('-').isdigit():
            interpret_state.dataStack.append(int(token))
            print(interpret_state.dataStack[-1])

        # If the token is a known word (primitive), execute its behavior
        elif token in opcodes.Primitives:
            # Compile-time behavior
            opcodes.Primitives[token]["compile"](compile_state)
            # Execute-time behavior
            if opcodes.Primitives[token]["execute"]:
                opcodes.Primitives[token]["execute"](interpret_state)
            print(interpret_state.dataStack[-1] if interpret_state.dataStack else "Empty stack")

        # If the user types '.dict', print the dictionary content
        elif token == ".dict":
            for key, value in opcodes.Primitives.items():
                print(f"{key}: {value}")

        else:
            print(f"Unknown token: {token}")
            continue 

        print("ok")

if __name__ == "__main__":
    main()