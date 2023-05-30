import tkinter as tk
from tkinter import messagebox
import sqlite3

# Variáveis globais
entry_nome = None
entry_quantidade = None
treeview = None
entry_usuario = None
entry_senha = None

# Função para criar a tabela no banco de dados
def criar_tabela():
    conn = sqlite3.connect('almoxarifado.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS estoque
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       nome TEXT NOT NULL,
                       quantidade INTEGER NOT NULL)''')
    conn.commit()
    conn.close()

# Função para cadastrar um item no estoque
def cadastrar_item():
    global entry_nome
    global entry_quantidade
    nome = entry_nome.get()
    quantidade = entry_quantidade.get()

    if nome and quantidade:
        conn = sqlite3.connect('almoxarifado.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO estoque (nome, quantidade) VALUES (?, ?)', (nome, quantidade))
        conn.commit()
        conn.close()
        messagebox.showinfo('Sucesso', 'Item cadastrado com sucesso.')
        limpar_campos()
        listar_itens()
    else:
        messagebox.showwarning('Erro', 'Preencha todos os campos.')

# Função para excluir um item do estoque
def excluir_item():
    global treeview
    selected_item = treeview.focus()
    if selected_item:
        item_id = treeview.item(selected_item)['text']
        conn = sqlite3.connect('almoxarifado.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM estoque WHERE id = ?', (item_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo('Sucesso', 'Item excluído com sucesso.')
        listar_itens()
    else:
        messagebox.showwarning('Erro', 'Selecione um item para excluir.')

# Função para alterar um item do estoque
def alterar_item():
    global treeview
    global entry_nome
    global entry_quantidade
    selected_item = treeview.focus()
    if selected_item:
        item_id = treeview.item(selected_item)['text']
        nome = entry_nome.get()
        quantidade = entry_quantidade.get()

        if nome and quantidade:
            conn = sqlite3.connect('almoxarifado.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE estoque SET nome = ?, quantidade = ? WHERE id = ?', (nome, quantidade, item_id))
            conn.commit()
            conn.close()
            messagebox.showinfo('Sucesso', 'Item alterado com sucesso.')
            limpar_campos()
            listar_itens()
        else:
            messagebox.showwarning('Erro', 'Preencha todos os campos.')
    else:
        messagebox.showwarning('Erro', 'Selecione um item para alterar.')

# Função para listar os itens do estoque
def listar_itens():
    global treeview
    conn = sqlite3.connect('almoxarifado.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM estoque')
    rows = cursor.fetchall()
    treeview.delete(*treeview.get_children())
    for row in rows:
        treeview.insert('', 'end', text=row[0], values=(row[1], row[2]))
    conn.close()

# Função para limpar os campos de entrada
def limpar_campos():
    global entry_nome
    global entry_quantidade
    entry_nome.delete(0, 'end')
    entry_quantidade.delete(0, 'end')

# Função para criar a janela de login
def login():
    global entry_usuario
    global entry_senha

    def autenticar():
        usuario = entry_usuario.get()
        senha = entry_senha.get()
        if usuario == 'admin' and senha == '123456':
            messagebox.showinfo('Sucesso', 'Login realizado com sucesso.')
            login_window.destroy()
            criar_tabela()
            listar_itens()
        else:
            messagebox.showwarning('Erro', 'Usuário ou senha inválidos.')

    login_window = tk.Toplevel(root)
    login_window.title('Login')

    label_usuario = tk.Label(login_window, text='Usuário:')
    label_usuario.pack()
    entry_usuario = tk.Entry(login_window)
    entry_usuario.pack()

    label_senha = tk.Label(login_window, text='Senha:')
    label_senha.pack()
    entry_senha = tk.Entry(login_window, show='*')
    entry_senha.pack()

    btn_login = tk.Button(login_window, text='Login', command=autenticar)
    btn_login.pack()

# Função para criar a janela principal
def main_window():
    global entry_nome
    global entry_quantidade
    global treeview

    root.withdraw()

    main_window = tk.Toplevel(root)
    main_window.title('Sistema de Almoxarifado')

    frame_cadastro = tk.Frame(main_window)
    frame_cadastro.pack(pady=10)

    label_nome = tk.Label(frame_cadastro, text='Nome:')
    label_nome.grid(row=0, column=0, sticky='w')
    entry_nome = tk.Entry(frame_cadastro)
    entry_nome.grid(row=0, column=1)

    label_quantidade = tk.Label(frame_cadastro, text='Quantidade:')
    label_quantidade.grid(row=1, column=0, sticky='w')
    entry_quantidade = tk.Entry(frame_cadastro)
    entry_quantidade.grid(row=1, column=1)

    btn_cadastrar = tk.Button(frame_cadastro, text='Cadastrar', command=cadastrar_item)
    btn_cadastrar.grid(row=2, column=0, pady=5)

    btn_excluir = tk.Button(frame_cadastro, text='Excluir', command=excluir_item)
    btn_excluir.grid(row=2, column=1, pady=5)

    btn_alterar = tk.Button(frame_cadastro, text='Alterar', command=alterar_item)
    btn_alterar.grid(row=2, column=2, pady=5)

    frame_lista = tk.Frame(main_window)
    frame_lista.pack(padx=10, pady=10)

    treeview = tk.ttk.Treeview(frame_lista, columns=('nome', 'quantidade'), show='headings')
    treeview.heading('nome', text='Nome')
    treeview.heading('quantidade', text='Quantidade')
    treeview.pack(side='left')

    scrollbar = tk.Scrollbar(frame_lista, orient='vertical', command=treeview.yview)
    scrollbar.pack(side='right', fill='y')

    treeview.configure(yscrollcommand=scrollbar.set)

    frame_botoes = tk.Frame(main_window)
    frame_botoes.pack(pady=10)

    btn_listar = tk.Button(frame_botoes, text='Listar Itens', command=listar_itens)
    btn_listar.pack()

    btn_limpar = tk.Button(frame_botoes, text='Limpar Campos', command=limpar_campos)
    btn_limpar.pack()

    root.protocol('WM_DELETE_WINDOW', root.quit)
    main_window.protocol('WM_DELETE_WINDOW', root.quit)

# Criação da janela raiz
root = tk.Tk()
root.title('Login')
root.geometry('300x150')

btn_login = tk.Button(root, text='Login', command=login)
btn_login.pack(pady=50)

root.mainloop()
