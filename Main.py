import tkinter as tk
import time
from tkinter.colorchooser import askcolor
from tkinter import font
import configparser

speed_scale = None

def type_text(widget, text, delay):
    for char in text:
        widget.insert(tk.END, char)
        widget.update()
        widget.see(tk.END)
        time.sleep(delay)

def set_background_color():
    color = askcolor()[1]
    text_widget.config(bg=color)

def set_text_color():
    color = askcolor()[1]
    text_widget.config(fg=color)

def set_font():
    selected_indices = font_listbox.curselection()
    if selected_indices:
        font_name = font.families()[int(selected_indices[0])]
        text_widget.config(font=(font_name, 12))

def start_typing():
    text_widget.delete("1.0", tk.END)
    text_to_type = text_entry.get()
    typing_delay = float(speed_scale.get())
    type_text(text_widget, text_to_type, typing_delay)

def save_settings():
    config = configparser.ConfigParser()
    config['Settings'] = {
        'Background Color': text_widget.cget('bg'),
        'Text Color': text_widget.cget('fg'),
        'Font': text_widget.cget('font'),
    }
    with open('settings.ini', 'w') as configfile:
        config.write(configfile)

def load_settings():
    config = configparser.ConfigParser()
    config.read('settings.ini')
    if 'Settings' in config:
        settings = config['Settings']
        text_widget.config(bg=settings['Background Color'])
        text_widget.config(fg=settings['Text Color'])
        text_widget.config(font=settings['Font'])

root = tk.Tk()
root.title("Эффект печатания текста")

window_width = 1000
window_height = 600
root.geometry(f"{window_width}x{window_height}")

root.resizable(width=False, height=False)

frame_left = tk.Frame(root)
frame_left.grid(row=0, column=0, padx=10, pady=10)

frame_right = tk.Frame(root)
frame_right.grid(row=0, column=1, padx=10, pady=10)

text_widget = tk.Text(frame_left, wrap=tk.WORD)
text_widget.pack()

text_label = tk.Label(frame_left, text="Введите текст:")
text_label.pack()

text_entry = tk.Entry(frame_left)
text_entry.pack()

scrollbar = tk.Scrollbar(frame_left, command=text_widget.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_widget.config(yscrollcommand=scrollbar.set)

speed_scale = tk.Scale(frame_left, from_=0.01, to=1.0, resolution=0.01, orient=tk.HORIZONTAL, length=200)
speed_scale.set(0.05)
speed_scale.pack()

start_button = tk.Button(frame_left, text="Начать печать", command=start_typing)
start_button.pack()

background_button = tk.Button(frame_right, text="Настройка фона", command=set_background_color)
background_button.pack()

text_color_button = tk.Button(frame_right, text="Настройка цвета текста", command=set_text_color)
text_color_button.pack()

font_label = tk.Label(frame_right, text="Выберите шрифт:")
font_label.pack()

font_listbox = tk.Listbox(frame_right, selectmode=tk.SINGLE)
for family in font.families():
    font_listbox.insert(tk.END, family)
font_listbox.pack()

font_button = tk.Button(frame_right, text="Применить шрифт", command=set_font)
font_button.pack()

load_button = tk.Button(frame_right, text="Загрузить настройки", command=load_settings)
load_button.pack()

save_button = tk.Button(frame_right, text="Сохранить настройки", command=save_settings)
save_button.pack()

load_settings()

root.mainloop()
