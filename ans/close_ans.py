import tkinter as tk
from tkinter import messagebox

# Основные цвета
BG_COLOR = "#F6D35B"
TEXT_COLOR = "#2c3e50"
BUTTON_COLOR = "#f1c40f"
BUTTON_TEXT = "#000"
CORRECT_COLOR = "#2ecc71"
WRONG_COLOR = "#e74c3c"

def check_answers():
    correct_answers = [
        "четкая последовательность действий",  # Вопрос 1
        "бесконечность",  # Вопрос 2
        "рекурсивный",  # Вопрос 3
        "O(log n)",  # Вопрос 4
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

questions = [
    "1. Что такое алгоритм?",
    "2. Каким свойством НЕ обладает алгоритм?",
    "3. Как называется алгоритм, который вызывает сам себя?",
    "4. Какая сложность у алгоритма бинарного поиска?",
    "5. Какой алгоритм сортировки имеет наилучшую среднюю сложность?"
]

entries = []
for i, question in enumerate(questions):
    tk.Label(root, text=question, bg=BG_COLOR, fg=TEXT_COLOR, font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=5)
    entry = tk.Entry(root, width=50, font=("Arial", 12))
    entry.pack(padx=10, pady=2)
    entries.append(entry)

# Кнопка проверки ответов
btn = tk.Button(root, text="Проверить", font=('Arial', 16, 'bold'), width=40, height=2, bg=BUTTON_COLOR, fg=BUTTON_TEXT, command=check_answers)
btn.pack(pady=20)

root.mainloop()