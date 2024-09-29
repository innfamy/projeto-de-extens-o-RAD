import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry  # Biblioteca para escolher datas
from database import Database

# Inicializa o objeto do banco de dados
db = Database()


# Função para adicionar uma nova doação
def adicionar_doacao():
    data = data_doacao_entry.get()
    tipo = tipo_combobox.get()

    if tipo == 'Roupas':
        tipo_roupa = tipo_roupa_entry.get()
        tamanho = tamanho_entry.get()
        cor = cor_entry.get()
        condicao = condicao_entry.get()

        item_id = db.adicionar_item_doacao(data, tipo)
        db.adicionar_roupa(item_id, tipo_roupa, tamanho, cor, condicao)

    elif tipo == 'Alimentos':
        tipo_alimento = tipo_alimento_entry.get()
        data_validade = data_validade_entry.get()

        item_id = db.adicionar_item_doacao(data, tipo)
        db.adicionar_alimento(item_id, tipo_alimento, data_validade)

    listar_doacoes_geral()


# Função para listar apenas roupas
def listar_roupas():
    # Limpa o treeview
    for row in treeview.get_children():
        treeview.delete(row)

    # Busca e adiciona roupas ao treeview
    roupas = db.buscar_doacoes()
    for item in roupas:
        if item[2] == 'Roupas':  # O índice 2 corresponde ao tipo
            treeview.insert('', 'end', values=(item[0], item[1], item[3], item[4], item[5], item[6],))
            treeview["columns"] = ("id", "data_doacao", "tipo_roupa", "tamanho", "cor", "condicao")
            treeview.heading("id", text="ID")
            treeview.heading("data_doacao", text="Data de Doação")
            treeview.heading("tipo_roupa", text="Tipo de Roupa")
            treeview.heading("tamanho", text="Tamanho")
            treeview.heading("cor", text="Cor")
            treeview.heading("condicao", text="Condição")

            # Ajustar a largura das colunas para roupas
            treeview.column("id", width=50, anchor='center')
            treeview.column("data_doacao", width=100, anchor='center')
            treeview.column("tipo_roupa", width=100, anchor='center')
            treeview.column("tamanho", width=70, anchor='center')
            treeview.column("cor", width=70, anchor='center')
            treeview.column("condicao", width=100, anchor='center')


# Função para listar apenas alimentos
def listar_alimentos():
    # Limpa o treeview
    for row in treeview.get_children():
        treeview.delete(row)

    # Busca e adiciona alimentos ao treeview
    alimentos = db.buscar_doacoes()
    for item in alimentos:
        if item[2] == 'Alimentos':  # O índice 2 corresponde ao tipo
            treeview.insert('', 'end', values=(item[0], item[1], item[7], item[8]))
            treeview["columns"] = ("id", "data_doacao", "tipo_alimento", "data_validade")
            treeview.heading("id", text="ID")
            treeview.heading("data_doacao", text="Data de Doação")
            treeview.heading("tipo_alimento", text="Tipo de Alimento")
            treeview.heading("data_validade", text="Data Validade")

            # Ajustar a largura das colunas para alimentos
            treeview.column("id", width=50, anchor='center')
            treeview.column("data_doacao", width=100, anchor='center')
            treeview.column("tipo_alimento", width=100, anchor='center')
            treeview.column("data_validade", width=100, anchor='center')


# Função para listar todas as doações de forma geral
def listar_doacoes_geral():
    # Limpar o Treeview antes de inserir novos dados
    for item in treeview.get_children():
        treeview.delete(item)

    # Buscar todas as doações do banco de dados
    doacoes = db.buscar_doacoes()

    # Inserir os dados no Treeview
    for doacao in doacoes:
        treeview.insert("", "end", values=doacao)

    # Definir as colunas, incluindo todos os campos
    treeview["columns"] = (
        "id", "data_doacao", "tipo", "tipo_roupa", "tamanho", "cor", "condicao", "tipo_alimento", "data_validade")

    # Configurar os cabeçalhos das colunas
    treeview.heading("id", text="ID")
    treeview.heading("data_doacao", text="Data de Doação")
    treeview.heading("tipo", text="Tipo")
    treeview.heading("tipo_roupa", text="Tipo de Roupa")
    treeview.heading("tamanho", text="Tamanho")
    treeview.heading("cor", text="Cor")
    treeview.heading("condicao", text="Condição")
    treeview.heading("tipo_alimento", text="Tipo de Alimento")
    treeview.heading("data_validade", text="Data Validade")

    # Ajustar a largura das colunas
    treeview.column("id", width=20, anchor='center')
    treeview.column("tipo", width=50, anchor='center')
    treeview.column("data_doacao", width=50, anchor='center')
    treeview.column("tipo_alimento", width=50, anchor='center')
    treeview.column("data_validade", width=50, anchor='center')
    treeview.column("tipo_roupa", width=50, anchor='center')
    treeview.column("tamanho", width=50, anchor='center')
    treeview.column("cor", width=50, anchor='center')
    treeview.column("condicao", width=50, anchor='center')


