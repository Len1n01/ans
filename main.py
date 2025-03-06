import tkinter as tk
from tkinter import ttk, messagebox
import subprocess

# Основные цвета
BG_COLOR = "#F6D35B"
TEXT_COLOR = "#2c3e50"
BUTTON_COLOR = "#f1c40f"
BUTTON_TEXT = "#000"

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
    subprocess.run(["python", "ans/log_ans.py"])

# Создание окна
root = tk.Tk()
root.geometry("1024x600")
root.title("Опросник")
root.configure(bg=BG_COLOR)

# Верхняя панель с кнопками "О программе" и "Помощь"
frame_top = tk.Frame(root, bg=BG_COLOR)
frame_top.pack(anchor='nw', pady=10, padx=10)

tk.Button(frame_top, text="О программе", font=("Arial", 14, "bold"), bg=BUTTON_COLOR, fg=BUTTON_TEXT,
          padx=10, pady=5, command=show_about).grid(row=0, column=0, padx=5)

tk.Button(frame_top, text="Помощь", font=("Arial", 14, "bold"), bg=BUTTON_COLOR, fg=BUTTON_TEXT,
          padx=10, pady=5, command=show_help).grid(row=0, column=1, padx=5)

# Заголовок
title_label = tk.Label(root, text="Опросник для университета", font=("Arial", 24, "bold"), bg=BG_COLOR, fg=TEXT_COLOR)
title_label.pack(pady=20)

# Фрейм для кнопок
frame_buttons = tk.Frame(root, bg=BG_COLOR)
frame_buttons.pack(pady=20)

# Создание кнопок для разных типов вопросов
buttons = [
    ("Открытые вопросы", open_open_file),
    ("Закрытые вопросы", open_close_file),
    ("Пазл", open_pazl_file),
    ("Логика", open_log_file)
]

for text, command in buttons:
    tk.Button(frame_buttons, text=text, font=("Arial", 16, "bold"), width=30, height=2,
              bg=BUTTON_COLOR, fg=BUTTON_TEXT, command=command).pack(pady=10)

root.mainloop()