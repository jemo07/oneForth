

# OneForth

OneForth is a simple Forth-like interpreter built in Python. It provides a basic REPL interface for executing Forth-like commands and also comes with a GUI interface built using Tkinter.

## Features

- Basic arithmetic operations: `+`, `-`
- Stack operations
- Dictionary view with `.dict` command
- Command history in the REPL
- GUI interface with colored output

## Installation

1. Ensure you have Python 3.x installed.
2. Clone this repository:
   ```
   git clone [repository-url]
   cd OneForth
   ```
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Console-based REPL

Run the `oneForth.py` script:

```
python oneForth.py
```

You'll be greeted with the `ok>` prompt. Start entering your Forth-like commands.

You can print the disctionary entries with the word `.dict` with the following output. 

```
ok> .dict
+: {'compile': <function llvm_plus at 0x7f63ce0feb90>, 'execute': <function plus at 0x7f63ce1204c0>}
-: {'compile': <function llvm_minus at 0x7f63ce0fec20>, 'execute': <function minus at 0x7f63ce0fe5f0>}
.: {'compile': <function primitive.<locals>.<lambda> at 0x7f63ce0fe9e0>, 'execute': <function dot at 0x7f63ce0fe950>}
.S: {'compile': <function primitive.<locals>.<lambda> at 0x7f63ce0feb00>, 'execute': <function dot_s at 0x7f63ce0fea70>}
ok

```

Let's break down the output:

`+: {'compile': <function llvm_plus at 0x7f63ce0feb90>, 'execute': <function plus at 0x7f63ce1204c0>}`
   - This is the entry for the `+` word.
   - `'compile': <function llvm_plus at 0x7f63ce0feb90>` means that when the `+` word is compiled, the `llvm_plus` function is called.
   - `'execute': <function plus at 0x7f63ce1204c0>` means that when the `+` word is executed, the `plus` function is called.

`-: {'compile': <function llvm_minus at 0x7f63ce0fec20>, 'execute': <function minus at 0x7f63ce0fe5f0>}`
   - This is the entry for the `-` word.
   - Similar to the `+` word, this entry specifies the functions to call for compilation (`llvm_minus`) and execution (`minus`).

`.: {'compile': <function primitive.<locals>.<lambda> at 0x7f63ce0fe9e0>, 'execute': <function dot at 0x7f63ce0fe950>}`
   - This is the entry for the `.` word.
   - The `compile` function is a lambda function, which is an anonymous function created by the `primitive` decorator. This lambda function simply appends the word to the `codes` list in the `CompileState`.
   - The `execute` function is the `dot` function, which pops and prints the top of the data stack.

`.S: {'compile': <function primitive.<locals>.<lambda> at 0x7f63ce0feb00>, 'execute': <function dot_s at 0x7f63ce0fea70>}`
   - This is the entry for the `.S` word.
   - Similar to the `.` word, the `compile` function is a lambda function created by the `primitive` decorator.
   - The `execute` function is the `dot_s` function, which prints the entire data stack.

The memory addresses (like `0x7f63ce0feb90`) are just the locations in memory where these functions are stored. They can vary each time you run the program and are not particularly important for understanding the functionality.

### GUI Interface

This is just a WIP, it might stop working at anny time as I focus on getting
the core of the Forth system running. 
Run the `oneForthGUI.py` script:

```
python oneForthGUI.py
```

A window will open with a similar `ok>` prompt. Enter your commands in this window.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
