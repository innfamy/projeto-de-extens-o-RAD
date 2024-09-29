import sqlite3


class Database:
    def __init__(self, db_name="doacoes.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.criar_tabelas()

    def criar_tabelas(self):
        # Criar tabela de itens de doação
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS item_doacao (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                data_doacao TEXT NOT NULL,
                                tipo TEXT NOT NULL
                              )''')

        # Criar tabela de roupas
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS roupas (
                                item_id INTEGER,
                                tipo_roupa TEXT NOT NULL,
                                tamanho TEXT NOT NULL,
                                cor TEXT NOT NULL,
                                condicao TEXT NOT NULL,
                                FOREIGN KEY(item_id) REFERENCES item_doacao(id) ON DELETE CASCADE
                              )''')

        # Criar tabela de alimentos
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS alimentos (
                                item_id INTEGER,
                                tipo_alimento TEXT NOT NULL,
                                data_validade TEXT NOT NULL,
                                FOREIGN KEY(item_id) REFERENCES item_doacao(id) ON DELETE CASCADE
                              )''')
        self.conn.commit()

    def adicionar_item_doacao(self, data_doacao, tipo):
        self.cursor.execute("INSERT INTO item_doacao (data_doacao, tipo) VALUES (?, ?)", (data_doacao, tipo))
        self.conn.commit()
        return self.cursor.lastrowid

    def adicionar_roupa(self, item_id, tipo_roupa, tamanho, cor, condicao):
        self.cursor.execute("INSERT INTO roupas (item_id, tipo_roupa, tamanho, cor, condicao) VALUES (?, ?, ?, ?, ?)",
                            (item_id, tipo_roupa, tamanho, cor, condicao))
        self.conn.commit()

    def adicionar_alimento(self, item_id, tipo_alimento, data_validade):
        self.cursor.execute("INSERT INTO alimentos (item_id, tipo_alimento, data_validade) VALUES (?, ?, ?)",
                            (item_id, tipo_alimento, data_validade))
        self.conn.commit()

    def buscar_doacoes(self):
        self.cursor.execute('''
            SELECT item_doacao.id, item_doacao.data_doacao, item_doacao.tipo,
                   roupas.tipo_roupa, roupas.tamanho, roupas.cor, roupas.condicao,
                   alimentos.tipo_alimento, alimentos.data_validade
            FROM item_doacao
            LEFT JOIN roupas ON item_doacao.id = roupas.item_id
            LEFT JOIN alimentos ON item_doacao.id = alimentos.item_id
        ''')
        return self.cursor.fetchall()

    # Função para atualizar uma doação de roupa
    def atualizar_roupa(self, item_id, data_doacao, tipo_roupa, tamanho, cor, condicao):
        self.cursor.execute("UPDATE item_doacao SET data_doacao = ?, tipo = 'Roupas' WHERE id = ?",
                            (data_doacao, item_id))
        self.cursor.execute('''
            UPDATE roupas SET tipo_roupa = ?, tamanho = ?, cor = ?, condicao = ?
            WHERE item_id = ?
        ''', (tipo_roupa, tamanho, cor, condicao, item_id))
        self.conn.commit()

    # Função para atualizar uma doação de alimento
    def atualizar_alimento(self, item_id, data_doacao, tipo_alimento, data_validade):
        self.cursor.execute("UPDATE item_doacao SET data_doacao = ?, tipo = 'Alimentos' WHERE id = ?",
                            (data_doacao, item_id))
        self.cursor.execute('''
            UPDATE alimentos SET tipo_alimento = ?, data_validade = ?
            WHERE item_id = ?
        ''', (tipo_alimento, data_validade, item_id))
        self.conn.commit()

    # Função para deletar um item de doação, seja roupa ou alimento
    def deletar_item(self, item_id):
        self.cursor.execute("DELETE FROM item_doacao WHERE id = ?", (item_id,))
        self.conn.commit()

    def fechar_conexao(self):
        self.conn.close()
