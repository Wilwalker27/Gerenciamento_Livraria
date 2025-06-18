import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import hashlib
from PIL import Image, ImageTk
from datetime import date

# CORES E FONTES 
COR_FUNDO = "#0d1b2a"
COR_FRAME = "#1b263b"
COR_TEXTO = "#e0e1dd"
COR_BOTAO = "#415a77"
COR_BOTAO_HOVER = "#778da9"
FONTE_TITULO = ("Arial", 20, "bold")
FONTE_NORMAL = ("Arial", 12)
FONTE_LABEL = ("Arial", 10)

# --- Funções Auxiliares de Banco de Dados ---
def executar_query(query, params=(), fetch=None):
    # um helper pra facilitar a comunicação com o banco
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()
    cursor.execute(query, params)
    
    if fetch == 'fetchall':
        resultado = cursor.fetchall()
    elif fetch == 'fetchone':
        resultado = cursor.fetchone()
    else:
        resultado = None
    
    conn.commit()
    conn.close()
    return resultado


class FormularioBase(tk.Toplevel):
    # Classe base pra não repetir código de janela
    def __init__(self, root):
        super().__init__(root)
        self.geometry("600x600")
        self.configure(bg=COR_FUNDO)
        self.resizable(False, False)
        
        self.main_frame = tk.Frame(self, bg=COR_FUNDO)
        self.main_frame.pack(expand=True, fill='both', padx=40, pady=20)

    def criar_campo(self, label_texto, tipo_widget='entry', options=None):
        # Helper pra criar os campos do formulário
        frame_campo = tk.Frame(self.main_frame, bg=COR_FUNDO)
        frame_campo.pack(pady=10, fill='x')
        
        label = tk.Label(frame_campo, text=label_texto, font=FONTE_LABEL, bg=COR_FUNDO, fg=COR_TEXTO)
        label.pack(anchor='w')
        
        if tipo_widget == 'entry':
            widget = tk.Entry(frame_campo, font=FONTE_NORMAL, bg=COR_FRAME, fg=COR_TEXTO, relief='flat', insertbackground=COR_TEXTO)
            widget.pack(fill='x', ipady=8)
            return widget
        elif tipo_widget == 'combobox':
            widget = ttk.Combobox(frame_campo, font=FONTE_NORMAL, values=options, state='readonly')
            self.master.option_add('*TCombobox*Listbox.background', COR_FRAME)
            self.master.option_add('*TCombobox*Listbox.foreground', COR_TEXTO)
            self.master.option_add('*TCombobox*Listbox.selectBackground', COR_BOTAO_HOVER)
            widget.pack(fill='x', ipady=4)
            return widget

