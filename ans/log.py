import tkinter as tk
from tkinter import messagebox
import subprocess
from sentence_transformers import SentenceTransformer, util


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
        user_answer = entries[i].get()
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
            entries[i].delete(0, tk.END)
            results[i].config(text="")
        else:
            labels[i].config(text="")
            entries[i].delete(0, tk.END)
            results[i].config(text="")

# Создание окна
root = tk.Tk()
root.geometry('1024x600')
root.title("Логическая викторина")

frame = tk.Frame(root)
frame.pack(expand=True, anchor="w", padx=20)

for i in range(questions_per_page):
    label = tk.Label(frame, text="")
    label.pack(anchor="w", pady=5)
    labels.append(label)
    
    entry = tk.Entry(frame, width=50,)
    entry.pack(pady=2, anchor="w")
    entries.append(entry)
    
    result = tk.Label(frame, text="")
    result.pack(pady=5)
    results.append(result)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

btn_check = tk.Button(btn_frame, text="Проверить", width=20, height=2, command=check_answers)
btn_check.grid(row=0, column=0, padx=10)

btn_prev = tk.Button(btn_frame, text="Назад", width=10, height=2, command=lambda: switch_page(-1))
btn_prev.grid(row=0, column=1, padx=10)

btn_next = tk.Button(btn_frame, text="Вперед", width=10, height=2, command=lambda: switch_page(1))
btn_next.grid(row=0, column=2, padx=10)

btn_menu = tk.Button(btn_frame, text="Вернуться на главное меню",  width=25, height=2, command=open_main_menu)
btn_menu.grid(row=0, column=1, padx=10)

final_result_label = tk.Label(root, text="")
final_result_label.pack(pady=10)

update_questions()
root.mainloop()
