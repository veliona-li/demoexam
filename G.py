import os
import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry


# Функции работы с базой данных
def create_db():
    try:
        conn = sqlite3.connect('bookstore.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                genre TEXT NOT NULL,
                price REAL NOT NULL,
                pub_date TEXT NOT NULL,
                stock TEXT NOT NULL
            )
        ''')

        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error creating database: {e}")

def add_book(title, author, genre, price, pub_date, stock):
    try:
        conn = sqlite3.connect('bookstore.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO books (title, author, genre, price, pub_date, stock) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, author, genre, price, pub_date, stock))

        conn.commit()
        conn.close()
        messagebox.showinfo("Успех", "Книга успешно добавлена!")
    except Exception as e:
        print(f"Error adding book: {e}")
        messagebox.showerror("Ошибка", f"Ошибка при добавлении книги: {e}")

def view_books():
    try:
        conn = sqlite3.connect('bookstore.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM books')
        rows = cursor.fetchall()

        conn.close()
        return rows
    except Exception as e:
        print(f"Error viewing books: {e}")
        return []

def search_books(title):
    try:
        conn = sqlite3.connect('bookstore.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM books WHERE title LIKE ?', ('%' + title + '%',))
        rows = cursor.fetchall()

        conn.close()
        return rows
    except Exception as e:
        print(f"Error searching books: {e}")
        return []

def delete_book(book_id):
    try:
        conn = sqlite3.connect('bookstore.db')
        cursor = conn.cursor()

        cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))

        conn.commit()
        conn.close()
        messagebox.showinfo("Успех", f"Книга с ID {book_id} успешно удалена!")
    except Exception as e:
        print(f"Error deleting book: {e}")
        messagebox.showerror("Ошибка", f"Ошибка при удалении книги: {e}")

# Графический интерфейс
class BookstoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Система управления книжным магазином")
        self.center_window(1000, 700)

        # Меню
        menubar = tk.Menu(root)
        root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Добавить книгу", command=self.open_add_book_window)
        file_menu.add_command(label="Удалить книгу", command=self.open_delete_book_window)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=root.quit)

        # Поисковая строка
        self.search_frame = ttk.Frame(root)
        self.search_frame.pack(fill=tk.X, padx=10, pady=5)

        self.search_label = ttk.Label(self.search_frame, text="Поиск по названию:")
        self.search_label.pack(side=tk.LEFT, padx=(0, 5))

        self.search_entry = ttk.Entry(self.search_frame)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.search_button = ttk.Button(self.search_frame, text="Поиск", command=self.search_books)
        self.search_button.pack(side=tk.LEFT, padx=(5, 0))

        # Таблица книг
        self.tree_frame = ttk.Frame(root)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)

        self.tree_scroll = ttk.Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(self.tree_frame, columns=(
        "id", "title", "author", "genre", "price", "pub_date", "stock"),
                                 show='headings', yscrollcommand=self.tree_scroll.set)
        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Название")
        self.tree.heading("author", text="Автор")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("price", text="Цена")
        self.tree.heading("pub_date", text="Дата публикации")
        self.tree.heading("stock", text="В наличии")

        self.tree.column("id", width=40)
        self.tree.column("title", width=150)
        self.tree.column("author", width=150)
        self.tree.column("genre", width=100)
        self.tree.column("price", width=80)
        self.tree.column("pub_date", width=100)
        self.tree.column("stock", width=80)

        self.tree.tag_configure('out_of_stock', background='#FFCCCC')  # Красный для отсутствующих в наличии
        self.tree.tag_configure('in_stock', background='#CCFFCC')  # Зеленый для в наличии

        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree_scroll.config(command=self.tree.yview)

        self.tree.bind("<Double-1>", self.open_book_detail_window)

        self.view_books()

    def center_window(self, width=1000, height=700):
        # Получаем размеры экрана
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Рассчитываем позицию окна по центру
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        # Устанавливаем размеры и позицию окна
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def open_add_book_window(self):
        self.add_book_window = tk.Toplevel(self.root)
        self.add_book_window.title("Добавить книгу")
        self.add_book_window.geometry("400x400")

        self.title_label = ttk.Label(self.add_book_window, text="Название")
        self.title_label.pack(pady=5)
        self.title_entry = ttk.Entry(self.add_book_window)
        self.title_entry.pack(pady=5)

        self.author_label = ttk.Label(self.add_book_window, text="Автор")
        self.author_label.pack(pady=5)
        self.author_entry = ttk.Entry(self.add_book_window)
        self.author_entry.pack(pady=5)

        self.genre_label = ttk.Label(self.add_book_window, text="Жанр")
        self.genre_label.pack(pady=5)
        self.genre_entry = ttk.Entry(self.add_book_window)
        self.genre_entry.pack(pady=5)

        self.price_label = ttk.Label(self.add_book_window, text="Цена")
        self.price_label.pack(pady=5)
        self.price_entry = ttk.Entry(self.add_book_window)
        self.price_entry.pack(pady=5)

        self.pub_date_label = ttk.Label(self.add_book_window, text="Дата публикации")
        self.pub_date_label.pack(pady=5)
        self.pub_date_entry = DateEntry(self.add_book_window, date_pattern='y-mm-dd')
        self.pub_date_entry.pack(pady=5)

        self.stock_label = ttk.Label(self.add_book_window, text="В наличии")
        self.stock_label.pack(pady=5)
        self.stock_combo = ttk.Combobox(self.add_book_window, values=["Да", "Нет"])
        self.stock_combo.pack(pady=5)

        self.submit_button = ttk.Button(self.add_book_window, text="Добавить книгу", command=self.submit_book)
        self.submit_button.pack(pady=10)

    def submit_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        genre = self.genre_entry.get()
        price = self.price_entry.get()
        pub_date = self.pub_date_entry.get()
        stock = self.stock_combo.get()
        if title and author and genre and price and pub_date and stock:
            add_book(title, author, genre, float(price), pub_date, stock)
            self.add_book_window.destroy()
            self.view_books()
        else:
            messagebox.showerror("Ошибка", "Все поля обязательны для заполнения!")

    def open_delete_book_window(self):
        self.delete_book_window = tk.Toplevel(self.root)
        self.delete_book_window.title("Удалить книгу")
        self.delete_book_window.geometry("300x150")

        self.delete_label = ttk.Label(self.delete_book_window, text="ID книги для удаления")
        self.delete_label.pack(pady=5)
        self.delete_entry = ttk.Entry(self.delete_book_window)
        self.delete_entry.pack(pady=5)

        self.delete_button = ttk.Button(self.delete_book_window, text="Удалить книгу", command=self.delete_book)
        self.delete_button.pack(pady=10)

    def delete_book(self):
        book_id = self.delete_entry.get()
        if book_id:
            delete_book(book_id)
            self.delete_book_window.destroy()
            self.view_books()
        else:
            messagebox.showerror("Ошибка", "ID книги обязательно для заполнения!")

    def open_book_detail_window(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            book_id = item['values'][0]

            book = self.get_book_by_id(book_id)
            if book:
                self.detail_window = tk.Toplevel(self.root)
                self.detail_window.title("Детали книги")
                self.detail_window.geometry("400x400")

                detail_frame = ttk.Frame(self.detail_window, padding="10")
                detail_frame.pack(fill=tk.BOTH, expand=True)

                ttk.Label(detail_frame, text="ID:", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w", pady=2)
                ttk.Label(detail_frame, text=book[0], font=("Arial", 12)).grid(row=0, column=1, sticky="w", pady=2)

                ttk.Label(detail_frame, text="Название:", font=("Arial", 12, "bold")).grid(row=1, column=0, sticky="w", pady=2)
                ttk.Label(detail_frame, text=book[1], font=("Arial", 12)).grid(row=1, column=1, sticky="w", pady=2)

                ttk.Label(detail_frame, text="Автор:", font=("Arial", 12, "bold")).grid(row=2, column=0, sticky="w", pady=2)
                ttk.Label(detail_frame, text=book[2], font=("Arial", 12)).grid(row=2, column=1, sticky="w", pady=2)

                ttk.Label(detail_frame, text="Жанр:", font=("Arial", 12, "bold")).grid(row=3, column=0, sticky="w", pady=2)
                ttk.Label(detail_frame, text=book[3], font=("Arial", 12)).grid(row=3, column=1, sticky="w", pady=2)

                ttk.Label(detail_frame, text="Цена:", font=("Arial", 12, "bold")).grid(row=4, column=0, sticky="w", pady=2)
                ttk.Label(detail_frame, text=book[4], font=("Arial", 12)).grid(row=4, column=1, sticky="w", pady=2)

                ttk.Label(detail_frame, text="Дата публикации:", font=("Arial", 12, "bold")).grid(row=5, column=0, sticky="w", pady=2)
                ttk.Label(detail_frame, text=book[5], font=("Arial", 12)).grid(row=5, column=1, sticky="w", pady=2)

                ttk.Label(detail_frame, text="В наличии:", font=("Arial", 12, "bold")).grid(row=6, column=0, sticky="w", pady=2)
                ttk.Label(detail_frame, text=book[6], font=("Arial", 12)).grid(row=6, column=1, sticky="w", pady=2)

    def get_book_by_id(self, book_id):
        try:
            conn = sqlite3.connect('bookstore.db')
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
            row = cursor.fetchone()

            conn.close()
            return row
        except Exception as e:
            print(f"Error retrieving book: {e}")
            return None

    def search_books(self):
        title = self.search_entry.get()
        filtered_books = search_books(title)
        self.update_tree(filtered_books)

    def view_books(self):
        all_books = view_books()
        self.update_tree(all_books)

    def update_tree(self, books):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for book in books:
            tags = ()
            if book[6] == "Нет":
                tags += ('out_of_stock',)
            else:
                tags += ('in_stock',)

            self.tree.insert('', tk.END, values=(book[0], book[1], book[2], book[3], book[4], book[5], book[6]), tags=tags)


if __name__ == "__main__":
    create_db()
    root = tk.Tk()
    app = BookstoreApp(root)
    root.mainloop()