class TelaRegistrarLivro(FormularioBase):
    def __init__(self, root):
        super().__init__(root)
        self.title("Registrar Novo Livro")

        tk.Label(self.main_frame, text="REGISTRAR LIVRO", font=FONTE_TITULO, bg=COR_FUNDO, fg=COR_TEXTO).pack(pady=(0, 20))
        
        self.entry_titulo = self.criar_campo("Título")
        self.entry_autor = self.criar_campo("Autor")
        self.entry_editora = self.criar_campo("Editora")
        
        frame_ano_qtd = tk.Frame(self.main_frame, bg=COR_FUNDO)
        frame_ano_qtd.pack(fill='x', pady=10)
        
        sub_frame_ano = tk.Frame(frame_ano_qtd, bg=COR_FUNDO)
        sub_frame_ano.pack(side='left', expand=True, fill='x', padx=(0, 5))
        tk.Label(sub_frame_ano, text="Ano de publicação", font=FONTE_LABEL, bg=COR_FUNDO, fg=COR_TEXTO).pack(anchor='w')
        self.entry_ano = tk.Entry(sub_frame_ano, font=FONTE_NORMAL, bg=COR_FRAME, fg=COR_TEXTO, relief='flat', insertbackground=COR_TEXTO)
        self.entry_ano.pack(fill='x', ipady=8)

        sub_frame_qtd = tk.Frame(frame_ano_qtd, bg=COR_FUNDO)
        sub_frame_qtd.pack(side='left', expand=True, fill='x', padx=(5, 0))
        tk.Label(sub_frame_qtd, text="Quantidade", font=FONTE_LABEL, bg=COR_FUNDO, fg=COR_TEXTO).pack(anchor='w')
        self.entry_qtd = tk.Entry(sub_frame_qtd, font=FONTE_NORMAL, bg=COR_FRAME, fg=COR_TEXTO, relief='flat', insertbackground=COR_TEXTO)
        self.entry_qtd.pack(fill='x', ipady=8)
        self.entry_qtd.insert(0, '1') # default

        btn_registrar = tk.Label(self.main_frame, text="Registrar", font=("Arial", 14, "bold"), bg=COR_BOTAO, fg=COR_TEXTO, cursor="hand2")
        btn_registrar.pack(pady=30, ipady=12, fill='x')
        btn_registrar.bind("<Button-1>", self.registrar_livro)

    def registrar_livro(self, event=None):
        titulo = self.entry_titulo.get()
        autor = self.entry_autor.get()
        editora = self.entry_editora.get()
        ano = self.entry_ano.get()
        qtd_str = self.entry_qtd.get()

        if not all([titulo, autor, ano, qtd_str]):
            messagebox.showerror("Erro", "Todos os campos, exceto editora, são obrigatórios.", parent=self)
            return

        try:
            qtd = int(qtd_str)
            ano_int = int(ano)
            if qtd <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Ano e Quantidade devem ser números válidos e positivos.", parent=self)
            return

        query = "INSERT INTO livros (titulo, autor, editora, ano_publicacao, disponivel) VALUES (?, ?, ?, ?, 1)"
        try:
            for _ in range(qtd):
                executar_query(query, (titulo, autor, editora, ano_int))
            messagebox.showinfo("Sucesso", f"{qtd} cópia(s) de '{titulo}' registradas com sucesso!", parent=self)
            self.destroy()
        except Exception as e:
            messagebox.showerror("Erro de Banco de Dados", f"Ocorreu um erro: {e}", parent=self)

class TelaRegistrarEmprestimo(FormularioBase):
    def __init__(self, root):
        super().__init__(root)
        self.title("Registrar Novo Empréstimo")
        
        tk.Label(self.main_frame, text="REGISTRAR EMPRÉSTIMO", font=FONTE_TITULO, bg=COR_FUNDO, fg=COR_TEXTO).pack(pady=(0, 20))

        livros_disponiveis = [item[0] for item in executar_query("SELECT titulo FROM livros WHERE disponivel = 1 ORDER BY titulo", fetch='fetchall')]
        leitores = [item[0] for item in executar_query("SELECT nome_completo FROM leitores ORDER BY nome_completo", fetch='fetchall')]
        
        self.combo_titulo = self.criar_campo("Título", 'combobox', livros_disponiveis)
        self.combo_leitor = self.criar_campo("Leitor", 'combobox', leitores)

        # Datas
        hoje = date.today().strftime('%d/%m/%Y')
        self.entry_data_emprestimo = self.criar_campo("Data do empréstimo")
        self.entry_data_emprestimo.insert(0, hoje)
        self.entry_data_devolucao = self.criar_campo("Data da Devolução (prevista)")
        
        btn_registrar = tk.Label(self.main_frame, text="Registrar", font=("Arial", 14, "bold"), bg=COR_BOTAO, fg=COR_TEXTO, cursor="hand2")
        btn_registrar.pack(pady=30, ipady=12, fill='x')
        btn_registrar.bind("<Button-1>", self.registrar_emprestimo)

    def registrar_emprestimo(self, event=None):
        titulo = self.combo_titulo.get()
        leitor = self.combo_leitor.get()
        data_emp = self.entry_data_emprestimo.get()
        data_dev = self.entry_data_devolucao.get()

        if not all([titulo, leitor, data_emp, data_dev]):
            messagebox.showerror("Erro", "Todos os campos são obrigatórios.", parent=self)
            return
        
        try:
            # Pega o primeiro livro disponível com esse título
            livro_id = executar_query("SELECT id FROM livros WHERE titulo = ? AND disponivel = 1 LIMIT 1", (titulo,), fetch='fetchone')[0]
            leitor_id = executar_query("SELECT id FROM leitores WHERE nome_completo = ?", (leitor,), fetch='fetchone')[0]
            
            # Atualiza o livro para indisponível
            executar_query("UPDATE livros SET disponivel = 0 WHERE id = ?", (livro_id,))
            
            # Insere o empréstimo
            query_emprestimo = "INSERT INTO emprestimos (livro_id, leitor_id, data_emprestimo, data_devolucao, status) VALUES (?, ?, ?, ?, 'emprestado')"
            executar_query(query_emprestimo, (livro_id, leitor_id, data_emp, data_dev))
            
            messagebox.showinfo("Sucesso", "Empréstimo registrado!", parent=self)
            self.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível registrar o empréstimo. Verifique os dados. Erro: {e}", parent=self)

