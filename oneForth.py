import sys
import readline  # This will use pyreadline on Windows if installed
from opcodes import Primitives
from state import InterpretState, CompileState

def evaluate_input(token, interpret_state, compile_state):
    # Exit the REPL if the user types 'bye'
    if token == "bye":
        sys.exit(0)  # This will close the console-based REPL. For GUI, you might need a different approach.
    # Print the dictionary content if the user types '.dict'
    elif token == ".dict":
        entries = []
        for key, value in Primitives.items():
            entry = f"Word: {key}"
            for sub_key, sub_value in value.items():
                if callable(sub_value):
                    entry += f"\n  {sub_key.capitalize()}: {sub_value.__name__}"
            entries.append(entry)
        return "\n\n".join(entries)
    # If the token is a number, push it onto the data stack
    elif token.lstrip('-').isdigit():
        interpret_state.dataStack.append(int(token))
        return str(interpret_state.dataStack[-1])
    # If the token is a known word (primitive), execute its behavior
    elif token in Primitives:
        # Compile-time behavior
        Primitives[token]["compile"](compile_state)
        # Execute-time behavior
        if Primitives[token]["execute"]:
            Primitives[token]["execute"](interpret_state)
        return str(interpret_state.dataStack[-1] if interpret_state.dataStack else "Empty stack")
    else:
        return f"Unknown token: {token}"


def main():
    interpret_state = InterpretState()
    compile_state = CompileState()
    while True:
        try:
            # Read
            token = input("ok> ")
            # Process the token using evaluate_input
            result = evaluate_input(token, interpret_state, compile_state)
            # Print the result
            print(result)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()