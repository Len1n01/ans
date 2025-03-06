import tkinter as tk
from tkinter import messagebox
import subprocess

# Основные цвета
BG_COLOR = "#F6D35B"
TEXT_COLOR = "#2c3e50"
BUTTON_COLOR = "#f1c40f"
BUTTON_TEXT = "#000"

# Функция возврата в главное меню
def open_main_menu():
    root.destroy()
    subprocess.run(["python", "main.py"])

# Функция проверки ответов
def check_answers():
    correct_answers = [
        "четкая последовательность действий",  # Вопрос 1
        "бесконечность",  # Вопрос 2
        "рекурсивный",  # Вопрос 3
        "o(log n)",  # Вопрос 4
        "быстрая сортировка"  # Вопрос 5
    ]
    
    user_answers = [entry.get().strip().lower() for entry in entries]
    score = sum(1 for i in range(5) if user_answers[i] == correct_answers[i].lower())
    messagebox.showinfo("Результат", f"Вы набрали {score} из 5 правильных ответов!")

# Создание окна
root = tk.Tk()
root.geometry('1024x600')
root.title("Тест по алгоритмам")
root.configure(bg=BG_COLOR)

# Создание контейнера для выравнивания по левому краю
frame = tk.Frame(root, bg=BG_COLOR)
frame.pack(expand=True, anchor="w", padx=20)

questions = [
    "1. Что такое алгоритм?",
    "2. Каким свойством НЕ обладает алгоритм?",
    "3. Как называется алгоритм, который вызывает сам себя?",
    "4. Какая сложность у алгоритма бинарного поиска?",
    "5. Какой алгоритм сортировки имеет наилучшую среднюю сложность?"
]

entries = []
for i, question in enumerate(questions):
    tk.Label(frame, text=question, bg=BG_COLOR, fg=TEXT_COLOR, font=("Arial", 14, "bold")).pack(anchor="w", pady=5)
    entry = tk.Entry(frame, width=50, font=("Arial", 12))
    entry.pack(pady=2, anchor="w")
    entries.append(entry)

# Контейнер для кнопок
btn_frame = tk.Frame(root, bg=BG_COLOR)
btn_frame.pack(pady=10)

# Кнопки в одной строке
btn_check = tk.Button(btn_frame, text="Проверить", font=('Arial', 16, 'bold'), width=20, height=2, bg=BUTTON_COLOR, fg=BUTTON_TEXT, command=check_answers)
btn_check.grid(row=0, column=0, padx=10)

btn_menu = tk.Button(btn_frame, text="Вернуться на главное меню", font=("Arial", 16, "bold"), width=25, height=2, bg=BUTTON_COLOR, fg=BUTTON_TEXT, command=open_main_menu)
btn_menu.grid(row=0, column=1, padx=10)

root.mainloop()