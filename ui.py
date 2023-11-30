import tkinter as tk
from tkinter import messagebox, Listbox, ttk, filedialog
import sys
import ftplib
import os

# выход из программы
def exit():
    sys.exit()

def connect():
    host = host_entry.get() 
    login = login_entry.get() 
    password = password_entry.get()
    try:
        ftp = ftplib.FTP(host, login, password)
        print(ftp.nlst())
        input_frame.pack_forget()
        messagebox.showinfo("Успех", "Вы подключились к ftp-серверу")
        folder = ''
        progress = ttk.Progressbar(root, orient="horizontal", length=128, mode="determinate")
        progress.pack(pady=20)
        question_button = tk.Button(root, text="Создать каталоги по заданию", command=lambda: make_directories(ftp, progress), bg = 'green')
        question_button.pack()
        display_files(ftp, folder)
    except:
        host_entry.delete(0, tk.END)
        login_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        messagebox.showerror("Ошибка", "Пожалуйста, введите данные заново")
        
def display_files(ftp, folder, path=[], folder_listbox=None, folder_window = None):
    if folder != '':
        ftp.cwd(folder)
    if folder == '..':
        path
    content = ftp.nlst()

    if folder_window is None:
        folder_window = tk.Toplevel(root)
        
        folder_window.geometry('400x300')

        folder_listbox = Listbox(folder_window, width=60, height=10)
        folder_listbox.grid(row=0, column=5)
        select_button = tk.Button(folder_window, text="Загрузить файл", command=lambda: upload_file(ftp), bg='green')
        select_button.grid(row=1, column=5)

        
        upload_entry = tk.Entry(folder_window)
        upload_entry.grid(row=2, column=5)

        upload_button = tk.Button(folder_window, text="Создать каталог", command=lambda: make_directory(ftp, upload_entry.get()), bg='yellow')
        upload_button.grid(row=3, column=5)
        


    path_str = '/'.join(path)
    folder_window.title(f'Каталог {path_str}')

    folder_listbox.delete(0, tk.END)  # Очистка содержимого списка

    for item in content:
        folder_listbox.insert(tk.END, item)

    folder_listbox.insert(tk.END, '..')

    folder_listbox.bind("<Double-Button-1>", lambda event: double_click_action(ftp, folder_listbox.get(tk.ACTIVE), path=path, folder_listbox=folder_listbox, folder_window=folder_window))

def double_click_action(ftp, folder, path=[], folder_listbox=None, folder_window = None):
    if folder == '..':
        if path == []:
            pass
        else:
            path.pop()
    else:
        path.append(folder)
    try:
        display_files(ftp, folder, path=path, folder_listbox=folder_listbox, folder_window=folder_window)
    except:
        download_file(ftp, folder)
        path.pop()
        folder = path[-1]

def download_file(ftp, filename):
    with open(filename, 'wb') as file:
        ftp.retrbinary('RETR ' + filename, file.write)
    print(f"Файл {filename} успешно загружен")

def upload_file(ftp):
    try:
        file_path = filedialog.askopenfilename()
        file_path = file_path.replace("/", r"\\")
        with open(file_path, 'rb') as file:
        # Загружаем файл на FTP сервер
            ftp.storbinary(f'STOR {os.path.basename(file_path)}', file)
            messagebox.showinfo("Успех", "Вы загрузили файл на сервер")
    except:
        messagebox.showerror("Ошибка", "Не удалось загрузить файл на сервер")

def make_directory(ftp, directory):
    try:
        ftp.mkd(directory)
        messagebox.showinfo("Успех", "Вы создали каталог")
    except:
        messagebox.showerror("Ошибка", "Не удалось создать каталог")


# функция создания директорий в соответствии с заданием
def make_directories(ftp, progress):
    ftp.cwd('/')
    ftp.cwd('SudakovZM_4041')
    print(ftp.nlst())
    directories = ftp.nlst()
    for i in range(65, 73):
        if chr(i) in directories:
            ftp.cwd(chr(i))
            for d in ftp.nlst():
                ftp.rmd(d)
            ftp.cwd('..')
        ftp.mkd(chr(i))
        progress["value"] += 2
        ftp.cwd(chr(i))
        for i in range(65, 73):
            ftp.mkd(chr(i))
            progress["value"] += 2
        ftp.cwd('..')
    ftp.nlst()

if __name__ == '__main__':
    # создаем главное окно
    root = tk.Tk()
    # задаем размер окна
    root.geometry('400x300')

    # задаем имя окна
    root.title('FTP client')

    input_frame = tk.Frame(root)
    input_frame.pack()

    information_label = tk.Label(input_frame, text="Введите данные для входа:")
    information_label.pack()


    host_label = tk.Label(input_frame, text="Адрес сервера:")
    host_label.pack()
    host_entry = tk.Entry(input_frame)
    host_entry.pack()

    login_label = tk.Label(input_frame, text="Логин:")
    login_label.pack()
    login_entry = tk.Entry(input_frame)
    login_entry.pack()

    password_label = tk.Label(input_frame, text="Пароль:")
    password_label.pack()
    password_entry = tk.Entry(input_frame, show = '*')
    password_entry.pack()

    submit_connection = tk.Button(input_frame, text="Отправить", command=connect)
    submit_connection.pack()

    exit_button = tk.Button(root, text="Выход", command=exit, bg = 'red')
    exit_button.pack(side="bottom", anchor = "se")
    root.mainloop()

