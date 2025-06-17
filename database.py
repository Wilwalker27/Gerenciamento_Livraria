# Arquivo: database.py (versão 4 - Completa)

import sqlite3
import hashlib
import random # Usaremos para variar a disponibilidade dos livros

def criar_banco():
    """
    Cria e configura o banco de dados inicial e todas as tabelas necessárias.
    Este script deve ser executado uma única vez ou sempre que o banco de dados
    precisar ser recriado do zero.
    """
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()

    # --- Tabela de usuários ---
    # Armazena quem pode acessar o sistema (admin ou voluntário)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin', 'voluntario'))
        )
    ''')

    # --- Tabela de livros ---
    # Armazena todos os livros da biblioteca
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            editora TEXT,
            ano_publicacao INTEGER,
            disponivel BOOLEAN NOT NULL CHECK(disponivel IN (0, 1))
        )
    ''')

    # --- Tabela de leitores ---
    # Armazena os dados dos membros da biblioteca que pegam livros emprestados
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leitores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_completo TEXT NOT NULL,
            telefone TEXT,
            endereco TEXT
        )
    ''')

    # --- Tabela de empréstimos ---
    # Registra o histórico de todos os empréstimos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emprestimos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            livro_id INTEGER NOT NULL,
            leitor_id INTEGER NOT NULL,
            data_emprestimo DATE NOT NULL,
            data_devolucao DATE,
            status TEXT NOT NULL CHECK(status IN ('emprestado', 'devolvido')),
            observacoes TEXT, -- NOVA COLUNA
            FOREIGN KEY (livro_id) REFERENCES livros(id),
            FOREIGN KEY (leitor_id) REFERENCES leitores(id)
        )
    ''')


    # --- INSERÇÃO DE DADOS DE EXEMPLO (APENAS SE AS TABELAS ESTIVEREM VAZIAS) ---

    # Insere usuários iniciais
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        print("Criando usuários iniciais...")
        admin_senha = hashlib.sha256('admin'.encode()).hexdigest()
        voluntario_senha = hashlib.sha256('1234'.encode()).hexdigest()
        usuarios_iniciais = [('admin', admin_senha, 'admin'), ('voluntario', voluntario_senha, 'voluntario')]
        cursor.executemany('INSERT INTO usuarios (login, senha, role) VALUES (?, ?, ?)', usuarios_iniciais)
        print("Usuários 'admin' (senha: admin) e 'voluntario' (senha: 1234) criados.")

    # Insere a lista de 50 livros famosos
    cursor.execute("SELECT COUNT(*) FROM livros")
    if cursor.fetchone()[0] == 0:
        print("Inserindo lista de 50 livros famosos...")
        livros_famosos = [
            ('Dom Quixote', 'Miguel de Cervantes', 'Editora Fictícia', 1605, 1),
            ('O Senhor dos Anéis', 'J.R.R. Tolkien', 'Editora Fictícia', 1954, 1),
            ('O Pequeno Príncipe', 'Antoine de Saint-Exupéry', 'Editora Fictícia', 1943, 0),
            ('Cem Anos de Solidão', 'Gabriel García Márquez', 'Editora Fictícia', 1967, 1),
            ('1984', 'George Orwell', 'Editora Fictícia', 1949, 1),
            ('O Apanhador no Campo de Centeio', 'J.D. Salinger', 'Editora Fictícia', 1951, 1),
            ('A Metamorfose', 'Franz Kafka', 'Editora Fictícia', 1915, 1),
            ('Guerra e Paz', 'Liev Tolstói', 'Editora Fictícia', 1869, 0),
            ('O Grande Gatsby', 'F. Scott Fitzgerald', 'Editora Fictícia', 1925, 1),
            ('Ulisses', 'James Joyce', 'Editora Fictícia', 1922, 1),
            ('A Divina Comédia', 'Dante Alighieri', 'Editora Fictícia', 1320, 1),
            ('Moby Dick', 'Herman Melville', 'Editora Fictícia', 1851, 1),
            ('O Processo', 'Franz Kafka', 'Editora Fictícia', 1925, 1),
            ('Crime e Castigo', 'Fiódor Dostoiévski', 'Editora Fictícia', 1866, 1),
            ('Orgulho e Preconceito', 'Jane Austen', 'Editora Fictícia', 1813, 0),
            ('O Morro dos Ventos Uivantes', 'Emily Brontë', 'Editora Fictícia', 1847, 1),
            ('Frankenstein', 'Mary Shelley', 'Editora Fictícia', 1818, 1),
            ('Admirável Mundo Novo', 'Aldous Huxley', 'Editora Fictícia', 1932, 1),
            ('A Revolução dos Bichos', 'George Orwell', 'Editora Fictícia', 1945, 1),
            ('O Sol é para Todos', 'Harper Lee', 'Editora Fictícia', 1960, 1),
            ('As Vinhas da Ira', 'John Steinbeck', 'Editora Fictícia', 1939, 1),
            ('O Som e a Fúria', 'William Faulkner', 'Editora Fictícia', 1929, 0),
            ('Em Busca do Tempo Perdido', 'Marcel Proust', 'Editora Fictícia', 1913, 1),
            ('A Montanha Mágica', 'Thomas Mann', 'Editora Fictícia', 1924, 1),
            ('Os Miseráveis', 'Victor Hugo', 'Editora Fictícia', 1862, 1),
            ('O Conde de Monte Cristo', 'Alexandre Dumas', 'Editora Fictícia', 1844, 1),
            ('Anna Karenina', 'Liev Tolstói', 'Editora Fictícia', 1877, 1),
            ('Madame Bovary', 'Gustave Flaubert', 'Editora Fictícia', 1856, 1),
            ('Drácula', 'Bram Stoker', 'Editora Fictícia', 1897, 1),
            ('O Retrato de Dorian Gray', 'Oscar Wilde', 'Editora Fictícia', 1890, 1),
            ('Ilíada', 'Homero', 'Editora Fictícia', -800, 1),
            ('Odisseia', 'Homero', 'Editora Fictícia', -800, 1),
            ('Eneida', 'Virgílio', 'Editora Fictícia', -19, 0),
            ('O Príncipe', 'Nicolau Maquiavel', 'Editora Fictícia', 1532, 1),
            ('Utopia', 'Thomas More', 'Editora Fictícia', 1516, 1),
            ('Leviatã', 'Thomas Hobbes', 'Editora Fictícia', 1651, 1),
            ('O Contrato Social', 'Jean-Jacques Rousseau', 'Editora Fictícia', 1762, 1),
            ('A Riqueza das Nações', 'Adam Smith', 'Editora Fictícia', 1776, 1),
            ('A Origem das Espécies', 'Charles Darwin', 'Editora Fictícia', 1859, 1),
            ('Dom Casmurro', 'Machado de Assis', 'Editora Fictícia', 1899, 1),
            ('Memórias Póstumas de Brás Cubas', 'Machado de Assis', 'Editora Fictícia', 1881, 1),
            ('Grande Sertão: Veredas', 'João Guimarães Rosa', 'Editora Fictícia', 1956, 0),
            ('Vidas Secas', 'Graciliano Ramos', 'Editora Fictícia', 1938, 1),
            ('A Hora da Estrela', 'Clarice Lispector', 'Editora Fictícia', 1977, 1),
            ('O Cortiço', 'Aluísio Azevedo', 'Editora Fictícia', 1890, 1),
            ('Capitães da Areia', 'Jorge Amado', 'Editora Fictícia', 1937, 1),
            ('O Guarani', 'José de Alencar', 'Editora Fictícia', 1857, 1),
            ('Macunaíma', 'Mário de Andrade', 'Editora Fictícia', 1928, 1),
            ('Fahrenheit 451', 'Ray Bradbury', 'Editora Fictícia', 1953, 1),
            ('O Nome da Rosa', 'Umberto Eco', 'Editora Fictícia', 1980, 0)
        ]
        livros_com_status = [(t, a, e, ano, random.choice([1, 1, 1, 0])) for t, a, e, ano, s in livros_famosos]
        cursor.executemany('INSERT INTO livros (titulo, autor, editora, ano_publicacao, disponivel) VALUES (?, ?, ?, ?, ?)', livros_com_status)
        print(f"{len(livros_com_status)} livros de exemplo inseridos.")

    # Insere um leitor de exemplo
    cursor.execute("SELECT COUNT(*) FROM leitores")
    if cursor.fetchone()[0] == 0:
        print("Inserindo leitor de exemplo...")
        cursor.execute("INSERT INTO leitores (nome_completo, telefone, endereco) VALUES (?, ?, ?)",
                       ('João da Silva Leitor', '71999998888', 'Rua das Flores, 123'))
        print("Leitor de exemplo inserido.")


    # Salva as alterações e fecha a conexão
    conn.commit()
    conn.close()
    print("\nBanco de dados 'biblioteca.db' verificado e pronto para uso.")


if __name__ == '__main__':
    criar_banco()