class TelaRegistrarDevolucao(FormularioBase):
    def __init__(self, root):
        super().__init__(root)
        self.title("Registrar Devolução")
        
        tk.Label(self.main_frame, text="REGISTRAR DEVOLUÇÃO", font=FONTE_TITULO, bg=COR_FUNDO, fg=COR_TEXTO).pack(pady=(0, 20))

        leitores_com_emprestimo = [item[0] for item in executar_query("SELECT DISTINCT l.nome_completo FROM leitores l JOIN emprestimos e ON l.id = e.leitor_id WHERE e.status = 'emprestado' ORDER BY l.nome_completo", fetch='fetchall')]
        
        self.combo_leitor = self.criar_campo("Leitor", 'combobox', leitores_com_emprestimo)
        self.combo_leitor.bind("<<ComboboxSelected>>", self.atualizar_livros_emprestados)
        
        self.combo_titulo = self.criar_campo("Título", 'combobox', [])
        
        self.entry_danos = self.criar_campo("Danos ao livro (opcional)")
        
        btn_registrar = tk.Label(self.main_frame, text="Registrar Devolução", font=("Arial", 14, "bold"), bg=COR_BOTAO, fg=COR_TEXTO, cursor="hand2")
        btn_registrar.pack(pady=30, ipady=12, fill='x')
        btn_registrar.bind("<Button-1>", self.registrar_devolucao)
        
    def atualizar_livros_emprestados(self, event=None):
        leitor_nome = self.combo_leitor.get()
        if not leitor_nome: return
        
        query = """
            SELECT li.titulo FROM livros li
            JOIN emprestimos e ON li.id = e.livro_id
            JOIN leitores le ON le.id = e.leitor_id
            WHERE le.nome_completo = ? AND e.status = 'emprestado'
        """
        livros_emprestados = [item[0] for item in executar_query(query, (leitor_nome,), fetch='fetchall')]
        self.combo_titulo['values'] = livros_emprestados
        if livros_emprestados:
            self.combo_titulo.set(livros_emprestados[0])

    def registrar_devolucao(self, event=None):
        titulo = self.combo_titulo.get()
        leitor = self.combo_leitor.get()
        danos = self.entry_danos.get()
        data_hoje = date.today().strftime('%d/%m/%Y')
        
        if not all([titulo, leitor]):
            messagebox.showerror("Erro", "Leitor e Título são obrigatórios.", parent=self)
            return
            
        try:
            # Pega o ID do empréstimo em aberto
            query_id = """
                SELECT e.id, e.livro_id FROM emprestimos e
                JOIN leitores le ON e.leitor_id = le.id
                JOIN livros li ON e.livro_id = li.id
                WHERE le.nome_completo = ? AND li.titulo = ? AND e.status = 'emprestado'
                LIMIT 1
            """
            emprestimo_id, livro_id = executar_query(query_id, (leitor, titulo), fetch='fetchone')
            
            # Atualiza o status do empréstimo
            executar_query("UPDATE emprestimos SET status = 'devolvido', data_devolucao = ?, observacoes = ? WHERE id = ?", (data_hoje, danos, emprestimo_id))
            
            # Atualiza o livro para disponível
            executar_query("UPDATE livros SET disponivel = 1 WHERE id = ?", (livro_id,))
            
            messagebox.showinfo("Sucesso", "Devolução registrada!", parent=self)
            self.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível registrar a devolução. Erro: {e}", parent=self)

