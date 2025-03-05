import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *

def show_about():
    tk.messagebox.showinfo("О программе ", "Опросник для университета")
def show_help():
    tk.messagebox.showinfo("Помощь", "Для начала опроса нажмите кнопку 'Начать опрос'")

root = tk.Tk()
root.geometry("1024x940")
root.title("Опросник")
root.resizable(False, False)

# about , help
frame_top = tk.Frame(root)
frame_top.pack(anchor='nw')

btn_about = tk.Button(frame_top, text="О программе", command=show_about)
btn_about.grid(row=0, column=0)

btn_help = tk.Button(frame_top, text="Помощь", command=show_help)
btn_help.grid(row=0, column=1)

# загаловок
title_label = ttk.Label(root, text="Опросник для университета", font=("Arial", 20, "bold"))
title_label.pack(pady=10)

# создание фрейма для кнопок
frame_buttons = tk.Frame(root)
frame_buttons.pack(padx=10, pady=10)
# кнопка начать опрос
btn_open = tk.Button(frame_buttons, text="Откр вопрос", font=("Arial", 14, "bold"), padx=20, pady=5, bd=2, width=20)
btn_open.pack(pady=20, padx=10)

btn_close = tk.Button(frame_buttons, text="Закры вопрос", font=("Arial", 14, "bold"), padx=20, pady=5, bd=2, width=20)
btn_close.pack(pady=20, padx=10)

btn_pazl = tk.Button(frame_buttons, text="Пазл", font=("Arial", 14, "bold"), padx=20, pady=5, bd=2, width=20)
btn_pazl.pack(pady=20, padx=10)

btn_log = tk.Button(frame_buttons, text="Логика", font=("Arial", 14, "bold"), padx=20, pady=5, bd=2, width=20)
btn_log.pack(pady=20, padx=10)

btn_log = tk.Button(frame_buttons, text="Логика", font=("Arial", 14, "bold"), padx=20, pady=5, bd=2, width=20)
btn_log.pack(pady=20, padx=10)
root.mainloop()