from tkinter import ttk
from tkinter import *
import tkinter as tk

def on_mouse_wheel(event):
    canvas.yview_scroll(-1 * (event.delta // 120), "units") 

def create_question(root, question, answers, row_start):
    """Функция для создания вопроса с вариантами ответа."""
    label = tk.Label(root, text=question, font=("Arial", 12, "bold"))
    label.grid(row=row_start, column=0, columnspan=2, sticky="w", padx=10, pady=5)

    selected_option = tk.IntVar(value=-1)  # Общая переменная для чекбоксов

    for i, answer in enumerate(answers):
        chk_btn = tk.Checkbutton(root, text=answer, variable=selected_option, onvalue=i, offvalue=-1, anchor='w')
        chk_btn.grid(row=row_start + i + 1, column=0, columnspan=2, sticky="w", padx=30)

    return selected_option  # Для обработки ответов

root = tk.Tk()
root.geometry("1024x600")  # Уменьшил высоту для проверки прокрутки
root.title("Тест по алгоритмам")
# Создаем Canvas и Scrollbar
canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

# Связываем прокрутку с Canvas
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

# Размещаем содержимое внутри Canvas
canvas.create_window((0, 0), window=scrollable_frame, anchor="n", width=1024)

canvas.configure(yscrollcommand=scrollbar.set)

# Размещаем прокрутку и холст
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Центрируем содержимое внутри scrollable_frame
frame = tk.Frame(scrollable_frame)
frame.pack(anchor="n", pady=10)

# Список вопросов и ответов
questions = [
    ("Какой из следующих алгоритмов является алгоритмом обучения с учителем?",
     ["K-Means", "Линейная регрессия", "DBSCAN", "PCA", "Генетический алгоритм"]),

    ("Какой алгоритм чаще всего используется для классификации?",
     ["Логистическая регрессия", "K-Means", "Градиентный спуск", "PCA", "A*"]),

    ("Какой из методов используется для уменьшения размерности данных?",
     ["KNN", "SVM", "PCA", "Random Forest", "Градиентный бустинг"]),

    ("Какой алгоритм относится к методам кластеризации?",
     ["Decision Tree", "K-Means", "Линейная регрессия", "Градиентный бустинг", "Байесовский классификатор"]),

    ("Какой метод используется для оптимизации нейронных сетей?",
     ["Градиентный спуск", "K-Means", "Логистическая регрессия", "DBSCAN", "Гистограмма"])
]

selected_answers = []
row = 0  # Начальная строка
for question, answers in questions:
    selected_answers.append(create_question(frame, question, answers, row))
    row += len(answers) + 2  # Увеличиваем номер строки для следующего вопроса
    
canvas.bind_all("<MouseWheel>", on_mouse_wheel)

root.mainloop()
