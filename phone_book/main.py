import tkinter as tk                                           #Импортируем библиотеку Tkinter
from tkinter import ttk                                        #Импортируем виджет TreeView
import sqlite3                                                 #Импортируем встраиваемую СУБД SqlLite3


class Main(tk.Frame):                 #Создаем класс главного окна
    def __init__(self, root):         #Конструктор __init__(отвечает за инициализацию)
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):      #Создаем функцию хранения и инициализации объектов графического интерфейса(панель инструментов)
        toolbar = tk.Frame(bg="#d7d8e0", bd=2)                      #Создание панели инструментов
        toolbar.pack(side=tk.TOP, fill=tk.X)
        self.add_img = tk.PhotoImage(file="./img/add.png")          #Создание кнопки добавления записей
        btn_open_dialog = tk.Button(
            toolbar, bg="#d7d8e0", bd=0, image=self.add_img, command=self.open_dialog
        )
        btn_open_dialog.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(     
            self, columns=("ID", "name", "tel", "email"), height=45, show="headings"      #Создаем таблицу 
        )

        self.tree.column("ID", width=30, anchor=tk.CENTER)     
        self.tree.column("name", width=300, anchor=tk.CENTER)          #Передаем параметры колонкам
        self.tree.column("tel", width=150, anchor=tk.CENTER)           
        self.tree.column("email", width=150, anchor=tk.CENTER)

        self.tree.heading("ID", text="ID")
        self.tree.heading("name", text="ФИО")        #Создаем читаемые названия для колонок которые будет видеть пользователь
        self.tree.heading("tel", text="Телефон")
        self.tree.heading("email", text="E-mail")

        self.tree.pack(side=tk.LEFT)           #'Упаковываем' колонки

        self.update_img = tk.PhotoImage(file="./img/update.png")
        btn_edit_dialog = tk.Button(
            toolbar,
            bg="#d7d8e0",                     #Создание кнопки редактирования записей
            bd=0,
            image=self.update_img,
            command=self.open_update_dialog,
        )
        btn_edit_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file="./img/delete.png")
        btn_delete = tk.Button(
            toolbar,
            bg="#d7d8e0",                     #Создание кнопки удаления записей
            bd=0,
            image=self.delete_img,
            command=self.delete_records,
        )
        btn_delete.pack(side=tk.LEFT)

        self.search_img = tk.PhotoImage(file="./img/search.png")
        btn_search = tk.Button(
            toolbar,
            bg="#d7d8e0",                     #Создание кнопки поиска записей
            bd=0,
            image=self.search_img,
            command=self.open_search_dialog,
        )
        btn_search.pack(side=tk.LEFT)

    def open_dialog(self):             #Вызывает дочернее окно(окно добавления данных)
        Child()

    def records(self, name, tel, email):        #Метод вызывающий метод записи
        self.db.insert_data(name, tel, email)
        self.view_records()

    def view_records(self):         #Метод для отображения записей на главном окне
        self.db.cursor.execute("SELECT * FROM db")
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=row) for row in self.db.cursor.fetchall()]

    def open_update_dialog(self):        #Вызывает дочернее окно(окно редактирования данных)
        Update()

    def update_records(self, name, tel, email):      #Метод для редактирования записей
        self.db.cursor.execute(
            """UPDATE db SET name=?, tel=?, email=? WHERE id=?""",
            (name, tel, email, self.tree.set(self.tree.selection()[0], "#1")),
        )
        self.db.conn.commit()
        self.view_records()

    def delete_records(self):           #Метод для удаления записей
        for selection_items in self.tree.selection():
            self.db.cursor.execute(
                "DELETE FROM db WHERE id=?", (self.tree.set(selection_items, "#1"))
            )
        self.db.conn.commit()
        self.view_records()

    def open_search_dialog(self):       #Вызывает дочернее окно(окно поиска данных)               
        Search()

    def search_records(self, name):     #Метод для поиска данных(поиск по строке name, а после поиска очищение таблицы кроме выбранного запроса)
        name = "%" + name + "%"
        self.db.cursor.execute("SELECT * FROM db WHERE name LIKE ?", (name,)) 

        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=row) for row in self.db.cursor.fetchall()]


