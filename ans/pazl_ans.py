import tkinter as tk
import subprocess
from random import shuffle
from tkinter import messagebox
from pathlib import Path

# Список вопросов и ответов по этапам
stages = [
    {"questions": ["Столица Франции?", "2 + 2 = ?", "Главный цветок 8 марта?", "Какой газ мы вдыхаем?", "Сколько континентов на Земле?"], "answers": ["Париж", "4", "Тюльпан", "Кислород", "7"]},
    {"questions": ["Столица Германии?", "5 * 3 = ?", "Какой металл ржавеет?", "Какой газ мы выдыхаем?", "Самая длинная река?"], "answers": ["Берлин", "15", "Железо", "Углекислый газ", "Амазонка"]},
    {"questions": ["Столица Италии?", "10 / 2 = ?", "Самый высокий водопад?", "Какая планета самая большая?", "Чему равно 3^2?"], "answers": ["Рим", "5", "Анхель", "Юпитер", "9"]},
    {"questions": ["Столица Испании?", "7 + 8 = ?", "Какой океан самый большой?", "Какой газ самый лёгкий?", "Кто написал 'Гамлет'?"], "answers": ["Мадрид", "15", "Тихий", "Водород", "Шекспир"]},
    {"questions": ["Столица Великобритании?", "Корень из 81?", "Сколько месяцев в году?", "Как называется самая длинная кость человека?", "Кто открыл Америку?"], "answers": ["Лондон", "9", "12", "Бедренная", "Колумб"]},
    {"questions": ["Столица Японии?", "12 * 3 = ?", "Какая самая маленькая планета?", "Самая глубокая точка Земли?", "Первый человек в космосе?"], "answers": ["Токио", "36", "Меркурий", "Марианская впадина", "Гагарин"]}
] * 1  # Умножаем список, чтобы получить 30 вопросов

stage_index = 0
answered_questions = 0
total_correct = 0
total_wrong = 0

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"pazl")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def load_stage():
    global selected_question, question_buttons, answer_buttons, answered_questions
    selected_question = None
    answered_questions = 0
    next_btn.config(state=tk.DISABLED)

    for widget in left_frame.winfo_children():
        widget.destroy()
    for widget in right_frame.winfo_children():
        widget.destroy()

    questions = stages[stage_index]["questions"]
    answers = stages[stage_index]["answers"][:]
    shuffle(answers)

    question_buttons.clear()
    answer_buttons.clear()

    for q in questions:
        btn = tk.Button(left_frame, text=q, width=30, height=2, relief=tk.RAISED,bg="#1A237E", fg="#FFFFFF",font=("AnonymousPro Regular", 12, ""))
        btn.pack(pady=15)
        btn.bind("<Button-1>", lambda e, text=q, b=btn: on_drag_question(text, b))
        question_buttons[q] = btn

    for a in answers:
        btn = tk.Button(right_frame, text=a, width=30, height=2, relief=tk.RAISED,bg="#1A237E", fg="#FFFFFF",font=("AnonymousPro Regular", 12, ""))
        btn.pack(pady=15)
        btn.bind("<Button-1>", lambda e, text=a, b=btn: on_drag_answer(text, b))
        answer_buttons[a] = btn

def check_completion():
    if answered_questions == len(stages[stage_index]["questions"]):
        next_btn.config(state=tk.NORMAL)

def next_stage():
    global stage_index
    if stage_index < len(stages) - 1:
        stage_index += 1
        load_stage()
    else:
        show_final_result()

def show_final_result():
    messagebox.showinfo("Результат", f"Правильных ответов: {total_correct}\nНеправильных ответов: {total_wrong}")

def on_drag_question(text, btn):
    global selected_question
    selected_question = (text, btn)

def on_drag_answer(text, btn):
    global selected_question, answered_questions, total_correct, total_wrong
    if selected_question:
        q_text, q_btn = selected_question
        if stages[stage_index]["answers"][stages[stage_index]["questions"].index(q_text)] == text:
            total_correct += 1
        else:
            total_wrong += 1
        q_btn.pack_forget()
        btn.pack_forget()
        answered_questions += 1
        check_completion()
        selected_question = None

def open_main_menu():
    root.destroy()
    subprocess.run(["python", "main.py"])

root = tk.Tk()
root.title("Соедини вопросы и ответы")
root.geometry("1024x600")
root.resizable(False, False)

canvas = tk.Canvas(
    root,
    bg = "#121212",
    height = 600,
    width = 1024,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)
canvas.place(x = 0, y = 0)

left_frame = tk.Frame(root, bg="#121212")
left_frame.place(x=100, y=50)
right_frame = tk.Frame(root, bg="#121212")
right_frame.place(x=600, y=50)

bottom_frame = tk.Frame(root, bg="#121212")
bottom_frame.pack(side=tk.BOTTOM, pady=100)

next_btn_image = tk.PhotoImage(file=relative_to_assets("button_2.png"))
next_btn = tk.Button(
    bottom_frame,
    image=next_btn_image,
    borderwidth=0,
    highlightthickness=0,
    command=show_final_result,
    relief="flat",
    state=tk.DISABLED
)
next_btn.pack(side=tk.LEFT, padx=10)

main_menu_btn_image = tk.PhotoImage(file=relative_to_assets("button_1.png"))
main_menu_btn = tk.Button(
    bottom_frame,
    image=main_menu_btn_image,
    borderwidth=0,
    highlightthickness=0,
    command=open_main_menu,
    relief="flat"
)
main_menu_btn.pack(side=tk.LEFT, padx=10)

question_buttons = {}
answer_buttons = {}

load_stage()
root.mainloop()