import random
import string
import tkinter as tk
from tkinter import messagebox

def generate_password():
    length = length_var.get()
    include_uppercase = uppercase_var.get()
    include_lowercase = lowercase_var.get()
    include_digits = digits_var.get()
    include_special = special_var.get()
    specific_symbols = specific_symbols_var.get()

    characters = ''
    password_list = []

    if include_uppercase:
        characters += string.ascii_uppercase
        password_list.append(random.choice(string.ascii_uppercase))

    if include_lowercase:
        characters += string.ascii_lowercase
        password_list.append(random.choice(string.ascii_lowercase))

    if include_digits:
        characters += string.digits
        password_list.append(random.choice(string.digits))

    if include_special:
        characters += string.punctuation
        password_list.append(random.choice(string.punctuation))

    if specific_symbols:
        password_list.extend(specific_symbols)
        characters += specific_symbols

    if not characters:
        messagebox.showerror("Error", "At least one character type must be selected.")
        return

    if length < len(password_list):
        messagebox.showerror("Error", f"Length must be at least {len(password_list)} to include all selected character types.")
        return

    password_list += random.choices(characters, k=length - len(password_list))

    random.shuffle(password_list)

    password = ''.join(password_list[:length])
    result_var.set(password)

def copy_to_clipboard():
    password = result_var.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")

root = tk.Tk()
root.title("Password Generator")
root.geometry("350x400")
root.configure(bg="#2e2e2e")

default_font = ("Arial", 10)
root.option_add("*Font", default_font)

title_label = tk.Label(root, text="Password Generator", font=("Arial", 14, "bold"), fg="#ffffff", bg="#2e2e2e")
title_label.pack(pady=10)

input_frame = tk.Frame(root, bg="#2e2e2e")
input_frame.pack(pady=10)

length_var = tk.IntVar(value=12)
uppercase_var = tk.BooleanVar(value=True)
lowercase_var = tk.BooleanVar(value=True)
digits_var = tk.BooleanVar(value=True)
special_var = tk.BooleanVar(value=True)
specific_symbols_var = tk.StringVar()
result_var = tk.StringVar()

tk.Label(input_frame, text="Password Length:", fg="#ffffff", bg="#2e2e2e").grid(row=0, column=0, sticky="w", padx=5, pady=2)
tk.Entry(input_frame, textvariable=length_var, width=10).grid(row=0, column=1, sticky="e", padx=5, pady=2)

tk.Checkbutton(input_frame, text="Include Uppercase Letters", variable=uppercase_var, fg="#ffffff", bg="#2e2e2e", selectcolor="#3e3e3e").grid(row=1, columnspan=2, sticky="w", padx=5, pady=2)
tk.Checkbutton(input_frame, text="Include Lowercase Letters", variable=lowercase_var, fg="#ffffff", bg="#2e2e2e", selectcolor="#3e3e3e").grid(row=2, columnspan=2, sticky="w", padx=5, pady=2)
tk.Checkbutton(input_frame, text="Include Digits", variable=digits_var, fg="#ffffff", bg="#2e2e2e", selectcolor="#3e3e3e").grid(row=3, columnspan=2, sticky="w", padx=5, pady=2)
tk.Checkbutton(input_frame, text="Include Special Characters", variable=special_var, fg="#ffffff", bg="#2e2e2e", selectcolor="#3e3e3e").grid(row=4, columnspan=2, sticky="w", padx=5, pady=2)

tk.Label(input_frame, text="Specific Symbols:", fg="#ffffff", bg="#2e2e2e").grid(row=5, column=0, sticky="w", padx=5, pady=2)
tk.Entry(input_frame, textvariable=specific_symbols_var, width=10).grid(row=5, column=1, sticky="e", padx=5, pady=2)

button_frame = tk.Frame(root, bg="#2e2e2e")
button_frame.pack(pady=10)

tk.Button(button_frame, text="Generate Password", command=generate_password, bg="#5cb85c", fg="#ffffff", activebackground="#4cae4c").grid(row=0, column=0, padx=10)

tk.Button(button_frame, text="Copy to Clipboard", command=copy_to_clipboard, bg="#5bc0de", fg="#ffffff", activebackground="#46b8da").grid(row=0, column=1, padx=10)

tk.Label(root, text="Generated Password:", fg="#ffffff", bg="#2e2e2e").pack(pady=5)
tk.Entry(root, textvariable=result_var, state='readonly', width=30, justify='center').pack(pady=5)

root.mainloop()
