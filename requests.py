import os
import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry


# Функции работы с базой данных
def create_db():
    try:
        conn = sqlite3.connect('requests.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                priority TEXT NOT NULL,
                request_type TEXT NOT NULL,
                description TEXT NOT NULL,
                due_date TEXT NOT NULL,
                responsible TEXT NOT NULL,
                status TEXT NOT NULL
            )
        ''')

        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error creating database: {e}")

def add_request(subject, priority, request_type, description, due_date, responsible, status):
    try:
        conn = sqlite3.connect('requests.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO requests (subject, priority, request_type, description, due_date, responsible, status) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (subject, priority, request_type, description, due_date, responsible, status))

        conn.commit()
        conn.close()
        messagebox.showinfo("Успех", "Заявка успешно добавлена!")
    except Exception as e:
        print(f"Error adding request: {e}")
        messagebox.showerror("Ошибка", f"Ошибка при добавлении заявки: {e}")

def view_requests():
    try:
        conn = sqlite3.connect('requests.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM requests')
        rows = cursor.fetchall()

        conn.close()
        return rows
    except Exception as e:
        print(f"Error viewing requests: {e}")
        return []

def search_requests(subject):
    try:
        conn = sqlite3.connect('requests.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM requests WHERE subject LIKE ?', ('%' + subject + '%',))
        rows = cursor.fetchall()

        conn.close()
        return rows
    except Exception as e:
        print(f"Error searching requests: {e}")
        return []

def delete_request(request_id):
    try:
        conn = sqlite3.connect('requests.db')
        cursor = conn.cursor()

        cursor.execute('DELETE FROM requests WHERE id = ?', (request_id,))

        conn.commit()
        conn.close()
        messagebox.showinfo("Успех", f"Заявка с ID {request_id} успешно удалена!")
    except Exception as e:
        print(f"Error deleting request: {e}")
        messagebox.showerror("Ошибка", f"Ошибка при удалении заявки: {e}")

# Графический интерфейс
class RequestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Система управления заявками")
        self.center_window(1000, 700)

        # Меню
        menubar = tk.Menu(root)
        root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Создать заявку", command=self.open_create_request_window)
        file_menu.add_command(label="Удалить заявку", command=self.open_delete_request_window)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=root.quit)

        # Поисковая строка
        self.search_frame = ttk.Frame(root)
        self.search_frame.pack(fill=tk.X, padx=10, pady=5)

        self.search_label = ttk.Label(self.search_frame, text="Поиск по теме:")
        self.search_label.pack(side=tk.LEFT, padx=(0, 5))

        self.search_entry = ttk.Entry(self.search_frame)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.search_button = ttk.Button(self.search_frame, text="Поиск", command=self.search_requests)
        self.search_button.pack(side=tk.LEFT, padx=(5, 0))

        # Таблица заявок
        self.tree_frame = ttk.Frame(root)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)

        self.tree_scroll = ttk.Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(self.tree_frame, columns=(
        "id", "subject", "priority", "request_type", "due_date", "responsible", "status"),
                                 show='headings', yscrollcommand=self.tree_scroll.set)
        self.tree.heading("id", text="ID")
        self.tree.heading("subject", text="Тема")
        self.tree.heading("priority", text="Приоритет")
        self.tree.heading("request_type", text="Тип")
        self.tree.heading("due_date", text="Плановая дата")
        self.tree.heading("responsible", text="Ответственный")
        self.tree.heading("status", text="Статус")

        self.tree.column("id", width=40)
        self.tree.column("subject", width=150)
        self.tree.column("priority", width=100)
        self.tree.column("request_type", width=100)
        self.tree.column("due_date", width=100)
        self.tree.column("responsible", width=150)
        self.tree.column("status", width=100)

        self.tree.tag_configure('closed', background='#FFCCCC')  # Красный для закрытых заявок
        self.tree.tag_configure('open', background='#CCFFCC')  # Зеленый для открытых заявок
        self.tree.tag_configure('low', background='#F0F0F0')  # Серый для низкого приоритета
        self.tree.tag_configure('medium', background='#FFFF99')  # Желтый для среднего приоритета
        self.tree.tag_configure('high', background='#FF9999')  # Красный для высокого приоритета

        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree_scroll.config(command=self.tree.yview)

        self.tree.bind("<Double-1>", self.open_request_detail_window)

        self.view_requests()

    def center_window(self, width=1000, height=700):
        # Получаем размеры экрана
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Рассчитываем позицию окна по центру
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        # Устанавливаем размеры и позицию окна
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def open_create_request_window(self):
        self.create_request_window = tk.Toplevel(self.root)
        self.create_request_window.title("Создать заявку")
        self.create_request_window.geometry("400x500")

        self.subject_label = ttk.Label(self.create_request_window, text="Тема")
        self.subject_label.pack(pady=5)
        self.subject_entry = ttk.Entry(self.create_request_window)
        self.subject_entry.pack(pady=5)

        self.priority_label = ttk.Label(self.create_request_window, text="Приоритет")
        self.priority_label.pack(pady=5)
        self.priority_combo = ttk.Combobox(self.create_request_window, values=["Низкий", "Средний", "Высокий"])
        self.priority_combo.pack(pady=5)

        self.type_label = ttk.Label(self.create_request_window, text="Тип")
        self.type_label.pack(pady=5)
        self.type_combo = ttk.Combobox(self.create_request_window, values=["Инцидент", "Обслуживание"])
        self.type_combo.pack(pady=5)

        self.desc_label = ttk.Label(self.create_request_window, text="Описание")
        self.desc_label.pack(pady=5)
        self.desc_entry = ttk.Entry(self.create_request_window)
        self.desc_entry.pack(pady=5)

        self.due_date_label = ttk.Label(self.create_request_window, text="Плановая дата")
        self.due_date_label.pack(pady=5)
        self.due_date_entry = DateEntry(self.create_request_window, date_pattern='y-mm-dd')
        self.due_date_entry.pack(pady=5)

        self.responsible_label = ttk.Label(self.create_request_window, text="Ответственный")
        self.responsible_label.pack(pady=5)
        self.responsible_entry = ttk.Entry(self.create_request_window)
        self.responsible_entry.pack(pady=5)

        self.status_label = ttk.Label(self.create_request_window, text="Статус")
        self.status_label.pack(pady=5)
        self.status_combo = ttk.Combobox(self.create_request_window, values=["Открыта", "Закрыта"])
        self.status_combo.pack(pady=5)

        self.submit_button = ttk.Button(self.create_request_window, text="Добавить заявку", command=self.submit_request)
        self.submit_button.pack(pady=10)

    def submit_request(self):
        subject = self.subject_entry.get()
        priority = self.priority_combo.get()
        request_type = self.type_combo.get()
        description = self.desc_entry.get()
        due_date = self.due_date_entry.get()
        responsible = self.responsible_entry.get()
        status = self.status_combo.get()
        if subject and priority and request_type and description and due_date and responsible and status:
            add_request(subject, priority, request_type, description, due_date, responsible, status)
            self.create_request_window.destroy()
            self.view_requests()
        else:
            messagebox.showerror("Ошибка", "Все поля обязательны для заполнения!")

    def open_delete_request_window(self):
        self.delete_request_window = tk.Toplevel(self.root)
        self.delete_request_window.title("Удалить заявку")
        self.delete_request_window.geometry("300x150")

        self.delete_label = ttk.Label(self.delete_request_window, text="ID заявки для удаления")
        self.delete_label.pack(pady=5)
        self.delete_entry = ttk.Entry(self.delete_request_window)
        self.delete_entry.pack(pady=5)

        self.delete_button = ttk.Button(self.delete_request_window, text="Удалить заявку", command=self.delete_request)
        self.delete_button.pack(pady=10)

    def delete_request(self):
        request_id = self.delete_entry.get()
        if request_id:
            delete_request(request_id)
            self.delete_request_window.destroy()
            self.view_requests()
        else:
            messagebox.showerror("Ошибка", "ID заявки обязательно для заполнения!")

    def open_request_detail_window(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            request_id = item['values'][0]

            request = self.get_request_by_id(request_id)
            if request:
                self.detail_window = tk.Toplevel(self.root)
                self.detail_window.title("Детали заявки")
                self.detail_window.geometry("400x400")

                detail_frame = ttk.Frame(self.detail_window, padding="10")
                detail_frame.pack(fill=tk.BOTH, expand=True)

                ttk.Label(detail_frame, text="ID:", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w", pady=2)
                ttk.Label(detail_frame, text=request[0], font=("Arial", 12)).grid(row=0, column=1, sticky="w", pady=2)

                ttk.Label(detail_frame, text="Тема:", font=("Arial", 12, "bold")).grid(row=1, column=0, sticky="w", pady=2)
                ttk.Label(detail_frame, text=request[1], font=("Arial", 12)).grid(row=1, column=1, sticky="w", pady=2)

                ttk.Label(detail_frame, text="Приоритет:", font=("Arial", 12, "bold")).grid(row=2, column=0, sticky="w", pady=2)
                ttk.Label(detail_frame, text=request[2], font=("Arial", 12)).grid(row=2, column=1, sticky="w", pady=2)

                ttk.Label(detail_frame, text="Тип:", font=("Arial", 12, "bold")).grid(row=3, column=0, sticky="w", pady=2)
                ttk.Label(detail_frame, text=request[3], font=("Arial", 12)).grid(row=3, column=1, sticky="w", pady=2)

                ttk.Label(detail_frame, text="Описание:", font=("Arial", 12, "bold")).grid(row=4, column=0, sticky="w", pady=2)
                ttk.Label(detail_frame, text=request[4], font=("Arial", 12), wraplength=300).grid(row=4, column=1, sticky="w", pady=2)

                ttk.Label(detail_frame, text="Плановая дата:", font=("Arial", 12, "bold")).grid(row=5, column=0, sticky="w", pady=2)
                ttk.Label(detail_frame, text=request[5], font=("Arial", 12)).grid(row=5, column=1, sticky="w", pady=2)

                ttk.Label(detail_frame, text="Ответственный:", font=("Arial", 12, "bold")).grid(row=6, column=0, sticky="w", pady=2)
                ttk.Label(detail_frame, text=request[6], font=("Arial", 12)).grid(row=6, column=1, sticky="w", pady=2)

                ttk.Label(detail_frame, text="Статус:", font=("Arial", 12, "bold")).grid(row=7, column=0, sticky="w", pady=2)
                ttk.Label(detail_frame, text=request[7], font=("Arial", 12)).grid(row=7, column=1, sticky="w", pady=2)

    def get_request_by_id(self, request_id):
        try:
            conn = sqlite3.connect('requests.db')
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM requests WHERE id = ?', (request_id,))
            row = cursor.fetchone()

            conn.close()
            return row
        except Exception as e:
            print(f"Error retrieving request: {e}")
            return None

    def search_requests(self):
        subject = self.search_entry.get()
        filtered_requests = search_requests(subject)
        self.update_tree(filtered_requests)

    def view_requests(self):
        all_requests = view_requests()
        self.update_tree(all_requests)

    def update_tree(self, requests):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for request in requests:
            tags = ()
            if request[7] == "Закрыта":
                tags += ('closed',)
            else:
                tags += ('open',)

            if request[2] == "Низкий":
                tags += ('low',)
            elif request[2] == "Средний":
                tags += ('medium',)
            elif request[2] == "Высокий":
                tags += ('high',)

            self.tree.insert('', tk.END, values=(request[0], request[1], request[2], request[3], request[5], request[6], request[7]), tags=tags)


if __name__ == "__main__":
    create_db()
    root = tk.Tk()
    app = RequestApp(root)
    root.mainloop()