# TELA PARA CADASTRAR LEITOR
class TelaCadastrarLeitor(FormularioBase):
    def __init__(self, root):
        super().__init__(root)
        self.title("Cadastrar Novo Leitor")

        tk.Label(self.main_frame, text="CADASTRAR LEITOR", font=FONTE_TITULO, bg=COR_FUNDO, fg=COR_TEXTO).pack(pady=(0, 20))
        
        self.entry_nome = self.criar_campo("Nome")
        self.entry_endereco = self.criar_campo("Endereço")
        self.entry_telefone = self.criar_campo("Telefone")
        self.entry_email = self.criar_campo("Email")

        btn_registrar = tk.Label(self.main_frame, text="Registrar", font=("Arial", 14, "bold"), bg=COR_BOTAO, fg=COR_TEXTO, cursor="hand2")
        btn_registrar.pack(pady=30, ipady=12, fill='x')
        btn_registrar.bind("<Button-1>", self.registrar_leitor)

    def registrar_leitor(self, event=None):
        nome = self.entry_nome.get()
        endereco = self.entry_endereco.get()
        telefone = self.entry_telefone.get()
        email = self.entry_email.get()

        if not nome:
            messagebox.showerror("Erro de Cadastro", "O campo 'Nome' é obrigatório.", parent=self)
            return

        try:
            query = "INSERT INTO leitores (nome_completo, endereco, telefone, email) VALUES (?, ?, ?, ?)"
            executar_query(query, (nome, endereco, telefone, email))
            messagebox.showinfo("Sucesso", f"Leitor '{nome}' cadastrado com sucesso!", parent=self)
            self.destroy() # Fecha a janela de cadastro
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Já existe um leitor com este nome.", parent=self)
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao cadastrar o leitor: {e}", parent=self)


