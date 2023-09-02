import tkinter as tk
from tkinter import scrolledtext
from opcodes import Primitives
from state import InterpretState, CompileState
import oneForth

class OneForthREPL(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("OneForth")
        self.geometry("600x400")

        self.interpret_state = InterpretState()
        self.compile_state = CompileState()

        self.text_widget = scrolledtext.ScrolledText(self, wrap=tk.WORD, bg="black", fg="white")
        self.text_widget.pack(expand=True, fill=tk.BOTH)
        self.text_widget.bind('<Return>', self.process_input)

        # Display initial prompt
        self.text_widget.insert(tk.END, "ok> ")
        self.text_widget.mark_set(tk.INSERT, "end-1c")
        self.text_widget.focus()

    def process_input(self, event):
        # Get the last line (user's input) excluding the "ok> " prompt
        input_line = self.text_widget.get("end-2c linestart+4c", "end-1c")

        # Process the input
        output = self.evaluate_input(input_line.strip())  # strip() to remove any leading/trailing whitespace

        # Insert the output and the new prompt
        self.text_widget.insert(tk.END, "\n" + output + "\nok> ")
        self.text_widget.see(tk.END)
        self.text_widget.mark_set(tk.INSERT, "end-1c")

        return "break"

    def evaluate_input(self, token):
        # Use the evaluate_input function from oneForth.py
        result = oneForth.evaluate_input(token, self.interpret_state, self.compile_state)

        if token == ".dict":
            return result
    
        # Return the result or the top of the data stack
        if self.interpret_state.dataStack:
            return str(self.interpret_state.dataStack[-1])
        return result

if __name__ == "__main__":
    app = OneForthREPL()
    app.mainloop()