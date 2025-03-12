import tkinter as tk
from tkinter import messagebox, PhotoImage, Canvas, Text
import subprocess
from pathlib import Path

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
    
    user_answers = [entry.get("1.0", "end-1c").strip().lower() for entry in entries]
    score = sum(1 for i in range(5) if user_answers[i] == correct_answers[i].lower())
    messagebox.showinfo("Результат", f"Вы набрали {score} из 5 правильных ответов!")

# Создание окна
root = tk.Tk()
root.geometry('1024x600')
root.title("Тест по алгоритмам")
root.configure(bg = "#121212")

# Создание холста
canvas = Canvas(
    root,
    bg = "#121212",
    height = 600,
    width = 1024,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)
canvas.place(x = 0, y = 0)

# Путь к ресурсам
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"close")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Вопросы
questions = [
    "Что такое алгоритм?",
    "Каким свойством НЕ обладает алгоритм?",
    "Как называется алгоритм, который вызывает сам себя?",
    "Какая сложность у алгоритма бинарного поиска?",
    "Какой алгоритм сортировки имеет наилучшую среднюю сложность?"
]

entries = []
for i, question in enumerate(questions):
    canvas.create_text(
        229.0,
        55.0 + i * 88,
        anchor="nw",
        text=question,
        fill="#FFFFFF",
        font=("AnonymousPro Bold", 24 * -1)
    )
    entry_image = PhotoImage(file=relative_to_assets(f"entry_{i+1}.png"))
    entry_bg = canvas.create_image(
        495.5,
        117.5 + i * 88,
        image=entry_image
    )
    entry = Text(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    entry.place(
        x=229.0,
        y=97.0 + i * 88,
        width=533.0,
        height=39.0
    )
    entries.append(entry)

# Кнопки
button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = tk.Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=open_main_menu,
    relief="flat"
)
button_1.place(
    x=566.0,
    y=509.0,
    width=148.0,
    height=41.0
)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = tk.Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=check_answers,
    relief="flat"
)
button_2.place(
    x=273.0,
    y=509.0,
    width=148.0,
    height=41.0
)

root.resizable(False, False)
root.mainloop()