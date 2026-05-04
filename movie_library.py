import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATA_FILE = "data/movies.json"

def load_movies():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_movies(movies):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(movies, f, ensure_ascii=False, indent=2)

def add_movie():
    title = entry_title.get().strip()
    genre = entry_genre.get().strip()
    year = entry_year.get().strip()
    rating = entry_rating.get().strip()

    if not title or not genre or not year or not rating:
        messagebox.showerror("Ошибка", "Все поля обязательны для заполнения!")
        return

    try:
        year = int(year)
        rating = float(rating)
        if not (0 <= rating <= 10):
            raise ValueError
    except ValueError:
        messagebox.showerror("Ошибка", "Год — целое число, рейтинг — число от 0 до 10.")
        return

    movie = {"title": title, "genre": genre, "year": year, "rating": rating}
    movies.append(movie)
    save_movies(movies)
    update_table()
    clear_entries()

def update_table(filter_genre=None, filter_year=None):
    for i in tree.get_children():
        tree.delete(i)
    for movie in movies:
        if filter_genre and movie["genre"].lower() != filter_genre.lower():
            continue
        if filter_year and movie["year"] != filter_year:
            continue
        tree.insert("", "end", values=(movie["title"], movie["genre"], movie["year"], movie["rating"]))

def clear_entries():
    entry_title.delete(0, tk.END)
    entry_genre.delete(0, tk.END)
    entry_year.delete(0, tk.END)
    entry_rating.delete(0, tk.END)

movies = load_movies()

root = tk.Tk()
root.title("Movie Library")

tk.Label(root, text="Название:").grid(row=0, column=0, padx=5, pady=5)
entry_title = tk.Entry(root, width=30)
entry_title.grid(row=0, column=1, columnspan=3, padx=5, pady=5)

tk.Label(root, text="Жанр:").grid(row=1, column=0, padx=5, pady=5)
entry_genre = tk.Entry(root, width=30)
entry_genre.grid(row=1, column=1, columnspan=3, padx=5, pady=5)

tk.Label(root, text="Год:").grid(row=2, column=0, padx=5, pady=5)
entry_year = tk.Entry(root, width=10)
entry_year.grid(row=2, column=1, sticky="w", padx=5, pady=5)

tk.Label(root, text="Рейтинг:").grid(row=2, column=2, padx=5, pady=5)
entry_rating = tk.Entry(root, width=10)
entry_rating.grid(row=2, column=3, sticky="w", padx=5, pady=5)

tk.Button(root, text="Добавить фильм", command=add_movie).grid(row=3, column=0, columnspan=4, pady=10)

tk.Label(root, text="Фильтр по жанру:").grid(row=4, column=0, padx=5, pady=5)
filter_genre_var = tk.StringVar()
filter_genre_entry = tk.Entry(root, textvariable=filter_genre_var, width=20)
filter_genre_entry.grid(row=4, column=1, columnspan=2, padx=5, pady=5)
tk.Button(root, text="Фильтровать", command=lambda: update_table(filter_genre_var.get())).grid(row=4, column=3)

tk.Label(root, text="Фильтр по году:").grid(row=5, column=0, padx=5, pady=5)
filter_year_var = tk.StringVar()
filter_year_entry = tk.Entry(root, textvariable=filter_year_var, width=20)
filter_year_entry.grid(row=5, column=1, columnspan=2, padx=5, pady=5)
tk.Button(
    root,
    text="Фильтровать",
    command=lambda: update_table(filter_year=int(filter_year_var.get()) if filter_year_var.get().isdigit() else None),
).grid(row=5, column=3)

columns = ("Название", "Жанр", "Год", "Рейтинг")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)
tree.grid(row=6, column=0, columnspan=4, pady=10)

update_table()
root.mainloop()