# --- Classes das Janelas de Gerenciamento ---
class TelaGerenciarLeitores(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.title("Gerenciar Leitores")
        self.geometry("950x600")
        self.configure(bg=COR_FUNDO)
        self.resizable(True, True) # Permite redimensionar

        # Configura o redimensionamento
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Frame de busca
        frame_busca = tk.Frame(self, bg=COR_FUNDO)
        frame_busca.grid(row=0, column=0, pady=20, padx=20, sticky="ew")
        frame_busca.grid_columnconfigure(1, weight=1)
        # ... (widgets de busca sem alterações) ...
        tk.Label(frame_busca, text="Pesquise por um Leitor:", font=FONTE_NORMAL, bg=COR_FUNDO, fg=COR_TEXTO).grid(row=0, column=0, padx=(0, 10))
        self.entry_busca = tk.Entry(frame_busca, font=FONTE_NORMAL, width=40, bg=COR_FRAME, fg=COR_TEXTO, relief='flat', insertbackground=COR_TEXTO)
        self.entry_busca.grid(row=0, column=1, sticky="ew", ipady=5)
        self.entry_busca.bind("<KeyRelease>", self.buscar_leitor)

        # Tabela de Leitores
        frame_tabela = tk.Frame(self, bg=COR_FUNDO)
        frame_tabela.grid(row=1, column=0, pady=10, padx=20, sticky="nsew")
        frame_tabela.grid_rowconfigure(0, weight=1)
        frame_tabela.grid_columnconfigure(0, weight=1)

        # ... (código de estilo da tabela sem alterações) ...
        style = ttk.Style()
        style.theme_use("default")
        # ... (o resto do estilo continua igual) ...

        self.tabela = ttk.Treeview(frame_tabela, columns=('nome', 'telefone', 'endereco', 'email'), show='tree headings')
        self.tabela.column("#0", width=0, stretch=tk.NO)
        
        # --- AJUSTE: Centralizando todos os cabeçalhos e alguns dados ---
        self.tabela.heading('nome', text='Nome', anchor='center')
        self.tabela.heading('telefone', text='Telefone', anchor='center')
        self.tabela.heading('endereco', text='Endereço', anchor='center')
        self.tabela.heading('email', text='Email', anchor='center')

        self.tabela.column('nome', width=250, anchor='center') # Centralizado
        self.tabela.column('telefone', width=150, anchor='center') # Centralizado
        self.tabela.column('endereco', width=300)
        self.tabela.column('email', width=250)
        
        self.tabela.grid(row=0, column=0, sticky="nsew")
        self.popular_tabela_leitores()

        # Frame para os botões inferiores
        frame_botoes = tk.Frame(self, bg=COR_FUNDO)
        frame_botoes.grid(row=2, column=0, pady=20)
        
        btn_cadastrar = tk.Label(frame_botoes, text="Cadastrar leitor", font=("Arial", 14, "bold"), bg=COR_BOTAO, fg=COR_TEXTO, cursor="hand2")
        btn_cadastrar.pack(side='left', ipady=12, ipadx=20, padx=10)
        btn_cadastrar.bind("<Button-1>", self.abrir_cadastro_leitor)

        # --- NOVO: Botão de Relatório ---
        btn_relatorio = tk.Label(frame_botoes, text="Emitir Relatório", font=("Arial", 14, "bold"), bg="#2a9d8f", fg=COR_TEXTO, cursor="hand2")
        btn_relatorio.pack(side='left', ipady=12, ipadx=20, padx=10)
        btn_relatorio.bind("<Button-1>", self.emitir_relatorio)

    def popular_tabela_leitores(self, query=None):
        # Limpa a tabela
        for row in self.tabela.get_children():
            self.tabela.delete(row)

        if query:
            sql = "SELECT nome_completo, telefone, endereco, email FROM leitores WHERE nome_completo LIKE ? ORDER BY nome_completo"
            params = (f'%{query}%',)
        else:
            sql = "SELECT nome_completo, telefone, endereco, email FROM leitores ORDER BY nome_completo"
            params = ()
            
        leitores = executar_query(sql, params, fetch='fetchall')
        
        for leitor in leitores:
            self.tabela.insert('', 'end', values=leitor)

    def buscar_leitor(self, event=None):
        query = self.entry_busca.get()
        self.popular_tabela_leitores(query)

    def abrir_cadastro_leitor(self, event=None):
        # Abre a janela de cadastro
        janela_cadastro = TelaCadastrarLeitor(self)
        # Faz a janela principal esperar pela de cadastro
        self.wait_window(janela_cadastro)
        # Atualiza a tabela depois que a janela de cadastro for fechada
        self.popular_tabela_leitores()
        
        # AQUI O NOME JA DIZ 
    def emitir_relatorio(self, event=None):
        query = """
            SELECT DISTINCT le.nome_completo, le.telefone
            FROM leitores le
            JOIN emprestimos e ON le.id = e.leitor_id
            WHERE e.status = 'emprestado'
            ORDER BY le.nome_completo;
        """
        leitores_com_pendencias = executar_query(query, fetch='fetchall')

        # Cria uma nova janela para exibir o relatório
        janela_relatorio = tk.Toplevel(self)
        janela_relatorio.title("Relatório de Leitores com Empréstimos")
        janela_relatorio.geometry("500x400")
        janela_relatorio.configure(bg=COR_FUNDO)

        tk.Label(janela_relatorio, text="Leitores com Empréstimos Ativos", font=("Arial", 16, "bold"), bg=COR_FUNDO, fg=COR_TEXTO).pack(pady=10)

        texto_relatorio = tk.Text(janela_relatorio, bg=COR_FRAME, fg=COR_TEXTO, font=FONTE_NORMAL, relief='flat', height=15, width=60)
        texto_relatorio.pack(pady=10, padx=10)

        if not leitores_com_pendencias:
            texto_relatorio.insert('1.0', "Nenhum leitor com empréstimos ativos no momento.")
        else:
            relatorio_str = "Nome do Leitor\t\t\tTelefone\n"
            relatorio_str += "="*50 + "\n"
            for nome, telefone in leitores_com_pendencias:
                relatorio_str += f"{nome}\t\t\t{telefone}\n"
            
            texto_relatorio.insert('1.0', relatorio_str)
        
        texto_relatorio.config(state='disabled') # Torna o texto somente leitura
# --- FUNÇÕES DE ABERTURA DE JANELAS ---
def abrir_tela_registro_livro(root):
    TelaRegistrarLivro(root)

def abrir_tela_registro_emprestimo(root):
    TelaRegistrarEmprestimo(root)

def abrir_tela_registro_devolucao(root):
    TelaRegistrarDevolucao(root)

def abrir_gerenciar_leitores(root):
    TelaGerenciarLeitores(root)

class TelaAdmin:
    def __init__(self, root, usuario):
        self.root = root
        self.root.title("Painel Administrativo")
        self.root.geometry("800x600")
        self.root.configure(bg=COR_FUNDO)

        main_frame = tk.Frame(root, bg=COR_FUNDO)
        main_frame.pack(expand=True)

        label_titulo = tk.Label(main_frame, text=f"OLÁ, {usuario.upper()}", font=FONTE_TITULO, bg=COR_FUNDO, fg=COR_TEXTO)
        label_titulo.pack(pady=(0, 50))
        
        botoes_frame = tk.Frame(main_frame, bg=COR_FUNDO)
        botoes_frame.pack()

        # O comando agora passa o 'root' da janela admin para a nova tela
        botoes_info = [
            ("Registrar Livros", lambda: abrir_tela_registro_livro(self.root)),
            ("Registrar Empréstimo", lambda: abrir_tela_registro_emprestimo(self.root)),
            ("Registrar Devolução", lambda: abrir_tela_registro_devolucao(self.root)),
            ("Gerenciar Leitores", lambda: abrir_gerenciar_leitores(self.root))
        ]

        for texto, comando in botoes_info:
            btn = tk.Label(botoes_frame, text=texto, font=("Arial", 14), width=25, bg=COR_BOTAO, fg=COR_TEXTO, cursor="hand2")
            btn.pack(pady=10, ipady=15, ipadx=10)
            btn.bind("<Button-1>", lambda e, cmd=comando: cmd())
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=COR_BOTAO_HOVER))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=COR_BOTAO))

