import tkinter as tk
import subprocess
from random import shuffle

# Основные цвета
BG_COLOR = "#F6D35B"
TEXT_COLOR = "#2c3e50"
BUTTON_COLOR = "#f1c40f"
BUTTON_TEXT = "#000"

# Вопросы и ответы
questions = [
    "Столица Франции?",
    "2 + 2 = ?",
    "Главный цветок 8 марта?",
    "Какой газ мы вдыхаем?",
    "Сколько континентов на Земле?"
]
answers = ["Париж", "4", "Тюльпан", "Кислород", "7"]

# Перемешиваем ответы
shuffled_answers = answers[:]
shuffle(shuffled_answers)

def reset_game():
    global selected_question
    selected_question = None
    result_label.config(text="")
    for btn in question_buttons.values():
        btn.config(bg=BUTTON_COLOR)
        btn.pack()
    for btn in answer_buttons.values():
        btn.config(bg=BUTTON_COLOR)
        btn.pack()

def open_main_menu():
    root.destroy()
    subprocess.run(["python", "main.py"])

root = tk.Tk()
root.title("Соедини вопросы и ответы")
root.geometry("1024x600")
root.configure(bg=BG_COLOR)

left_frame = tk.Frame(root, bg=BG_COLOR)
left_frame.place(x=50, y=50)
right_frame = tk.Frame(root, bg=BG_COLOR)
right_frame.place(x=600, y=50)

question_buttons = {}
answer_buttons = {}
btn_width, btn_height = 30, 2
selected_question = None

def on_drag_question(text, btn):
    global selected_question
    selected_question = (text, btn)
    btn.config(bg="#ffcccb")

def on_drag_answer(text, btn):
    global selected_question
    if selected_question:
        q_text, q_btn = selected_question
        if answers[questions.index(q_text)] == text:
            q_btn.pack_forget()
            btn.pack_forget()
        else:
            q_btn.config(bg="red")
            btn.config(bg="red")
        selected_question = None

for q in questions:
    btn = tk.Button(left_frame, text=q, font=("Arial", 14, "bold"), width=btn_width, height=btn_height,
                    bg=BUTTON_COLOR, fg=BUTTON_TEXT, relief=tk.RAISED)
    btn.pack(pady=10)
    btn.bind("<Button-1>", lambda e, text=q, b=btn: on_drag_question(text, b))
    question_buttons[q] = btn

for a in shuffled_answers:
    btn = tk.Button(right_frame, text=a, font=("Arial", 14, "bold"), width=btn_width, height=btn_height,
                    bg=BUTTON_COLOR, fg=BUTTON_TEXT, relief=tk.RAISED)
    btn.pack(pady=10)
    btn.bind("<Button-1>", lambda e, text=a, b=btn: on_drag_answer(text, b))
    answer_buttons[a] = btn

bottom_frame = tk.Frame(root, bg=BG_COLOR)
bottom_frame.pack(side=tk.BOTTOM, pady=20)

reset_btn = tk.Button(bottom_frame, text="Сбросить", command=reset_game, font=("Arial", 14, "bold"), width=15, height=2,
                      bg=BUTTON_COLOR, fg=BUTTON_TEXT)
reset_btn.pack(side=tk.LEFT, padx=10)

main_menu_btn = tk.Button(bottom_frame, text="Главное меню", command=open_main_menu, font=("Arial", 12, "bold"), width=15, height=2,
                          bg=BUTTON_COLOR, fg=BUTTON_TEXT)
main_menu_btn.pack(side=tk.LEFT, padx=10)

result_label = tk.Label(root, text="", bg=BG_COLOR, font=("Arial", 12, "bold"))
result_label.pack()

root.mainloop()