# Função para selecionar um item do Treeview
def selecionar_item(event):
    try:
        item_selecionado = treeview.selection()[0]
        valores = treeview.item(item_selecionado, "values")

        # Carregar os valores nos campos de entrada
        data_doacao_entry.set_date(valores[1])
        tipo_combobox.set("Roupas" if valores[2] else "Alimentos")

        if valores[2]:  # Se é roupa
            tipo_roupa_entry.delete(0, tk.END)
            tipo_roupa_entry.insert(tk.END, valores[2])
            tamanho_entry.delete(0, tk.END)
            tamanho_entry.insert(tk.END, valores[3])
            cor_entry.delete(0, tk.END)
            cor_entry.insert(tk.END, valores[4])
            condicao_entry.delete(0, tk.END)
            condicao_entry.insert(tk.END, valores[5])

            roupa_frame.grid(row=3, column=0, padx=10, pady=10)
            alimento_frame.grid_forget()

        else:  # Se é alimento
            tipo_alimento_entry.delete(0, tk.END)
            tipo_alimento_entry.insert(tk.END, valores[6])
            data_validade_entry.set_date(valores[7])

            alimento_frame.grid(row=3, column=0, padx=10, pady=10)
            roupa_frame.grid_forget()

        global current_item_id
        current_item_id = valores[0]

    except IndexError:
        pass


# Função para editar uma doação
def editar_doacao():
    data = data_doacao_entry.get()
    tipo = tipo_combobox.get()

    if tipo == 'Roupas':
        tipo_roupa = tipo_roupa_entry.get()
        tamanho = tamanho_entry.get()
        cor = cor_entry.get()
        condicao = condicao_entry.get()

        db.atualizar_roupa(current_item_id, data, tipo_roupa, tamanho, cor, condicao)

    elif tipo == 'Alimentos':
        tipo_alimento = tipo_alimento_entry.get()
        data_validade = data_validade_entry.get()

        db.atualizar_alimento(current_item_id, data, tipo_alimento, data_validade)

    listar_doacoes_geral()


# Função para excluir uma doação
def excluir_doacao():
    if current_item_id:
        db.deletar_item(current_item_id)
        listar_doacoes_geral()
        messagebox.showinfo("Sucesso", "Doação excluída com sucesso!")


# Criar a interface Tkinter
root = tk.Tk()
root.title("Sistema de Doações")
root.geometry("1000x600")

# Iniciar a janela maximizada
root.state('zoomed')
root.grid_columnconfigure(1, weight=3)

# Elementos da UI
botoes = tk.Frame(root)
botoes.grid(row=0, column=0, padx=10, pady=50)

botoes_inciais = tk.Frame(botoes)
botoes_inciais.grid(row=1, column=0, padx=10, pady=10, sticky="W")

tk.Label(botoes_inciais, text="Data da Doação:").grid(row=1, column=0, padx=10, pady=10, sticky="W")
data_doacao_entry = DateEntry(botoes_inciais, width=20)
data_doacao_entry.grid(row=1, column=1, padx=10, pady=10, sticky="W")
tk.Label(botoes_inciais, text="Tipo de Item:").grid(row=0, column=0, padx=10, pady=10, sticky="W")
tipo_combobox = ttk.Combobox(botoes_inciais, values=["Roupas", "Alimentos"])
tipo_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="W")

# Campos específicos para roupas
roupa_frame = tk.Frame(botoes)
tk.Label(roupa_frame, text="Tipo de Roupa:").grid(row=0, column=0, padx=10, pady=10, sticky="W")
tipo_roupa_entry = tk.Entry(roupa_frame)
tipo_roupa_entry.grid(row=0, column=1, padx=10, pady=10, sticky="W")

