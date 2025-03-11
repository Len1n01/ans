from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, messagebox
import subprocess

# Пути к ресурсам
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r'open')

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

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
correct_answers = 0
wrong_answers = 0
selected = False

# Функция возврата в меню
def open_main_menu():
    window.destroy()
    subprocess.run(["python", "main.py"])

# Функция отображения вопроса
def show_question():
    global selected
    selected = False
    canvas.itemconfig(question_text, text=questions[current_question][0])
    
    for i, btn in enumerate(answer_buttons):
        btn.config(text=questions[current_question][1][i], state="normal", bg="#1A237E", command=lambda i=i: choose_answer(i))
    
    button_next.config(state="disabled")  # Блокируем кнопку "Следующий вопрос"
    
    if current_question == len(questions) - 1:
        button_next.config(text="Завершить", command=show_result)

# Функция выбора ответа
def choose_answer(index):
    global selected, score, correct_answers, wrong_answers
    if selected:
        return
    selected = True
    correct_index = questions[current_question][2]
    
    if index == correct_index:
        score += 2
        correct_answers += 1
        answer_buttons[index].config(bg="#76FF03")  # Зеленый для правильного ответа
    else:
        wrong_answers += 1
        answer_buttons[index].config(bg="#FF0004")  # Красный для ошибки
        answer_buttons[correct_index].config(bg="#76FF03")  # Подсветка правильного ответа
    
    for btn in answer_buttons:
        btn.config(state="disabled")
    
    button_next.config(state="normal")  # Разблокируем кнопку "Следующий вопрос"

# Функция перехода к следующему вопросу
def next_question():
    global current_question
    if current_question < len(questions) - 1:
        current_question += 1
        show_question()
    
# Функция показа итогов теста
def show_result():
    messagebox.showinfo("Результат", f"Правильных ответов: {correct_answers}\nОшибок: {wrong_answers}\nОбщий балл: {score}")
    open_main_menu()

# Создание окна
window = Tk()
window.geometry("1024x600")
window.configure(bg="#121212")
window.resizable(False, False)

canvas = Canvas(
    window,
    bg="#121212",
    height=600,
    width=1024,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

question_text = canvas.create_text(
    130.0, 79.0,
    anchor="nw",
    text="",
    fill="#E0E0E0",
    font=("AnonymousPro Regular", 24 * -1)
)

# Кнопки ответов
answer_buttons = []
button_positions = [153, 237, 321, 406]

for i in range(4):
    btn = Button(
        text="",
        font=("Arial", 14),
        bg="#1A237E",
        fg="#E0E0E0",
        activebackground="#E0E0E0",
        activeforeground="#E0E0E0",
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
        width=40,
        height=2
    )
    btn.place(x=329.0, y=button_positions[i], width=365.0, height=50.0)
    answer_buttons.append(btn)

# Кнопка "Следующий вопрос"
button_next = Button(
    text="Следующий",
    font=("Arial", 14),
    bg="#76FF03",
    fg="#121212",
    activebackground="#E0E0E0",
    activeforeground="#121212",
    borderwidth=0,
    highlightthickness=0,
    command=next_question,
    relief="flat",
    state="disabled"
)
button_next.place(x=546.0, y=499.0, width=148.0, height=41.0)

# Кнопка "Меню"
button_menu = Button(
    text="Меню",
    font=("Arial", 14),
    bg="#76FF03",
    fg="#121212",
    activebackground="#121212",
    activeforeground="#121212",
    borderwidth=0,
    highlightthickness=0,
    command=open_main_menu,
    relief="flat"
)
button_menu.place(x=329.0, y=499.0, width=148.0, height=41.0)

show_question()
window.mainloop()