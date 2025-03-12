import tkinter as tk
from tkinter import messagebox, PhotoImage, Canvas, Text
import subprocess
from sentence_transformers import SentenceTransformer, util
from pathlib import Path

# Функция для возврата в меню
def open_main_menu():
    root.destroy()
    subprocess.run(["python", "main.py"])

# Загружаем модель для анализа схожести
model = SentenceTransformer('all-MiniLM-L6-v2')

# Логические вопросы и правильные ответы
questions = [
    ("Что тяжелее: 1 кг железа или 1 кг ваты?", "Они весят одинаково."),
    ("У отца Васи три сына: Витя, Петя и ...?", "Вася."),
    ("Что можно увидеть с закрытыми глазами?", "Сон."),
    ("Сколько месяцев в году имеют 28 дней?", "Все."),
    ("Что больше: полтора литра или 1.5 литра?", "Одинаково."),
    ("Какое число идет после 999?", "1000."),
    ("Какое слово начинается с 'е' и заканчивается на 'o', но содержит только одну букву?", "Конверт."),
    ("Сколько концов у двух палок?", "Четыре."),
    ("Что можно держать, но не потрогать?", "Обещание."),
    ("Какое слово пишется неправильно во всех словарях?", "Неправильно."),
]

num_questions = len(questions)
entries = []
labels = []
results = []
current_page = 0
questions_per_page = 5

def check_answers():
    total_score = 0
    for i in range(questions_per_page):
        idx = current_page * questions_per_page + i
        if idx >= num_questions:
            break
        user_answer = entries[i].get("1.0", tk.END).strip()
        correct_answer = questions[idx][1]
        
        # Анализ схожести ответа
        emb1 = model.encode(user_answer, convert_to_tensor=True)
        emb2 = model.encode(correct_answer, convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(emb1, emb2).item()
        
        # Переводим в проценты
        score_percentage = round(similarity * 100, 2)
        
        # Выставляем баллы
        if score_percentage >= 80:
            score = 3
        elif score_percentage >= 70:
            score = 2
        elif score_percentage >= 55:
            score = 1
        else:
            score = 0
        
        total_score += score
        results[i].config(text=f"Схожесть: {score_percentage}% | Баллы: {score}")
    
    final_result_label.config(text=f"Общий счет: {total_score} из {questions_per_page * 3}")

def switch_page(direction):
    global current_page
    current_page += direction
    if current_page < 0:
        current_page = 0
    elif current_page >= num_questions // questions_per_page:
        current_page = num_questions // questions_per_page - 1
    update_questions()

def update_questions():
    for i in range(questions_per_page):
        idx = current_page * questions_per_page + i
        if idx < num_questions:
            labels[i].config(text=questions[idx][0])
            entries[i].delete("1.0", tk.END)
            results[i].config(text="")
        else:
            labels[i].config(text="")
            entries[i].delete("1.0", tk.END)
            results[i].config(text="")

# Создание окна
root = tk.Tk()
root.geometry('1024x600')
root.configure(bg = "#121212")
root.title("Логическая викторина")

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

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\ans\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

for i in range(questions_per_page):
    label = tk.Label(root, text="", bg="#121212", fg="#FFFFFF", font=("AnonymousPro Bold", 24))
    label.place(x=199, y=13 + i*88)
    labels.append(label)
    
    entry = Text(root, bd=0, bg="#BBBFE0", fg="#000716", highlightthickness=0)
    entry.place(x=199, y=53 + i*88, width=554, height=38)
    entries.append(entry)
    
    result = tk.Label(root, text="", bg="#121212", fg="#FFFFFF", font=("AnonymousPro Bold", 14))
    result.place(x=199, y=93 + i*88)
    results.append(result)

btn_frame = tk.Frame(root, bg="#121212")
btn_frame.place(x=199, y=509)

button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
btn_check = tk.Button(btn_frame, image=button_image_1, borderwidth=0, highlightthickness=0, command=check_answers, relief="flat")
btn_check.grid(row=0, column=0, padx=10)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
btn_prev = tk.Button(btn_frame, image=button_image_2, borderwidth=0, highlightthickness=0, command=lambda: switch_page(-1), relief="flat")
btn_prev.grid(row=0, column=1, padx=10)

button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
btn_next = tk.Button(btn_frame, image=button_image_3, borderwidth=0, highlightthickness=0, command=lambda: switch_page(1), relief="flat")
btn_next.grid(row=0, column=2, padx=10)

btn_menu = tk.Button(root, text="Вернуться на главное меню", width=25, height=2, command=open_main_menu)
btn_menu.place(x=402, y=559)

final_result_label = tk.Label(root, text="", bg="#121212", fg="#FFFFFF", font=("AnonymousPro Bold", 24))
final_result_label.place(x=199, y=559)

update_questions()
root.mainloop()