class Child(tk.Toplevel):                                            #Класс отвечающий за дочерние окна
    def __init__(self):                                              #Конструктор __init__(отвечает за инициализацию)
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):                                            #Метод инициализации и хранения объектов графического интерфейса(окно добавления контакта)
        self.title("Добавить")
        self.geometry("400x220")
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()

        label_name = tk.Label(self, text="ФИО:")
        label_name.place(x=50, y=50)
        label_select = tk.Label(self, text="Телефон:")
        label_select.place(x=50, y=80)
        label_sum = tk.Label(self, text="E-mail:")
        label_sum.place(x=50, y=110)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=80)
        self.entry_tel = ttk.Entry(self)
        self.entry_tel.place(x=200, y=110)

        self.btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        self.btn_cancel.place(x=220, y=170)

        self.btn_ok = ttk.Button(self, text="Добавить")
        self.btn_ok.place(x=300, y=170)

        self.btn_ok.bind(
            "<Button-1>",
            lambda event: self.view.records(
                self.entry_name.get(), self.entry_email.get(), self.entry_tel.get()
            ),
        )


class Update(Child):        #Класс отвечающий за изменение данных уже существующих контактов
    def __init__(self):     #Конструктор __init__(отвечает за инициализацию)
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):      #Метод инициализации и хранения объектов графического интерфейса(окно редактирования контакта)
        self.title("Редактирование контакта")
        btn_edit = ttk.Button(self, text="Редактировать")
        btn_edit.place(x=205, y=170)
        btn_edit.bind(
            "<Button-1>",
            lambda event: self.view.update_records(
                self.entry_name.get(), self.entry_email.get(), self.entry_tel.get()
            ),
        )
        btn_edit.bind("<Button-1>", lambda event: self.destroy(), add="+")
        self.btn_ok.destroy()

    def default_data(self):         #Метод для подгрузки данных в окно редактирования данных
        self.db.cursor.execute(
            "SELECT * FROM db WHERE id=?",
            self.view.tree.set(self.view.tree.selection()[0], "#1"),
        )
        row = self.db.cursor.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_email.insert(0, row[2])
        self.entry_tel.insert(0, row[3])


class Search(tk.Toplevel):       #Класс отвечающий за поиск уже существующих данных
    def __init__(self):          #Конструктор __init__(отвечает за инициализацию)
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):       #Метод инициализации и хранения объектов графического интерфейса(окно поиска контакта)
        self.title("Поиск контакта")
        self.geometry("300x100")
        self.resizable(False, False)

        label_search = tk.Label(self, text="Имя:")
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=100, y=20, width=150)

        btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy) 
        btn_cancel.place(x=185, y=50)

        search_btn = ttk.Button(self, text="Найти")
        search_btn.place(x=105, y=50)
        search_btn.bind(
            "<Button-1>",
            lambda event: self.view.search_records(self.entry_search.get()),
        )
        search_btn.bind("<Button-1>", lambda event: self.destroy(), add="+")


class DB:            #Создаем класс базы данных
    def __init__(self):            #Конструктор __init__(отвечает за инициализацию)
        self.conn = sqlite3.connect("db.db")        #Создаем соединение с базой данных
        self.cursor = self.conn.cursor()
        self.cursor.execute(            #Делаем запрос
            """CREATE TABLE IF NOT EXISTS db (
                id INTEGER PRIMARY KEY,               
                name TEXT,
                tel TEXT,
                email TEXT
            )"""
        )
        self.conn.commit()

    def insert_data(self, name, tel, email):       #Метод для добавления данных в базу данных
        self.cursor.execute(
            """INSERT INTO db(name, tel, email) VALUES(?, ?, ?)""", (name, tel, email)
        )
        self.conn.commit()


if __name__ == "__main__":         #Создание главного окна
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Телефонная книга")
    root.geometry("665x450")
    root.resizable(False, False)
    root.mainloop()