tk.Label(roupa_frame, text="Tamanho:").grid(row=1, column=0, padx=10, pady=10, sticky="W")
tamanho_entry = tk.Entry(roupa_frame)
tamanho_entry.grid(row=1, column=1, padx=10, pady=10, sticky="W")

tk.Label(roupa_frame, text="Cor:").grid(row=2, column=0, padx=10, pady=10, sticky="W")
cor_entry = tk.Entry(roupa_frame)
cor_entry.grid(row=2, column=1, padx=10, pady=10, sticky="W")

tk.Label(roupa_frame, text="Condição:").grid(row=3, column=0, padx=10, pady=10, sticky="W")
condicao_entry = tk.Entry(roupa_frame)
condicao_entry.grid(row=3, column=1, padx=10, pady=10, sticky="W")

# Campos específicos para alimentos
alimento_frame = tk.Frame(botoes)
tk.Label(alimento_frame, text="Tipo de Alimento:").grid(row=0, column=0, padx=10, pady=10, sticky="nw")
tipo_alimento_entry = tk.Entry(alimento_frame)
tipo_alimento_entry.grid(row=0, column=1, padx=10, pady=10, sticky="nw")

tk.Label(alimento_frame, text="Data de Validade:").grid(row=1, column=0, padx=10, pady=10, sticky="W")
data_validade_entry = DateEntry(alimento_frame, width=20, sticky="W")
data_validade_entry.grid(row=1, column=1, padx=10, pady=10, sticky="W")


# Mostrar o frame correto com base na seleção
def mostrar_frame(event):
    if tipo_combobox.get() == "Roupas":
        alimento_frame.grid_forget()
        roupa_frame.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    elif tipo_combobox.get() == "Alimentos":
        roupa_frame.grid_forget()
        alimento_frame.grid(row=2, column=0, padx=10, pady=10, sticky="w")


tipo_combobox.bind("<<ComboboxSelected>>", mostrar_frame)

botoes_sql = tk.Frame(botoes)
botoes_sql.grid(row=3, column=0, padx=10, pady=10)

# Botões para adicionar, editar e excluir doação
tk.Button(botoes_sql, text="Adicionar Item", command=adicionar_doacao).grid(row=0, column=0, padx=10, pady=10)
tk.Button(botoes_sql, text="Editar Item", command=editar_doacao).grid(row=0, column=1, padx=10, pady=10)
tk.Button(botoes_sql, text="Excluir Item", command=excluir_doacao).grid(row=0, column=2, padx=10, pady=10)

botoes_planilha = tk.Frame(root)
botoes_planilha.grid(row=1, column=1, padx=350, columnspan=3, sticky="ew")

# Botões para listar tipos de doações
tk.Button(botoes_planilha, text="Mostrar Apenas Roupas", command=listar_roupas).grid(row=0, column=0, padx=10, pady=10,
                                                                                     sticky="w")
tk.Button(botoes_planilha, text="Mostrar Apenas Alimentos", command=listar_alimentos).grid(row=0, column=1, padx=10,
                                                                                           pady=10)
tk.Button(botoes_planilha, text="Mostrar Todos", command=listar_doacoes_geral).grid(row=0, column=2, padx=10, pady=10,
                                                                                    sticky="e")

# Tabela para exibir doações
treeview = ttk.Treeview(root, columns=(
    "id", "data_doacao", "tipo_roupa", "tamanho", "cor", "condicao", "tipo_alimento", "data_validade"), show='headings')
treeview.grid(row=0, column=1, padx=100, pady=50, columnspan=3, sticky="ew")

treeview.heading("id", text="ID")
treeview.heading("data_doacao", text="Data")
treeview.heading("tipo_roupa", text="Tipo de Roupa")
treeview.heading("tamanho", text="Tamanho")
treeview.heading("cor", text="Cor")
treeview.heading("condicao", text="Condição")
treeview.heading("tipo_alimento", text="Tipo de Alimento")
treeview.heading("data_validade", text="Data Validade")

# Bind para selecionar o item ao clicar
treeview.bind('<ButtonRelease-1>', selecionar_item)

# Iniciar exibindo todos os itens
listar_doacoes_geral()

# Iniciar a aplicação
root.mainloop()

# Fechar a conexão com o banco de dados ao finalizar
db.fechar_conexao()
