import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"design\main")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Функции для информации
def show_about():
    messagebox.showinfo("О программе", "Опросник для университета")

def show_help():
    messagebox.showinfo("Помощь", "Для начала опроса нажмите кнопку 'Начать опрос'")

# Функции для открытия файлов
def open_open_file():
    window.destroy()
    subprocess.run(["python", "ans/open_ans.py"])

def open_close_file():
    window.destroy()
    subprocess.run(["python", "ans/close_ans.py"])

def open_pazl_file():
    window.destroy()
    subprocess.run(["python", "ans/pazl_ans.py"])

def open_log_file():
    window.destroy()
    subprocess.run(["python", "ans/log.py"])

window = Tk()
window.geometry("1024x600")
window.configure(bg="#121212")

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

# Кнопки и текст
button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(image=button_image_1, borderwidth=0, highlightthickness=0, command=open_log_file, relief="flat")
button_1.place(x=329.0, y=406.0, width=365.0, height=50.0)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(image=button_image_2, borderwidth=0, highlightthickness=0, command=open_pazl_file, relief="flat")
button_2.place(x=329.0, y=321.0, width=365.0, height=50.0)

button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
button_3 = Button(image=button_image_3, borderwidth=0, highlightthickness=0, command=open_close_file, relief="flat")
button_3.place(x=329.0, y=237.0, width=365.0, height=50.0)

button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
button_4 = Button(image=button_image_4, borderwidth=0, highlightthickness=0, command=open_open_file, relief="flat")
button_4.place(x=329.0, y=153.0, width=365.0, height=50.0)

button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
button_5 = Button(image=button_image_5, borderwidth=0, highlightthickness=0, command=show_help, relief="flat")
button_5.place(x=137.0, y=14.0, width=116.7, height=35.97)

button_image_6 = PhotoImage(file=relative_to_assets("button_6.png"))
button_6 = Button(image=button_image_6, borderwidth=0, highlightthickness=0, command=show_about, relief="flat")
button_6.place(x=10.0, y=14.0, width=116.6, height=35.97)

canvas.create_text(
    231.0, 86.0,
    anchor="nw",
    text="Опросник для университета",
    fill="#E0E0E0",
    font=("AnonymousPro Regular", 40 * -1)
)

window.resizable(False, False)
window.mainloop()
