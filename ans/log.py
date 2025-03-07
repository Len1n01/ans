import tkinter as tk
from tkinter import messagebox
from difflib import SequenceMatcher
import subprocess
import torch
import torch.nn.functional as F

# Основные цвета
BG_COLOR = "#F6D35B"
TEXT_COLOR = "#2c3e50"
BUTTON_COLOR = "#f1c40f"
BUTTON_TEXT = "#000"

# Вопросы и правильные ответы
questions = [
    ("Какое число нужно прибавить к 15, чтобы получить 30?", "15"),
    ("Если у двоих отцов по два сына, сколько всего человек в семье?", "4"),
    ("Два человека играли в шахматы 2 часа. Сколько времени играл каждый?", "2"),
    ("Что тяжелее: 1 кг железа или 1 кг пуха?", "одинаково"),
    ("В комнате 4 угла. В каждом углу сидит кошка. Напротив каждой кошки сидит еще одна. Сколько кошек в комнате?", "4"),
    ("Если одно яйцо варится 4 минуты, сколько времени нужно варить 5 яиц?", "4"),
    ("Человек купил корову за 500 рублей и продал за 600. Потом купил ее снова за 700 и продал за 800. Сколько он заработал?", "200"),
    ("Какое число получится, если перевернуть 9 вверх ногами?", "6"),
    ("Если мама старше сына на 25 лет, то через сколько лет разница в их возрасте будет 30 лет?", "никогда"),
    ("Какое слово всегда звучит неверно?", "неверно"),
    ("Что можно увидеть с закрытыми глазами?", "сон"),
    ("Если 10 человек построились в круг, у каждого по 2 соседа. Сколько всего соседей?", "20"),
    ("Какое слово начинается с трёх букв 'Г', но не является повторением одной буквы?", "ГГГра"),
    ("Чем больше из нее берешь, тем больше она становится. Что это?", "яма"),
    ("У родителей 6 сыновей, у каждого есть сестра. Сколько всего детей в семье?", "7"),
]

current_page = 0
entries = []
user_answers = ["" for _ in questions]

def vectorize_text(text):
    return torch.tensor([ord(c) for c in text], dtype=torch.float32)

def calculate_similarity(answer, correct):
    answer_vector = vectorize_text(answer.lower())
    correct_vector = vectorize_text(correct.lower())
    min_length = min(len(answer_vector), len(correct_vector))
    answer_vector = answer_vector[:min_length]
    correct_vector = correct_vector[:min_length]
    similarity = F.cosine_similarity(answer_vector.unsqueeze(0), correct_vector.unsqueeze(0)).item()
    return similarity * 100

# Функция для возврата в главное меню
def open_main_menu():
    root.destroy()
    subprocess.run(["python", "main.py"])

# Функция для отображения вопросов
def show_questions():
    global entries
    for widget in frame_questions.winfo_children():
        widget.destroy()
    
    entries = []
    start = current_page * 5
    end = start + 5
    for i in range(start, min(end, len(questions))):
        question, _ = questions[i]
        tk.Label(frame_questions, text=question, font=("Arial", 16), bg=BG_COLOR, fg=TEXT_COLOR).pack()
        entry = tk.Entry(frame_questions, font=("Arial", 14))
        entry.pack()
        entry.insert(0, user_answers[i])
        entries.append((entry, i))
    
    update_buttons()

# Функция для обновления кнопок навигации
def update_buttons():
    next_btn.pack_forget()
    prev_btn.pack_forget()
    submit_btn.pack_forget()
    btn_menu.pack_forget()
    
    if current_page < len(questions) // 5 - 1:
        next_btn.pack(pady=10)
    if current_page > 0:
        prev_btn.pack(pady=10)
    if current_page == len(questions) // 5 - 1:
        submit_btn.pack(pady=20)
        btn_menu.pack(pady=10)

# Функция проверки ответов
def check_answers():
    correct_count = 0
    total_score = 0
    total_similarity = 0
    result_details = ""
    
    for i, (_, correct_answer) in enumerate(questions):
        user_answer = user_answers[i].strip()
        similarity = calculate_similarity(user_answer, correct_answer)
        total_similarity += similarity
        result_details += f"Вопрос {i+1}: {similarity:.2f}% правильности\n"
        
        if similarity >= 55:
            total_score += 1
            correct_count += 1
    
    percentage_correct = (total_similarity / len(questions)) if questions else 0
    result_message = f"Правильных ответов: {correct_count}\nНабранные баллы: {total_score}\nСредний процент правильности: {percentage_correct:.2f}%\n\n{result_details}"
    messagebox.showinfo("Результат", result_message)

# Функции для навигации
def next_page():
    global current_page
    save_answers()
    current_page += 1
    show_questions()

def prev_page():
    global current_page
    save_answers()
    current_page -= 1
    show_questions()

def save_answers():
    for entry, index in entries:
        user_answers[index] = entry.get()

# Создание окна
root = tk.Tk()
root.geometry("1024x600")
root.title("Логический опросник")
root.configure(bg=BG_COLOR)

# Заголовок
title_label = tk.Label(root, text="Логический опросник", font=("Arial", 24, "bold"), bg=BG_COLOR, fg=TEXT_COLOR)
title_label.pack(pady=20)

# Фрейм для вопросов
frame_questions = tk.Frame(root, bg=BG_COLOR)
frame_questions.pack(pady=20)

# Кнопки навигации
prev_btn = tk.Button(root, text="Назад", font=("Arial", 16, "bold"), width=15, height=2, bg=BUTTON_COLOR,
                     fg=BUTTON_TEXT, command=prev_page)
next_btn = tk.Button(root, text="Далее", font=("Arial", 16, "bold"), width=15, height=2, bg=BUTTON_COLOR,
                     fg=BUTTON_TEXT, command=next_page)
submit_btn = tk.Button(root, text="Проверить ответы", font=("Arial", 16, "bold"), width=30, height=2,
                       bg=BUTTON_COLOR, fg=BUTTON_TEXT, command=check_answers)
btn_menu = tk.Button(root, text="Вернуться в меню", font=("Arial", 16, "bold"), width=25, height=2,
                     bg=BUTTON_COLOR, fg=BUTTON_TEXT, command=open_main_menu)

# Отображение вопросов
show_questions()

root.mainloop()
