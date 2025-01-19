import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import json

# Глобальные переменные для отслеживания состояния модификаторов
ctrl_pressed = False
shift_pressed = False
alt_pressed = False
win_pressed = False

# Функция для добавления нового сочетания
def add_combination():
    name = name_entry.get()
    keys = keys_entry.get()
    color = color_combobox.get()  # Получить выбранный цвет

    if not name or not keys or not color:
        messagebox.showerror("Ошибка", "Заполните все поля.")
        return

    try:
        with open("combinations.json", "r") as file:
            combinations = json.load(file)
    except FileNotFoundError:
        combinations = []

    combinations.append({"name": name, "keys": keys, "color": color})

    with open("combinations.json", "w") as file:
        json.dump(combinations, file)

    messagebox.showinfo("Успех", "Сочетание добавлено!")
    name_entry.delete(0, tk.END)
    keys_entry.delete(0, tk.END)
    color_combobox.set("")  # Сброс выбора цвета
    update_combinations_list()




# Функция для обновления списка сочетаний
def update_combinations_list():
    try:
        with open("combinations.json", "r") as file:
            combinations = json.load(file)
    except FileNotFoundError:
        combinations = []

    # Очищаем текущий список
    for widget in combinations_frame.winfo_children():
        widget.destroy()

    # Добавляем каждое сочетание с кнопками
    for index, combination in enumerate(combinations):
        frame = tk.Frame(combinations_frame, bg="#424242")
        frame.pack(fill=tk.X, pady=2, padx=5)

        label = tk.Label(
            frame,
            text=f"{combination['name']} ({combination['keys']})",
            font=("Arial", 12),
            bg="#424242",
            fg="#e0e0e0"
        )
        label.pack(side=tk.LEFT, padx=5)

        # Кнопка редактирования с иконкой
        edit_button = ttk.Button(
            frame,
            image=edit_icon,
            command=lambda idx=index: edit_combination(idx),
            style="Rounded.TButton"
        )
        edit_button.pack(side=tk.RIGHT, padx=5)

        # Кнопка удаления с иконкой
        delete_button = ttk.Button(
            frame,
            image=delete_icon,
            command=lambda idx=index: delete_combination(idx),
            style="Rounded.TButton"
        )
        delete_button.pack(side=tk.RIGHT, padx=5)

    # Обновляем область прокрутки
    combinations_canvas.configure(scrollregion=combinations_canvas.bbox("all"))

# Функция для удаления сочетания
def delete_combination(index):
    try:
        with open("combinations.json", "r") as file:
            combinations = json.load(file)
    except FileNotFoundError:
        combinations = []

    if 0 <= index < len(combinations):
        del combinations[index]

        with open("combinations.json", "w") as file:
            json.dump(combinations, file)

        messagebox.showinfo("Успех", "Сочетание успешно удалено!")
        update_combinations_list()

# Функция для редактирования сочетания
def edit_combination(index):
    try:
        with open("combinations.json", "r") as file:
            combinations = json.load(file)
    except FileNotFoundError:
        combinations = []

    if 0 <= index < len(combinations):
        # Заполняем поля ввода данными выбранного сочетания
        name_entry.delete(0, tk.END)
        name_entry.insert(0, combinations[index]["name"])
        keys_entry.delete(0, tk.END)
        keys_entry.insert(0, combinations[index]["keys"])

        # Удаляем старое сочетание
        del combinations[index]

        # Сохраняем обновленный список
        with open("combinations.json", "w") as file:
            json.dump(combinations, file)

        update_combinations_list()

# Функция для обработки нажатия клавиш
def on_key_press(event):
    global ctrl_pressed, shift_pressed, alt_pressed, win_pressed

    # Определяем, какие модификаторы нажаты
    if event.keysym.lower() == "control_l":
        ctrl_pressed = True
    if event.keysym.lower() == "shift_l":
        shift_pressed = True
    if event.keysym.lower() == "alt_l":
        alt_pressed = True
    if event.keysym.lower() == "win_l":
        win_pressed = True

    # Собираем список нажатых клавиш
    keys = []
    if ctrl_pressed:
        keys.append("ctrl")
    if shift_pressed:
        keys.append("shift")
    if alt_pressed:
        keys.append("alt")
    if win_pressed:
        keys.append("win")

    # Добавляем основную клавишу (если это не модификатор)
    if event.keysym.lower() not in ["control_l", "shift_l", "alt_l", "win_l"]:
        keys.append(event.keysym.lower())

    # Обновляем поле ввода
    keys_entry.delete(0, tk.END)
    keys_entry.insert(0, "+".join(keys))

