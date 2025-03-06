import tkinter as tk
from random import shuffle

# Вопросы и правильные ответы
questions = [
    "Столица Франции?",
    "2 + 2 = ?",
    "Главный цветок 8 марта?",
    "Какой газ мы вдыхаем?",
    "Сколько континентов на Земле?"
]
answers = [
    "Париж",
    "4",
    "Тюльпан",
    "Кислород",
    "7"
]

# Перемешиваем ответы
shuffled_answers = answers[:]
shuffle(shuffled_answers)

# Функция проверки
connections = {}
def check_answers():
    correct = sum(1 for q, a in connections.items() if answers[questions.index(q)] == a)
    result_label.config(text=f"Правильных ответов: {correct} из {len(questions)}")

# Создаем окно
root = tk.Tk()
root.title("Пазл-викторина")
root.geometry("600x500")

# Холст для рисования пазлов
canvas = tk.Canvas(root, width=600, height=400, bg="white")
canvas.pack()

question_pieces = {}
answer_pieces = {}
selected_piece = None
lines = []

# Функция для перемещения пазлов

def on_drag_start(event):
    global selected_piece
    selected_piece = event.widget
    selected_piece.lift()

def on_drag_motion(event):
    if selected_piece:
        canvas.coords(selected_piece, event.x, event.y)

def on_drag_release(event):
    global selected_piece
    if selected_piece:
        closest = canvas.find_closest(event.x, event.y)[0]
        target = canvas.gettags(closest)
        if "answer" in target:
            q_text = selected_piece.cget("text")
            a_text = canvas.itemcget(closest, "text")
            connections[q_text] = a_text
            x1, y1, x2, y2 = canvas.bbox(selected_piece)
            x3, y3, x4, y4 = canvas.bbox(closest)
            line = canvas.create_line((x1+x2)//2, (y1+y2)//2, (x3+x4)//2, (y3+y4)//2, width=2, fill="black")
            lines.append(line)
        selected_piece = None

# Размещаем пазлы вопросов
for i, q in enumerate(questions):
    piece = canvas.create_rectangle(50, 50 + i * 70, 200, 100 + i * 70, fill="lightblue", tags=("question"))
    text = canvas.create_text(125, 75 + i * 70, text=q, font=("Arial", 10, "bold"), tags=("question"))
    question_pieces[q] = text
    canvas.tag_bind(text, "<Button-1>", on_drag_start)
    canvas.tag_bind(text, "<B1-Motion>", on_drag_motion)
    canvas.tag_bind(text, "<ButtonRelease-1>", on_drag_release)

# Размещаем пазлы ответов
for i, a in enumerate(shuffled_answers):
    piece = canvas.create_rectangle(400, 50 + i * 70, 550, 100 + i * 70, fill="lightgreen", tags=("answer"))
    text = canvas.create_text(475, 75 + i * 70, text=a, font=("Arial", 10, "bold"), tags=("answer"))
    answer_pieces[a] = text
    canvas.tag_bind(text, "<Button-1>", on_drag_start)
    canvas.tag_bind(text, "<B1-Motion>", on_drag_motion)
    canvas.tag_bind(text, "<ButtonRelease-1>", on_drag_release)

# Кнопка проверки
check_btn = tk.Button(root, text="Проверить", command=check_answers)
check_btn.pack(pady=10)

# Результат
result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
