import tkinter as tk
from tkinter import ttk, messagebox
import subprocess


# Функции для информации

def show_about():
    messagebox.showinfo("О программе", "Опросник для университета")

def show_help():
    messagebox.showinfo("Помощь", "Для начала опроса нажмите кнопку 'Начать опрос'")

# Функции для открытия файлов

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
    subprocess.run(["python", "ans/log.py"])

# Создание окна
root = tk.Tk()
root.geometry("1024x600")
root.title("Опросник")

# Верхняя панель с кнопками "О программе" и "Помощь"
frame_top = tk.Frame(root)
frame_top.pack(anchor='nw', pady=10, padx=10)

tk.Button(frame_top, text="О программе",
          padx=10, pady=5, command=show_about).grid(row=0, column=0, padx=5)

tk.Button(frame_top, text="Помощь",
          padx=10, pady=5, command=show_help).grid(row=0, column=1, padx=5)

# Заголовок
title_label = tk.Label(root, text="Опросник для университета")
title_label.pack(pady=20)

# Фрейм для кнопок
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=20)

# Создание кнопок для разных типов вопросов
buttons = [
    ("Открытые вопросы", open_open_file),
    ("Закрытые вопросы", open_close_file),
    ("Пазл", open_pazl_file),
    ("Логика", open_log_file)
]

for text, command in buttons:
    tk.Button(frame_buttons, text=text, width=30, height=2,command=command).pack(pady=10)
    
root.mainloop()