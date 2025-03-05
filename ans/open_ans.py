from tkinter import ttk
from tkinter import *
import tkinter as tk
import subprocess

def open_open_file():
    root.destroy()
    subprocess.run(["python", "main.py"])

def on_mouse_wheel(event):
    canvas.yview_scroll(-1 * (event.delta // 120), "units")

def create_question(root, question, answers, row_start):
    """Функция для создания вопроса с вариантами ответа."""
    label = tk.Label(root, text=question, font=("Arial", 12, "bold"))
    label.grid(row=row_start, column=0, columnspan=2, sticky="w", padx=10, pady=5)

    selected_option = tk.IntVar(value=-1)
    checkbuttons = []

    for i, answer in enumerate(answers):
        chk_btn = tk.Checkbutton(root, text=answer, variable=selected_option, onvalue=i, offvalue=-1, anchor='w')
        chk_btn.grid(row=row_start + i + 1, column=0, columnspan=2, sticky="w", padx=30)
        checkbuttons.append(chk_btn)

    return selected_option, checkbuttons

def check_answers():
    correct_answers = [1, 0, 2, 1, 0]  # Индексы правильных ответов
    score = 0
    for i, (selected, checkbuttons) in enumerate(zip(selected_answers, checkbuttons_list)):
        if selected.get() == correct_answers[i]:
            score += 2
        
        # Деактивируем чекбоксы после ответа
        for btn in checkbuttons:
            btn.config(state=DISABLED)
    
    result_label.config(text=f"Ваш результат: {score} баллов")

root = tk.Tk()
root.geometry("1024x600")
root.title("Тест по алгоритмам")

canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="n", width=1024)
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

frame = tk.Frame(scrollable_frame)
frame.pack(anchor="n", pady=10)

questions = [
    ("Какой из следующих алгоритмов является алгоритмом обучения с учителем?", ["K-Means", "Линейная регрессия", "DBSCAN", "PCA", "Генетический алгоритм"]),
    ("Какой алгоритм чаще всего используется для классификации?", ["Логистическая регрессия", "K-Means", "Градиентный спуск", "PCA", "A*"]),
    ("Какой из методов используется для уменьшения размерности данных?", ["KNN", "SVM", "PCA", "Random Forest", "Градиентный бустинг"]),
    ("Какой алгоритм относится к методам кластеризации?", ["Decision Tree", "K-Means", "Линейная регрессия", "Градиентный бустинг", "Байесовский классификатор"]),
    ("Какой метод используется для оптимизации нейронных сетей?", ["Градиентный спуск", "K-Means", "Логистическая регрессия", "DBSCAN", "Гистограмма"])
]

selected_answers = []
checkbuttons_list = []
row = 0
for question, answers in questions:
    selected_option, checkbuttons = create_question(frame, question, answers, row)
    selected_answers.append(selected_option)
    checkbuttons_list.append(checkbuttons)
    row += len(answers) + 2

buttons_frame = tk.Frame(frame)
buttons_frame.grid(row=row, column=0, columnspan=2, pady=10)

check_button = tk.Button(buttons_frame, text="Проверить ответы", command=check_answers, font=("Arial", 12))
check_button.pack(side="left", padx=5)

btn = tk.Button(buttons_frame, text="Возврат в меню", command=open_open_file, font=("Arial", 12))
btn.pack(side="left", padx=5)

result_label = tk.Label(frame, text="", font=("Arial", 12, "bold"))
result_label.grid(row=row + 1, column=0, columnspan=2, pady=10)

canvas.bind_all("<MouseWheel>", on_mouse_wheel)

root.mainloop()
