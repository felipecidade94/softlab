# SoftLab 🎓💻

SoftLab é um protótipo para o cadastro de alunos e gerenciamento de projetos em laboratórios makers. Este projeto foi desenvolvido para ajudar a organizar e administrar alunos e seus projetos, fornecendo uma interface gráfica amigável e funcionalidades essenciais.

## Funcionalidades 🚀

- **Autenticação e Sessões**:
  - Login e logout para administradores e alunos.
  - Validação de credenciais para acessar diferentes funcionalidades com base no tipo de usuário.

- **Gerenciamento de Alunos**:
  - Registro de novos alunos.
  - Listagem de alunos cadastrados.
  - Filtragem de alunos por instituição.
  - Alteração e remoção de dados de alunos.
  - Recuperação de senha dos alunos (sem envio de email).

- **Gerenciamento de Projetos**:
  - Adição de novos projetos para alunos.
  - Listagem de projetos de um aluno específico.
  - Exibição de informações detalhadas dos projetos, incluindo materiais utilizados.
  - Remoção de projetos cadastrados.

- **Banco de Dados**:
  - Utilização de SQLite para armazenar informações dos alunos e projetos.
  - Estrutura de tabelas para `alunos`, `projetos` e `materiais`.
  - Funções de inserção, atualização, remoção e consulta no banco de dados.

- **Interface Gráfica**:
  - Utilização de `Tkinter` para criar uma interface de usuário amigável.
  - Diferentes janelas e frames para cada funcionalidade.
  - Botões e entradas de texto para interação com o usuário.

- **Música de Fundo**:
  - Utilização do `pygame` para tocar música de fundo no aplicativo.
  - Controle de play/pause da música através de botões na interface.

## Limitações ⚠️

- Não há funcionalidade de envio de emails para recuperação de senhas.
- A música de fundo e a imagem do logo devem estar no mesmo diretório do código para que o aplicativo funcione corretamente.
- A música deve ter o nome **Contato.mp3**.
- A imagem do logo deve ser chamada **Logo.png**.

## Bibliotecas Utilizadas 📚

- **Tkinter**: Biblioteca padrão do Python para a criação de interfaces gráficas. Já vem instalada com o Python.
  - Importação:
    ```python
    import tkinter as tk
    from tkinter import Tk, Label, ttk, messagebox, simpledialog, Entry, Button, Toplevel
    ```

- **Pillow (PIL)**: Biblioteca para manipulação de imagens.
  - Instalação:
    ```bash
    pip install Pillow
    ```
  - Importação:
    ```python
    from PIL import ImageTk, Image
    ```

- **SQLite3**: Biblioteca padrão do Python para banco de dados SQLite.
  - Instalação: Não é necessária, já vem instalada com o Python.
  - Importação:
    ```python
    import sqlite3
    ```

- **Pygame**: Biblioteca para criação de jogos e manipulação de multimídia, utilizada aqui para tocar música.
  - Instalação:
    ```bash
    pip install pygame
    ```
  - Importação:
    ```python
    import pygame
    ```

- **Datetime**: Biblioteca padrão do Python para manipulação de datas e horários.
  - Instalação: Não é necessária, já vem instalada com o Python.
  - Importação:
    ```python
    from datetime import datetime
    ```

## Instalação ⚙️

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/felipecidade94/softlab
   ```

2. **Crie um ambiente virtual (opcional, mas recomendado):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   .\venv\Scripts\activate  # Windows
   ```

