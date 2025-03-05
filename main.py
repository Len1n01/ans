import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
import subprocess

def show_about():
    tk.messagebox.showinfo("О программе ", "Опросник для университета")
def show_help():
    tk.messagebox.showinfo("Помощь", "Для начала опроса нажмите кнопку 'Начать опрос'")

# функции для открытия файлов
def open_open_file():
    root.destroy()
    subprocess.run(["python", "ans/open_ans.py"])

def open_close_file():
    root.destroy()
    subprocess.run(["python", "ans/close_ans.py"])

def open_pazl_file():
    root.destroy()
    subprocess.run(["python", "ans/pazl_ans.py"])

def open_log_file():
    root.destroy()
    subprocess.run(["python", "ans/log_ans.py"])

root = tk.Tk()
root.geometry("800x600")
root.title("Опросник")
root.resizable(False, False)

# about , help
frame_top = tk.Frame(root)
frame_top.pack(anchor='nw', pady=10)

btn_about = tk.Button(frame_top, text="О программе", command=show_about)
btn_about.grid(row=0, column=0, padx=5)

btn_help = tk.Button(frame_top, text="Помощь", command=show_help)
btn_help.grid(row=0, column=1, padx=5)

# загаловок
title_label = ttk.Label(root, text="Опросник для университета", font=("Arial", 20, "bold"))
title_label.pack(pady=20)

# создание фрейма для кнопок
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=20)

# кнопка начать опрос
btn_open = tk.Button(frame_buttons, text="Откр вопрос", command=open_open_file, font=("Arial", 14, "bold"), padx=20, pady=5, bd=2, width=20)
btn_open.pack(pady=10)

btn_close = tk.Button(frame_buttons, text="Закры вопрос", command=open_close_file, font=("Arial", 14, "bold"), padx=20, pady=5, bd=2, width=20)
btn_close.pack(pady=10)

btn_pazl = tk.Button(frame_buttons, text="Пазл", command=open_pazl_file, font=("Arial", 14, "bold"), padx=20, pady=5, bd=2, width=20)
btn_pazl.pack(pady=10)

btn_log = tk.Button(frame_buttons, text="Логика", command=open_log_file, font=("Arial", 14, "bold"), padx=20, pady=5, bd=2, width=20)
btn_log.pack(pady=10)

root.mainloop()