class TelaPrincipal:
    def __init__(self, root, usuario):
        self.root = root
        self.usuario_logado = usuario
        self.root.title(f"Biblioteca Saber Mais")
        self.root.geometry("800x650") # Aumentei um pouco a altura
        self.root.configure(bg=COR_FUNDO)

        # Configura o redimensionamento da janela
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        label_boas_vindas = tk.Label(self.root, text=f"Bem-vindo(a), {self.usuario_logado}!", font=("Arial", 16), bg=COR_FUNDO, fg=COR_TEXTO)
        label_boas_vindas.grid(row=0, column=0, pady=(20, 10), padx=20, sticky="n")

        frame_busca = tk.Frame(self.root, bg=COR_FUNDO)
        frame_busca.grid(row=1, column=0, pady=10, padx=20, sticky="ew")
        frame_busca.grid_columnconfigure(1, weight=1)
        # ... (widgets de busca sem alterações) ...
        tk.Label(frame_busca, text="Pesquise por um livro:", font=FONTE_NORMAL, bg=COR_FUNDO, fg=COR_TEXTO).grid(row=0, column=0, padx=(0, 10))
        self.entry_busca = tk.Entry(frame_busca, font=FONTE_NORMAL, width=40, bg=COR_FRAME, fg=COR_TEXTO, relief='flat', insertbackground=COR_TEXTO)
        self.entry_busca.grid(row=0, column=1, sticky="ew", ipady=5)
        self.entry_busca.bind("<KeyRelease>", self.buscar_livro)
        
        frame_tabela = tk.Frame(self.root, bg=COR_FUNDO)
        frame_tabela.grid(row=2, column=0, pady=10, padx=20, sticky="nsew")
        frame_tabela.grid_rowconfigure(0, weight=1)
        frame_tabela.grid_columnconfigure(0, weight=1)

        # ... (código de estilo da tabela sem alterações) ...
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=COR_FRAME, foreground=COR_TEXTO, fieldbackground=COR_FRAME, rowheight=25, font=FONTE_NORMAL)
        style.configure("Treeview.Heading", background=COR_BOTAO, foreground=COR_TEXTO, font=("Arial", 12, "bold"), relief="flat")
        style.map("Treeview", background=[('selected', COR_BOTAO_HOVER)])
        style.map("Treeview.Heading", background=[('active', COR_BOTAO)])

        self.tabela = ttk.Treeview(frame_tabela, columns=('titulo', 'autor', 'estoque'), show='tree headings')
        self.tabela.column("#0", width=0, stretch=tk.NO)
        self.tabela.heading('titulo', text='Título', anchor='center')
        self.tabela.heading('autor', text='Autor', anchor='center')
        self.tabela.heading('estoque', text='Estoque', anchor='center')
        self.tabela.column('titulo', width=400)
        self.tabela.column('autor', width=200)
        self.tabela.column('estoque', width=100, anchor='center')
        self.tabela.grid(row=0, column=0, sticky="nsew")
        
        # --- NOVO: Evento de duplo-clique para reserva ---
        self.tabela.bind("<Double-1>", self.reservar_livro)
        
        self.popular_tabela()

        # --- NOVO: Botão de Logout ---
        btn_logout = tk.Label(self.root, text="Sair (Logout)", font=("Arial", 11, "underline"), bg=COR_FUNDO, fg="lightblue", cursor="hand2")
        btn_logout.grid(row=3, column=0, pady=(10, 20), sticky="s")
        btn_logout.bind("<Button-1>", self.fazer_logout)

    def popular_tabela(self, query=None):
        for row in self.tabela.get_children():
            self.tabela.delete(row)
        
        if query:
            sql = "SELECT titulo, autor, disponivel FROM livros WHERE titulo LIKE ? OR autor LIKE ? ORDER BY titulo"
            params = (f'%{query}%', f'%{query}%')
        else:
            sql = "SELECT titulo, autor, disponivel FROM livros ORDER BY titulo"
            params = ()
            
        livros = executar_query(sql, params, fetch='fetchall')
        
        for row in livros:
            titulo, autor, disponivel = row
            estoque = "Disponível" if disponivel else "Emprestado"
            self.tabela.insert('', 'end', values=(titulo, autor, estoque))

    def buscar_livro(self, event=None):
        query = self.entry_busca.get()
        self.popular_tabela(query)
    
    def reservar_livro(self, event=None):
        # Pega o item selecionado
        selecionado = self.tabela.selection()
        if not selecionado:
            return # Sai da função se nada for selecionado

        item = self.tabela.item(selecionado[0])
        titulo, autor, status = item['values']
        
        if status == 'Emprestado':
            messagebox.showwarning("Indisponível", f"O livro '{titulo}' já está emprestado e não pode ser reservado.", parent=self.root)
            return
            
        # Pergunta ao usuário se quer reservar
        resposta = messagebox.askyesno("Confirmar Reserva", f"Deseja fazer uma reserva para o livro:\n\n{titulo}\n({autor})?", parent=self.root)
        
        if resposta:
            # Aqui entraria a lógica real de reserva no banco de dados
            messagebox.showinfo("Sucesso", f"Reserva para '{titulo}' realizada com sucesso!\n\n(Obs: Esta é uma função de exemplo.)", parent=self.root)

    def fazer_logout(self, event=None):
        self.root.destroy() # Fecha a janela atual
        # Recria a janela de login e reinicia o loop principal
        root_login = tk.Tk()
        app = TelaLogin(root_login)
        root_login.mainloop()

class TelaLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("Biblioteca Saber Mais - Login")
        self.root.geometry("400x600")
        self.root.configure(bg=COR_FUNDO)
        self.root.resizable(False, False)
        
        largura_tela = root.winfo_screenwidth()
        altura_tela = root.winfo_screenheight()
        pos_x = (largura_tela // 2) - (400 // 2)
        pos_y = (altura_tela // 2) - (600 // 2)
        self.root.geometry(f"400x600+{pos_x}+{pos_y}")

        main_frame = tk.Frame(root, bg=COR_FUNDO)
        main_frame.pack(expand=True, padx=30)

        try:
            # ATUALIZADO AQUI
            img = Image.open("livro.png")
            img = img.resize((120, 120), Image.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(img)
            label_imagem = tk.Label(main_frame, image=self.logo_img, bg=COR_FUNDO)
            label_imagem.pack(pady=(0, 20))
        except FileNotFoundError:
            label_imagem = tk.Label(main_frame, text="[IMAGEM 'livro.png' NÃO ENCONTRADA]", bg=COR_FUNDO, fg="red")
            label_imagem.pack(pady=(0, 20))
        # ... o resto do __init__ continua igual
        label_titulo = tk.Label(main_frame, text="Biblioteca Saber Mais", font=FONTE_TITULO, bg=COR_FUNDO, fg=COR_TEXTO)
        label_titulo.pack(pady=(0, 40))
        label_login = tk.Label(main_frame, text="LOGIN", font=FONTE_LABEL, bg=COR_FUNDO, fg=COR_TEXTO)
        label_login.pack(pady=(0, 5), anchor="w")
        frame_login = tk.Frame(main_frame, background=COR_FRAME, bd=0)
        frame_login.pack(pady=(0, 15), fill='x')
        self.entry_login = tk.Entry(frame_login, font=FONTE_NORMAL, width=25, relief="flat", bg=COR_FRAME, fg=COR_TEXTO, insertbackground=COR_TEXTO, highlightthickness=0, bd=0)
        self.entry_login.pack(padx=10, pady=10, fill='x')
        label_senha = tk.Label(main_frame, text="SENHA", font=FONTE_LABEL, bg=COR_FUNDO, fg=COR_TEXTO)
        label_senha.pack(pady=(10, 5), anchor="w")
        frame_senha = tk.Frame(main_frame, background=COR_FRAME, bd=0)
        frame_senha.pack(pady=(0, 20), fill='x')
        self.entry_senha = tk.Entry(frame_senha, show="*", font=FONTE_NORMAL, width=25, relief="flat", bg=COR_FRAME, fg=COR_TEXTO, insertbackground=COR_TEXTO, highlightthickness=0, bd=0)
        self.entry_senha.pack(padx=10, pady=10, fill='x')
        self.btn_login_label = tk.Label(main_frame, text="Log in", font=("Arial", 12, "bold"), bg=COR_BOTAO, fg=COR_TEXTO, cursor="hand2")
        self.btn_login_label.pack(pady=10, ipady=12, fill='x')
        self.btn_login_label.bind("<Button-1>", lambda event: self.verificar_login())
        self.btn_login_label.bind("<Enter>", self.on_enter)
        self.btn_login_label.bind("<Leave>", self.on_leave)
        link_senha = tk.Label(main_frame, text="Esqueceu a senha?", font=("Arial", 10, "underline"), bg=COR_FUNDO, fg=COR_TEXTO, cursor="hand2")
        link_senha.pack(pady=20)


    def on_enter(self, event):
        self.btn_login_label.config(bg=COR_BOTAO_HOVER)

    def on_leave(self, event):
        self.btn_login_label.config(bg=COR_BOTAO)

    def verificar_login(self):
        login = self.entry_login.get()
        senha = self.entry_senha.get()
        if not login or not senha:
            messagebox.showerror("Erro de Login", "Por favor, preencha todos os campos.")
            return

        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        resultado = executar_query("SELECT role FROM usuarios WHERE login = ? AND senha = ?", (login, senha_hash), fetch='fetchone')

        if resultado:
            role = resultado[0]
            self.root.destroy()
            nova_janela_root = tk.Tk()
            if role == 'admin':
                TelaAdmin(nova_janela_root, login)
            else:
                TelaPrincipal(nova_janela_root, login)
            nova_janela_root.mainloop()
        else:
            messagebox.showerror("Erro de Login", "Login ou senha incorretos.")

# --- INICIA A APLICAÇÃO ---
if __name__ == "__main__":
    root_login = tk.Tk()
    app = TelaLogin(root_login)
    root_login.mainloop()