# Функция для обработки отпускания клавиш
def on_key_release(event):
    global ctrl_pressed, shift_pressed, alt_pressed, win_pressed

    # Сбрасываем состояние модификаторов
    if event.keysym.lower() == "control_l":
        ctrl_pressed = False
    if event.keysym.lower() == "shift_l":
        shift_pressed = False
    if event.keysym.lower() == "alt_l":
        alt_pressed = False
    if event.keysym.lower() == "win_l":
        win_pressed = False

# Создаем главное окно
root = tk.Tk()
root.title("Менеджер сочетаний клавиш")
root.geometry("400x500")
root.configure(bg="#424242")  # Светлый фон


# Загружаем иконки
edit_icon = ImageTk.PhotoImage(Image.open("edit_icon.png").resize((20, 20)))
delete_icon = ImageTk.PhotoImage(Image.open("delete_icon.png").resize((20, 20)))

# Стили для кнопок
style = ttk.Style()
style.configure("Rounded.TButton", borderwidth=0, relief="flat", background="#424242", foreground="#333333", font=("Arial", 10), padding=5, bordercolor="#424242", focuscolor="#424242", lightcolor="#424242", darkcolor="#FBC9C9", borderradius=30)
style.map("Rounded.TButton", background=[("active", "#424242")])

# Поле для ввода названия
tk.Label(
    root,
    text="Название сочетания:",
    font=("Arial", 12),
    bg="#424242",
    fg="#e0e0e0", 
).pack(pady=5)

name_entry = tk.Entry(
    root,
    font=("Arial", 12),
    bg="#424242",
    fg="#e0e0e0",
    insertbackground="#333333",
    relief="flat",
    highlightthickness=1,
    highlightbackground="#6c757d"
)
name_entry.pack(pady=5)

# Поле для ввода сочетания клавиш
tk.Label(
    root,
    text="Комбинация клавиш:",
    font=("Arial", 12),
    fg="#f0f0f0",
    bg="#424242"
).pack(pady=5)

keys_entry = tk.Entry(
    root,
    font=("Arial", 12),
    fg="#ffffff",
    bg="#424242",
    insertbackground="#333333",
    relief="flat",
    highlightthickness=1,
    highlightbackground="#6c757d"
)
keys_entry.pack(pady=5)
# Добавляем выпадающий список для выбора цвета
tk.Label(root, text="Цвет:", font=("Arial", 12), bg="#424242", fg="#f0f0f0").pack(pady=5)
color_combobox = ttk.Combobox(
    root,
    values=[ "blue","green", "cyan", "purple", "yellow", "none"],
    state="readonly"
)
color_combobox.pack(pady=5)

# Привязываем обработчики событий клавиатуры
keys_entry.bind("<KeyPress>", on_key_press)
keys_entry.bind("<KeyRelease>", on_key_release)

# Кнопка для добавления сочетания
add_button = ttk.Button(
    root,
    text="Добавить новое сочетание",
    command=add_combination,
    style="Rounded.TButton"
)
add_button.pack(pady=10)

# Область с прокруткой для списка сочетаний
scroll_frame = tk.Frame(root, bg="#424242")
scroll_frame.pack(fill=tk.BOTH, expand=True, pady=10)

scrollbar = ttk.Scrollbar(scroll_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

combinations_canvas = tk.Canvas(
    scroll_frame,
    bg="#424242",
    yscrollcommand=scrollbar.set,
    highlightthickness=0
)
combinations_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=combinations_canvas.yview)

combinations_frame = tk.Frame(combinations_canvas, bg="#424242")
combinations_canvas.create_window((0, 0), window=combinations_frame, anchor="nw")

def on_frame_configure(event):
    combinations_canvas.configure(scrollregion=combinations_canvas.bbox("all"))

combinations_frame.bind("<Configure>", on_frame_configure)

# Запуск приложения
update_combinations_list()
root.mainloop()