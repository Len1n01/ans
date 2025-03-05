import tkinter as tk
from tkinter import messagebox
import subprocess

# Основные цвета
BG_COLOR = "#F6D35B"
TEXT_COLOR = "#2c3e50"
CORRECT_COLOR = "#2ecc71"
WRONG_COLOR = "#e74c3c"
BUTTON_COLOR = "#f1c40f"
BUTTON_TEXT = "#000"

# Функция для возврата в меню
def open_main_menu():
    root.destroy()
    subprocess.run(["python", "main.py"])

# Список вопросов и ответов
questions = [
    ("Какой из следующих алгоритмов является алгоритмом обучения с учителем?", ["K-Means", "Линейная регрессия", "DBSCAN", "PCA"], 1),
    ("Какой алгоритм чаще всего используется для классификации?", ["Логистическая регрессия", "K-Means", "Градиентный спуск", "PCA"], 0),
    ("Какой из методов используется для уменьшения размерности данных?", ["KNN", "SVM", "PCA", "Random Forest"], 2),
    ("Какой алгоритм относится к методам кластеризации?", ["Decision Tree", "K-Means", "Линейная регрессия", "Градиентный бустинг"], 1),
    ("Какой метод используется для оптимизации нейронных сетей?", ["Градиентный спуск", "K-Means", "Логистическая регрессия", "DBSCAN"], 0)
]

current_question = 0
score = 0
selected = False

# Создание окна
root = tk.Tk()
root.geometry("1024x600")
root.title("Тест по алгоритмам")
root.configure(bg=BG_COLOR)

# Функция отображения вопроса
def show_question():
    global selected
    selected = False
    question_label.config(text=questions[current_question][0])
    
    for i, btn in enumerate(answer_buttons):
        btn.config(text=questions[current_question][1][i], bg=BUTTON_COLOR, state="normal")
    
    next_button.config(state="disabled")

    if current_question == len(questions) - 1:
        next_button.config(text="Вернуться в меню")

# Функция выбора ответа
def choose_answer(index):
    global selected, score
    if selected:
        return
    selected = True
    correct_index = questions[current_question][2]
    
    for i, btn in enumerate(answer_buttons):
        if i == correct_index:
            btn.config(bg=CORRECT_COLOR)
        elif i == index:
            btn.config(bg=WRONG_COLOR)
        btn.config(state="disabled")
    
    if index == correct_index:
        score += 2
    
    next_button.config(state="normal")

# Функция перехода к следующему вопросу
def next_question():
    global current_question
    if current_question < len(questions) - 1:
        current_question += 1
        show_question()
    else:
        messagebox.showinfo("Результат", f"Ваш результат: {score} баллов")
        open_main_menu()

question_label = tk.Label(root, text="", font=("Arial", 18, "bold"), bg=BG_COLOR, fg=TEXT_COLOR, wraplength=900)
question_label.pack(pady=20)

answer_buttons = []
for i in range(4):
    btn = tk.Button(root, text="", font=("Arial", 16), width=40, height=2, bg=BUTTON_COLOR, fg=BUTTON_TEXT,
                    command=lambda i=i: choose_answer(i))
    btn.pack(pady=5)
    answer_buttons.append(btn)

next_button = tk.Button(root, text="Далее", font=("Arial", 14, "bold"), bg="#3498db", fg="white", padx=20, pady=10,
                        command=next_question, state="disabled")
next_button.pack(pady=20)

show_question()
root.mainloop()
