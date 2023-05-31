import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
import hashlib

def verificar_login():
    username = entry_username.get()
    password = entry_password.get()

    # Conexão com o banco de dados SQLite
    conn = sqlite3.connect("almoxarifado.db")
    cursor = conn.cursor()

    # Verifique as credenciais do usuário no banco de dados
    cursor.execute("SELECT * FROM usuarios WHERE username=?", (username,))
    user = cursor.fetchone()

    if user:
        stored_password = user[1]  # A senha armazenada está na segunda coluna da tabela
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        if hashed_password == stored_password:
            messagebox.showinfo("Login", "Login bem-sucedido!")
            # Destrua a janela de login e crie a nova janela com os menus
            login_window.destroy()
            conn.close()  # Feche a conexão com o banco de dados
            estoque()
        else:
            messagebox.showerror("Login", "Usuário ou senha incorretos.")
    else:
        messagebox.showerror("Login", "Usuário ou senha incorretos.")
    conn.close()  # Feche a conexão com o banco de dados

def criar_usuario():
    username = simpledialog.askstring("Novo Usuário", "Digite o nome de usuário:")
    password = simpledialog.askstring("Novo Usuário", "Digite a senha:")

    if username and password:
        # Conexão com o banco de dados SQLite
        conn = sqlite3.connect("almoxarifado.db")
        cursor = conn.cursor()

        # Verifica se o usuário já existe
        cursor.execute("SELECT * FROM usuarios WHERE username=?", (username,))
        user = cursor.fetchone()

        if user:
            messagebox.showerror("Novo Usuário", "O usuário já existe.")
        else:
            # Criptografa a senha usando SHA-256
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            # Insere o novo usuário no banco de dados
            cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            messagebox.showinfo("Novo Usuário", "Usuário criado com sucesso.")
        conn.close()  # Feche a conexão com o banco de dados
    else:
        messagebox.showerror("Novo Usuário", "Nome de usuário e senha são obrigatórios.")

def estoque():
    # Sistema do almoxarifado
    menu_window = tk.Tk()
    menu_window.title("Janela de Menus")
    menu_window.geometry("400x300")

    # Conexão com o banco de dados SQLite
    conn = sqlite3.connect("almoxarifado.db")
    cursor = conn.cursor()

    # Criação da tabela de itens do almoxarifado
    cursor.execute("CREATE TABLE IF NOT EXISTS itens (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, quantidade INTEGER)")
    conn.commit()

    # Adicionar item ao almoxarifado
    def cadastrar_item():
        nome = entry_nome_item.get()
        quantidade = entry_quantidade_item.get()

        cursor.execute("INSERT INTO itens (nome, quantidade) VALUES (?, ?)", (nome, quantidade))
        conn.commit()
        messagebox.showinfo("Cadastro de Item", "Item cadastrado com sucesso.")

    # Excluir item do almoxarifado
    def excluir_item():
        item_id = entry_id_item.get()

        cursor.execute("DELETE FROM itens WHERE id=?", (item_id,))
        conn.commit()
        messagebox.showinfo("Exclusão de Item", "Item excluído com sucesso.")

    # Alterar quantidade de um item no almoxarifado
    def alterar_item():
        item_id = entry_id_item.get()
        nova_quantidade = entry_nova_quantidade.get()

        cursor.execute("UPDATE itens SET quantidade=? WHERE id=?", (nova_quantidade, item_id))
        conn.commit()
        messagebox.showinfo("Alteração de Item", "Quantidade do item alterada com sucesso.")

    # Listar todos os itens do almoxarifado
    def listar_itens():
        cursor.execute("SELECT * FROM itens")
        itens = cursor.fetchall()

        messagebox.showinfo("Itens do Almoxarifado", str(itens))

    # Adicionar widgets para o sistema de almoxarifado
    label_nome_item = tk.Label(menu_window, text="Nome do Item:", font=("Arial", 12))
    label_nome_item.place(x=50, y=50)
    entry_nome_item = tk.Entry(menu_window, font=("Arial", 12))
    entry_nome_item.place(x=200, y=50)

    label_quantidade_item = tk.Label(menu_window, text="Quantidade:", font=("Arial", 12))
    label_quantidade_item.place(x=50, y=80)
    entry_quantidade_item = tk.Entry(menu_window, font=("Arial", 12))
    entry_quantidade_item.place(x=200, y=80)

    button_cadastrar_item = tk.Button(menu_window, text="Cadastrar Item", command=cadastrar_item, font=("Arial", 12))
    button_cadastrar_item.place(x=150, y=120)

    label_id_item = tk.Label(menu_window, text="ID do Item:", font=("Arial", 12))
    label_id_item.place(x=50, y=170)
    entry_id_item = tk.Entry(menu_window, font=("Arial", 12))
    entry_id_item.place(x=200, y=170)

    label_nova_quantidade = tk.Label(menu_window, text="Nova Quantidade:", font=("Arial", 12))
    label_nova_quantidade.place(x=50, y=200)
    entry_nova_quantidade = tk.Entry(menu_window, font=("Arial", 12))
    entry_nova_quantidade.place(x=200, y=200)

    button_excluir_item = tk.Button(menu_window, text="Excluir Item", command=excluir_item, font=("Arial", 12))
    button_excluir_item.place(x=150, y=240)

    button_alterar_item = tk.Button(menu_window, text="Alterar Item", command=alterar_item, font=("Arial", 12))
    button_alterar_item.place(x=150, y=270)

    button_listar_itens = tk.Button(menu_window, text="Listar Itens", command=listar_itens, font=("Arial", 12))
    button_listar_itens.place(x=150, y=300)

    menu_window.mainloop()

     # Feche a conexão com o banco de dados
    conn.close()

# Cria o banco de dados se não existir
conn = sqlite3.connect("almoxarifado.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS usuarios (username TEXT, password TEXT)")
conn.commit()
conn.close()

# Cria a janela de login
login_window = tk.Tk()
login_window.title("Janela de Login")
login_window.geometry("300x200")
login_window.resizable(False, False)

# Adicione os widgets para o login
label_username = tk.Label(login_window, text="Usuário:", font=("Arial", 12))
label_username.place(x=50, y=50)
entry_username = tk.Entry(login_window, font=("Arial", 12))
entry_username.place(x=150, y=50)

label_password = tk.Label(login_window, text="Senha:", font=("Arial", 12))
label_password.place(x=50, y=100)
entry_password = tk.Entry(login_window, show="*", font=("Arial", 12))
entry_password.place(x=150, y=100)

button_login = tk.Button(login_window, text="Login", command=verificar_login, font=("Arial", 12))
button_login.place(x=150, y=150)

button_criar_usuario = tk.Button(login_window, text="Criar Usuário", command=criar_usuario, font=("Arial", 12))
button_criar_usuario.place(x=50, y=150)

login_window.mainloop()
