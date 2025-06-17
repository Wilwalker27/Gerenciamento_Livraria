# 📚 Sistema de Gerenciamento de Biblioteca "Saber Mais"

✨ Um sistema desktop simples e elegante para gerenciar o acervo, os leitores e os empréstimos da sua biblioteca 
comunitária. ✨

<br>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.12-blue.svg" alt="Python 3.12">
  <img src="https://img.shields.io/badge/database-SQLite3-orange.svg" alt="SQLite3">
  <img src="https://img.shields.io/badge/status-concluído-green.svg" alt="Status: Concluído">
  <img src="https://img.shields.io/badge/licença-MIT-lightgrey.svg" alt="Licença MIT">
</p>

---

### 📋 Sumário
* [Sobre o Projeto](#-sobre-o-projeto)
* [🎯 Funcionalidades](#-funcionalidades)
* [🛠️ Tecnologias Utilizadas](#️-tecnologias-utilizadas)
* [🚀 Como Executar o Projeto](#-como-executar-o-projeto)
* [💡 Melhorias Futuras](#-melhorias-futuras)
* [✒️ Autor](#️-autor)

---

### 📖 Sobre o Projeto

O **Saber Mais** nasceu da necessidade de modernizar a gestão da Biblioteca Comunitária "Saber Livre", 
substituindo os antigos cadernos de registro por uma solução digital robusta e intuitiva. 💻

O sistema foi desenvolvido pensando nos voluntários da biblioteca, oferecendo uma interface limpa, de fácil 
aprendizado e com todas as ferramentas necessárias para o dia a dia: controle de livros, gerenciamento de leitores 
e um sistema completo para empréstimos e devoluções. Tudo isso em uma aplicação desktop leve e que não requer 
conexão com a internet para funcionar.

---

### 🎯 Funcionalidades

- ✅ **Autenticação Segura:** Sistema de login com 2 níveis de acesso (Administrador e Voluntário).
- ✅ **Painel de Administrador Completo:**
    - 📕 Cadastro de novos livros e múltiplas cópias.
    - 🧑‍🤝‍🧑 Gerenciamento de leitores (cadastrar, listar e buscar).
    - 📤 Registro de empréstimos de forma inteligente com menus dropdown.
    - 📥 Registro de devoluções com anotação de danos.
- ✅ **Painel do Voluntário:**
    - 🔍 Interface focada na consulta rápida de livros.
    - ⚡ Busca em tempo real por título ou autor.
- ✅ **Interface Gráfica Moderna:** Design limpo e agradável, pensado na experiência do usuário.
- ✅ **Banco de Dados Local:** Utiliza SQLite para portabilidade total, sem necessidade de instalar um servidor de 
banco de dados.

---

### 🛠️ Tecnologias Utilizadas

Este projeto foi construído com as seguintes ferramentas:

- 🐍 **Python 3.12:** A linguagem de programação principal.
- 🎨 **Tkinter:** Biblioteca nativa do Python para a construção da interface gráfica.
- 🗃️ **SQLite 3:** Banco de dados embarcado para armazenamento local de todos os dados.
- 🖼️ **Pillow:** Biblioteca para manipulação e exibição de imagens na interface.

---

### 🚀 Como Executar o Projeto

Este é um guia detalhado para você instalar e rodar a aplicação na sua máquina. Um deploy de respeito!

#### **1. Pré-requisitos**

Antes de começar, garanta que você tenha o **Python 3** instalado.

- Você pode baixar a versão mais recente em [python.org](https://www.python.org/downloads/).

#### **2. Passo a Passo da Instalação**

1.  **Clone este repositório** (ou baixe o ZIP e extraia):
    ```bash
    git clone 
[https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
    ```

2.  **Navegue até a pasta do projeto:**
    ```bash
    cd nome-da-pasta-do-projeto
    ```

3.  **Crie um Ambiente Virtual (Boa Prática):**
    Isso isola as dependências do projeto e mantém sua máquina organizada.
    
    * No macOS ou Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    * No Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

4.  **Crie o arquivo `requirements.txt`:**
    Na pasta do projeto, crie um arquivo com este nome e adicione o seguinte conteúdo. Ele informa ao `pip` qual 
biblioteca externa precisamos instalar.
    ```txt
    Pillow
    ```

5.  **Instale as Dependências:**
    Com o ambiente virtual ativado, execute o comando abaixo.
    ```bash
    pip install -r requirements.txt
    ```

6.  **Configure o Banco de Dados:**
    Este passo é crucial! O script `database.py` cria o arquivo de banco de dados e insere todos os dados de 
exemplo. Execute-o **uma única vez**.
    ```bash
    python database.py
    ```

7.  **Execute a Aplicação! 🎉**
    Tudo pronto! Agora é só iniciar o programa.
    ```bash
    python app.py
    ```

    - **Login Admin:** `admin` / `admin`
    - **Login Voluntário:** `voluntario` / `1234`

---

### 💡 Melhorias Futuras

O projeto tem uma base sólida e pode ser expandido com novas funcionalidades, como:

- [ ] Módulo de relatórios (livros mais emprestados, etc.).
- [ ] Sistema de notificação por e-mail para devoluções atrasadas.
- [ ] Funcionalidades de edição e exclusão de registros.
- [ ] Migração para uma plataforma web (Flask ou Django) para acesso remoto.

---

### ✒️ Autor

Feito com ❤️ por **Wiliaml Rigne**.

