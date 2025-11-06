import sqlite3
from datetime import date

conn = sqlite3.connect("game_database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Jogadores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    data_criacao TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Personagens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    classe TEXT,
    nivel INTEGER,
    jogador_id INTEGER,
    FOREIGN KEY (jogador_id) REFERENCES Jogadores(id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Itens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    tipo TEXT,
    valor INTEGER
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Inventario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    personagem_id INTEGER,
    item_id INTEGER,
    quantidade INTEGER,
    FOREIGN KEY (personagem_id) REFERENCES Personagens(id),
    FOREIGN KEY (item_id) REFERENCES Itens(id)
);
""")

conn.commit()

cursor.executemany("""
INSERT INTO Jogadores (name, email, data_criacao)
VALUES (?, ?, ?)
""", [
    ("João", "jaozinnxy@gmail.com", "20-11-2004"),
    ("Junior", "subzer@gmail.com", "20-12-2000"),
    ("Maria", "untrix@gmail.com", "22-05-2009")
])

cursor.executemany("""
INSERT INTO Personagens (nome, classe, nivel, jogador_id)
VALUES (?, ?, ?, ?)
""", [
    ("Horman", "Guerreiro", 10, 1),
    ("Lornam", "Mago", 5, 2),
    ("Trix", "Arqueiro", 10, 3)
])

cursor.executemany("""
INSERT INTO Itens (nome, objeto, valor )
VALUES (?, ?, ?)
""", [
    ("Espada Lendária", "armadura", 2000),
    ("Cura", "Poção", 750),
    ("Arco de Fogo", "arma", 500),
    ("Armadura de Cristal", "Armadura", 3000),
    ("Aumento de Força", "poção", 950)
])

cursor.executemany("""
INSERT INTO Inventario (personagem_id, item_id, quantidade)
VALUES (?, ?, ?)
""", [
    (1, 1, 1),
    (2, 2, 3),
    (3, 3, 1),
])

conn.commit()


def lista_de_jogadores():
    print("\nLista de todos os jogadores:")
    for lista in cursor.execute("SELECT id, name, email, data_criacao FROM Jogadores;"):
        print(lista)

def jogadores_com_arqueiro():
    print("\nJogadores de personagens com a classe 'Arqueiro':")
    query = """
    SELECT DISTINCT j.name
    FROM Jogadores j
    JOIN Personagens p ON j.id = p.jogador_id
    WHERE p.classe = 'Arqueiro';
    """
    for row in cursor.execute(query):
        print(row[0])

def item_mais_valioso():
    print("\nItem mais valioso do jogo:")
    query = "SELECT nome, valor FROM Itens ORDER BY valor DESC LIMIT 1;"
    result = cursor.execute(query).fetchone()
    if result:
        print(f"{result[0]} - Valor: {result[1]}")
    else:
        print("Nenhum item encontrado.")


lista_de_jogadores()
jogadores_com_arqueiro()
item_mais_valioso()

conn.close()