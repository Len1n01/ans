import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def say_hello():
    messagebox.showinfo("Hello", "Hello World")

root = tk.Tk()
root.geometry("1024x940")
root.title("Hello World")

label = ttk.Label(root, text="Hello World")
label.pack()

button = ttk.Button(root, text="Say Hello", command=say_hello)
button.pack()

root.mainloop()