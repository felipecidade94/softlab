import tkinter as tk
from tkinter import Tk, Label, ttk, messagebox, simpledialog, Entry, Button, Toplevel
from PIL import ImageTk, Image
import sqlite3
import pygame
from datetime import datetime
class SoftLab:
    def __init__(self):
        self.nome_banco_dados = "softlab.db"
        self.conexao = sqlite3.connect(self.nome_banco_dados)
        self.cursor = self.conexao.cursor()
        self.janela_principal = Tk()
        self.configurar_banco_dados()
        self.configurar_interface()
        self.login_aluno_ativo = False
        self.login_adm_ativo = False
        self.tocando_musica = True
        self.play_pause = "PAUSE" if self.tocando_musica == True else "PLAY"
        pygame.mixer.init()
        self.tocar_musica()
        self.janela_principal.mainloop()
        
    def configurar_banco_dados(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS alunos (
                                matricula INTEGER PRIMARY KEY,
                                nome TEXT,
                                instituicao TEXT,
                                idade INTEGER,
                                email TEXT,
                                sexo TEXT,
                                senha TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS projetos (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                matricula TEXT,
                                nome TEXT,
                                descricao TEXT,
                                FOREIGN KEY (matricula) REFERENCES alunos (matricula))''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS materiais (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                id_projeto INTEGER,
                                material TEXT,
                                FOREIGN KEY (id_projeto) REFERENCES projetos (id))''')
        self.conexao.commit()
        
    def configurar_interface(self):
        style = ttk.Style()
        style.configure("TButton", padding=1, font=("Arial", 15), foreground="black", background='#add8e6')
        style.configure('TLabel',  padding=10, font=('Arial', 20, 'bold'))
        self.janela_principal.title("SOFTLAB")
        self.janela_principal.geometry("480x780")
        logo_imagem = Image.open("Logo.png")
        logo_imagem = logo_imagem.resize((77, 85))
        self.logo_imagem = ImageTk.PhotoImage(logo_imagem)
        logo_label = Label(self.janela_principal, image=self.logo_imagem)
        logo_label.pack()
        frame = ttk.Frame(self.janela_principal)
        frame.pack(padx=0, pady=0)
        ttk.Button(frame, text="FAZER LOGIN COMO ADMINISTRADOR", command=self.abrir_login_adm, width=40).grid(row=0, column=0, pady=3)
        ttk.Button(frame, text="REGISTRE-SE", command=self.abrir_registrar, width=40).grid(row=1, column=0, pady=3)
        ttk.Button(frame, text="LISTAR ALUNOS", command=self.listar_alunos, width=40).grid(row=2, column=0, pady=0)
        ttk.Button(frame, text="LISTAR ALUNOS POR INSTITUIÇÃO", command=self.abrir_listar_alunos_por_instituicao, width=40).grid(row=3, column=0, pady=3)
        ttk.Button(frame, text="FAZER LOGIN COMO ALUNO", command=self.abrir_login_aluno, width=40).grid(row=4, column=0, pady=3)
        ttk.Button(frame, text='INFORMAÇÕES DO ALUNO', command=self.informacoes_aluno, width=40).grid(row=5, column=0, pady=3)
        ttk.Button(frame, text="ESQUECEU A SENHA?", command=self.abrir_esquecer_senha_aluno, width=40).grid(row=6, column=0, pady=3)
        ttk.Button(frame, text="ADICIONAR PROJETO", command=self.abrir_novo_projeto, width=40).grid(row=7, column=0, pady=3)
        ttk.Button(frame, text="LISTAR PROJETOS DO ALUNO", command=self.listar_projetos_aluno, width=40).grid(row=8, column=0, pady=3)
        ttk.Button(frame, text="INFORMAÇÕES DOS PROJETOS", command=self.informacoes_projetos, width=40).grid(row=9, column=0, pady=3)
        ttk.Button(frame, text="REMOVER PROJETO", command=self.abrir_remover_projeto, width=40).grid(row=10, column=0, pady=3)
        ttk.Button(frame, text="ALTERAR DADOS DO ALUNO", command=self.abrir_alterar_dados, width=40).grid(row=11, column=0, pady=3)
        ttk.Button(frame, text="REMOVER ALUNO", command=self.remover_aluno, width=40).grid(row=12, column=0, pady=3)
        ttk.Button(frame, text="LIMPAR BANCO DE DADOS", command=self.limpar_banco_de_dados, width=40).grid(row=13, column=0, pady=3)
        ttk.Button(frame, text="FAZER LOGOUT", command=self.fazer_logout, width=40).grid(row=14, column=0, pady=3)
        self.botao_play_pause = ttk.Button(frame, text="PAUSAR MÚSICA", command=self.alternar_musica, width=40)
        self.botao_play_pause.grid(row=15, column=0, pady=3)
        ttk.Button(frame, text="SAIR", command=self.sair, width=40).grid(row=16, column=0, pady=3)
        Label(self.janela_principal, text="Por Felipe Cidade Soares e Ivy Oliveira dos Reis\nhttps://github.com/felipecidade94/softlab", font=("Arial", 10), fg="blue").pack()
        
    def abrir_registrar(self):
        if not self.login_adm_ativo and not self.login_aluno_ativo:
            self.nova_janela = Toplevel(self.janela_principal)
            self.nova_janela.title("Formulário de Registro")
            self.nova_janela.geometry("200x500")
            self.widgets_registrar(self.nova_janela)
        else:
            messagebox.showerror('ERRO', 'Faça logout para registrar um aluno!')
            
    def widgets_registrar(self, janela):
        dias= [dia for dia in range(1, 32)]
        meses = [mes for mes in range(1, 13)]
        anos = [ano for ano in range(1980, datetime.now().year + 1)]
        label_instituicao = Label(janela, text="Instituição:", font=("Arial", 10, "bold"))
        label_instituicao.pack()
        self.entry_instituicao = Entry(janela)
        self.entry_instituicao.pack(padx=5, pady=5, fill=tk.X)
        label_nome = Label(janela, text="Nome:", font=("Arial", 10, "bold"))
        label_nome.pack()
        self.entry_nome = Entry(janela)
        self.entry_nome.pack(padx=5, pady=5, fill=tk.X)
        label_email = Label(janela, text="Email:", font=("Arial", 10, "bold"))
        label_email.pack()
        self.entry_email = Entry(janela)
        self.entry_email.pack(padx=5, pady=5, fill=tk.X)
        label_matricula = Label(janela, text="Matrícula:", font=("Arial", 10, "bold"))
        label_matricula.pack()
        self.entry_matricula = Entry(janela)
        self.entry_matricula.pack(padx=5, pady=5, fill=tk.X)
        label_idade = tk.Label(janela, text="Idade:", font=("Arial", 10, "bold"))
        label_idade.pack() 
        frame_idade_labels = tk.Frame(janela)
        frame_idade_labels.pack(padx=5, pady=5)
        frame_idade_entries = tk.Frame(janela)
        frame_idade_entries.pack(padx=5, pady=5, fill=tk.X)
        label_dia = tk.Label(frame_idade_labels, text="Dia", width=5, anchor='center')
        label_dia.pack(side="left", padx=5)
        label_mes = tk.Label(frame_idade_labels, text="Mês", width=8, anchor='center')
        label_mes.pack(side="left", padx=5)
        label_ano = tk.Label(frame_idade_labels, text="Ano", width=5, anchor='center')
        label_ano.pack(side="left", padx=5)
        self.combo_dia = ttk.Combobox(frame_idade_entries, values=dias, width=5)
        self.combo_dia.pack(side="left", padx=5)
        self.combo_mes = ttk.Combobox(frame_idade_entries, values=meses, width=5)
        self.combo_mes.pack(side="left", padx=5)
        self.combo_ano = ttk.Combobox(frame_idade_entries, values=anos, width=8)
        self.combo_ano.pack(side="left", padx=5)
        label_sexo = Label(janela, text="Sexo:", font=("Arial", 10, "bold"))
        label_sexo.pack()
        self.combo_sexo = ttk.Combobox(janela, values=["Masculino", "Feminino", "Outro"])
        self.combo_sexo.pack(padx=5, pady=5, fill=tk.X)
        label_senha = Label(janela, text="Senha:", font=("Arial", 10, "bold"))
        label_senha.pack()
        self.entry_senha = Entry(janela,show="*")
        self.entry_senha.pack(padx=5, pady=5, fill=tk.X)
        label_confirmar_senha = Label(janela, text="Confirmar Senha:", font=("Arial", 10, "bold"))
        label_confirmar_senha.pack()
        self.entry_confirmar_senha = Entry(janela,show="*")
        self.entry_confirmar_senha.pack(padx=5, pady=5, fill=tk.X)
        botao_registrar = Button(janela, text="Registrar", command=self.registrar)
        botao_registrar.pack(pady=10)
        
    def registrar(self):
        instituicao = self.entry_instituicao.get().strip().upper()
        nome = self.entry_nome.get().title().strip()
        matricula = self.entry_matricula.get().strip()
        email = self.entry_email.get().strip()
        sexo = self.combo_sexo.get().strip()
        senha = self.entry_senha.get().strip()
        confirmar_senha = self.entry_confirmar_senha.get().strip()
        if instituicao and nome and matricula and self.combo_dia.get() and self.combo_mes.get() and self.combo_ano.get() and sexo and email and senha and confirmar_senha:
            if not matricula.isnumeric():
                messagebox.showerror("ERRO", "A matricula deve ser um inteiro!")
                self.nova_janela.destroy()
            elif not nome.replace(' ', '').isalpha():
                messagebox.showerror("ERRO", "O nome deve conter apenas letras!")
                self.nova_janela.destroy()
            else:
                if senha != confirmar_senha:
                    messagebox.showerror("ERRO", "As senhas devem ser iguais!")
                    self.nova_janela.destroy()
                else:
                    try:
                        idade = self.calcular_idade(self.combo_dia.get(), self.combo_mes.get(), self.combo_ano.get())
                    except ValueError:
                        messagebox.showerror("ERRO", "Data de nascimento inválida!")
                        self.nova_janela.destroy()
                    self.cursor.execute("INSERT INTO alunos (instituicao, matricula, nome, idade, sexo, email, senha) VALUES (?, ?, ?, ?, ?, ?, ?)", (instituicao, matricula, nome, idade, sexo, email, senha))
                    self.conexao.commit()
                    messagebox.showinfo("SUCESSO", "Aluno cadastrado com sucesso!")
                    self.nova_janela.destroy()
        else:
            messagebox.showerror("ERRO", "Todos os campos devem ser preenchidos!")

    def calcular_idade(self, dia, mes, ano):
        data_nascimento = datetime(int(ano), int(mes), int(dia))
        data_atual = datetime.now()
        idade = data_atual.year - data_nascimento.year - ((data_atual.month, data_atual.day) < (data_nascimento.month, data_nascimento.day))
        return idade

    def listar_alunos(self):
        if self.login_adm_ativo:
            if self.tem_cadastro():
                self.cursor.execute("SELECT matricula, nome, instituicao FROM alunos ORDER BY nome")
                alunos = "\n".join([f"{nome} | Matrícula: {matricula} | Instituição: {instituicao}" for matricula, nome, instituicao in self.cursor.fetchall()])
                messagebox.showinfo("ALUNOS CADASTRADOS", alunos)
            else:
                messagebox.showerror('ERRO', 'Não há nenhum aluno cadastrado!')
        else:
            messagebox.showerror('ERRO', 'Não é possível listar alunos sem fazer login como administrador!')

    def widget_listar_alunos_por_instituicao(self, janela):
        label_instituicao = Label(janela, text="Instituição:", font=("Arial", 10, "bold"))
        label_instituicao.pack()
        self.combo_instituicao = ttk.Combobox(janela, values=self.nome_instituicoes())
        self.combo_instituicao.pack(padx=5, pady=5, fill=tk.X)
        self.botao_listar_alunos = Button(janela, text="Listar Alunos", command=self.listar_alunos_por_instituicao)
        self.botao_listar_alunos.pack(pady=10)

    def listar_alunos_por_instituicao(self):
        instituicao = self.combo_instituicao.get()
        self.cursor.execute("SELECT matricula, nome FROM alunos WHERE instituicao = ?", (instituicao,))
        alunos = "\n".join([f"{nome} | Matrícula: {matricula}" for matricula, nome in self.cursor.fetchall()])
        messagebox.showinfo("ALUNOS CADASTRADOS", alunos)
        self.nova_janela.destroy()

    def abrir_listar_alunos_por_instituicao(self):
        if self.tem_cadastro():
            if self.login_adm_ativo:
                self.nova_janela = Toplevel(self.janela_principal)
                self.nova_janela.title("Listar Alunos por Instituição")
                self.widget_listar_alunos_por_instituicao(self.nova_janela)
            else:
                messagebox.showerror('ERRO', 'Não é possível listar alunos sem fazer login como administrador!')
        else:
            messagebox.showerror('ERRO', 'Não há nenhum aluno cadastrado!')

    def widgets_login_adm(self, janela):        
        label_usuario_adm = Label(janela, text="Usuário:", font=("Arial", 10, "bold"))
        label_usuario_adm.pack()
        self.entry_usuario_adm = Entry(janela)
        self.entry_usuario_adm.pack(padx=5, pady=5, fill=tk.X)
        label_senha_adm = Label(janela, text="Senha:", font=("Arial", 10, "bold"))
        label_senha_adm.pack()
        self.entry_senha_adm = Entry(janela, show="*")
        self.entry_senha_adm.pack(padx=5, pady=5, fill=tk.X)
        self.botao_login_adm = Button(janela, text="Login", command=self.fazer_login_adm)
        self.botao_login_adm.pack(pady=10)

    def fazer_login_adm(self):
        usuario = self.entry_usuario_adm.get()
        senha = self.entry_senha_adm.get()
        if not usuario or not senha:
            messagebox.showerror("ERRO", "Por favor, preencha todos os campos!")
        else:
            if usuario == self.usuario_adm() and senha == self.senha_adm():
                self.login_adm_ativo = True
                messagebox.showinfo("SUCESSO", "Login realizado com sucesso!")
                self.nova_janela.destroy()
            else:
                messagebox.showerror("ERRO", "Usuário ou senha incorretos!")
                self.nova_janela.destroy()

    def abrir_login_adm(self):
        if self.login_adm_ativo == True or self.login_aluno_ativo == True:
            messagebox.showerror('ERRO', 'Já há um usuário logado!')
        else:
            self.nova_janela = Toplevel(self.janela_principal)
            self.nova_janela.geometry("200x150")
            self.widgets_login_adm(self.nova_janela)

    def widgets_login_aluno(self, janela):
        label_instituicao_aluno = Label(janela, text="Instituição:", font=("Arial", 10, "bold"))
        label_instituicao_aluno.pack()
        self.combo_instituicao_aluno = ttk.Combobox(janela, values=self.nome_instituicoes())
        self.combo_instituicao_aluno.pack(padx=5, pady=5, fill=tk.X)
        label_matricula_aluno = Label(janela, text="Matrícula:", font=("Arial", 10, "bold"))
        label_matricula_aluno.pack()
        self.entry_matricula_aluno = Entry(janela)
        self.entry_matricula_aluno.pack(padx=5, pady=5, fill=tk.X)
        label_senha_aluno = Label(janela, text="Senha:", font=("Arial", 10, "bold"))
        label_senha_aluno.pack()
        self.entry_senha_aluno = Entry(janela, show="*")
        self.entry_senha_aluno.pack(padx=5, pady=5, fill=tk.X)
        self.botao_login_aluno = Button(janela, text="Login", command=self.fazer_login_aluno)
        self.botao_login_aluno.pack(pady=10)

    def fazer_login_aluno(self):
        # if self.login_adm_ativo or self.login_aluno_ativo:
        #     messagebox.showerror('ERRO', 'Já há um usuário logado!')
        #     return
        instituicao = self.combo_instituicao_aluno.get()
        matricula = self.entry_matricula_aluno.get()
        senha = self.entry_senha_aluno.get()
        if instituicao and matricula and senha:
            if not matricula.isnumeric():
                messagebox.showerror("ERRO", "A matricula deve ser um inteiro!")
                self.nova_janela.destroy()
            else:
                if senha == self.senha_aluno(matricula, instituicao):
                    self.login_aluno_ativo = True
                    self.usuario_logado = matricula
                    messagebox.showinfo("SUCESSO", "Login realizado com sucesso!")
                    self.nova_janela.destroy()
                else:
                    messagebox.showerror("ERRO", "Usuário ou senha incorretos!")
                    self.nova_janela.destroy()
        else:
            messagebox.showerror("ERRO", "Por favor, preencha todos os campos!")
            self.nova_janela.destroy()

    def abrir_login_aluno(self):
        if self.tem_cadastro():
            if self.login_adm_ativo or self.login_aluno_ativo:
                messagebox.showerror('ERRO', 'Já há um usuário logado!')
            else:
                self.nova_janela = Toplevel(self.janela_principal)
                self.nova_janela.geometry("200x250")
                self.widgets_login_aluno(self.nova_janela)
        else:
            messagebox.showerror('ERRO', 'Nenhum aluno cadastrado!')

    def widgets_esquecer_senha_aluno(self, janela):
        label_instituicao_aluno = Label(janela, text="Instituição:", font=("Arial", 10, "bold"))
        label_instituicao_aluno.pack()
        self.combo_instituicao_aluno = ttk.Combobox(janela, values=self.nome_instituicoes())
        self.combo_instituicao_aluno.pack(padx=5, pady=5, fill=tk.X)
        label_matricula_aluno = Label(janela, text="Matrícula:", font=("Arial", 10, "bold"))
        label_matricula_aluno.pack()
        self.entry_matricula_aluno = Entry(janela)
        self.entry_matricula_aluno.pack(padx=5, pady=5, fill=tk.X)
        self.botao_mostrar_senha_aluno = Button(janela, text="Mostrar senha", command=self.mostrar_senha_aluno)
        self.botao_mostrar_senha_aluno.pack(pady=10)
        
    def mostrar_senha_aluno(self):        
        matricula = self.entry_matricula_aluno.get()
        instituicao = self.combo_instituicao_aluno.get()
        if not matricula.isnumeric():
            messagebox.showerror("ERRO", "A matricula deve ser um inteiro!")
        else:
            try:
                messagebox.showinfo("SENHA DO ALUNO", f"Senha: {self.senha_aluno(self.entry_matricula_aluno.get(), self.combo_instituicao_aluno.get())}")
                self.nova_janela.destroy()
            except:
                messagebox.showerror("ERRO", "Matricula ou instituição incorretos!")

    def abrir_esquecer_senha_aluno(self):
        if not self.tem_cadastro():
            messagebox.showerror('ERRO', 'Nenhum aluno cadastrado!')
        else:
            if not self.login_adm_ativo:
                messagebox.showerror('ERRO', 'Faça login como administrador primeiro')
                return
            else:
                self.nova_janela = Toplevel(self.janela_principal)
                self.nova_janela.geometry("200x200")
                self.widgets_esquecer_senha_aluno(self.nova_janela)

    def informacoes_aluno(self):
        if self.tem_cadastro():
            if self.login_aluno_ativo:
                self.cursor.execute("SELECT nome,email, idade, sexo, matricula, instituicao  FROM alunos WHERE matricula = ?", (self.usuario_logado,))
                aluno = self.cursor.fetchone()
                if aluno[2]=='Masculino':
                    messagebox.showinfo("INFORMAÇOES DO ALUNO", f"Nome: {aluno[0]}\nEmail: {aluno[1]}\nIdade: {aluno[2]}\nSexo: {aluno[3]}\nMatricula: {aluno[4]}\nInstituição: {aluno[5]}")
                else:
                    messagebox.showinfo("INFORMAÇOES DO ALUNA", f"Nome: {aluno[0]}\nEmail: {aluno[1]}\nIdade: {aluno[2]}\nSexo: {aluno[3]}\nMatricula: {aluno[4]}\nInstituição: {aluno[5]}")
            else:
                messagebox.showerror('ERRO', 'Não é possível listar as informações do aluno sem estar logado como aluno!')
        else:
            messagebox.showerror('ERRO', 'Não há nenhum aluno cadastrado!')

    def widget_adicionar_projeto(self, janela):
        label_adicionar_projeto = Label(janela, text="Adicionar Projeto", font=("Arial", 10, "bold"))
        label_adicionar_projeto.pack()
        label_nome_projeto = Label(janela, text="Nome do Projeto:", font=("Arial", 10, "bold"))
        label_nome_projeto.pack()
        self.entry_nome_projeto = Entry(janela)
        self.entry_nome_projeto.pack(padx=5, pady=5, fill=tk.X)
        label_descricao = Label(janela, text="Descrição:", font=("Arial", 10, "bold"))
        label_descricao.pack()
        self.entry_descricao = Entry(janela)
        self.entry_descricao.pack(padx=5, pady=5, fill=tk.X)
        label_materiais = Label(janela, text="Materiais (separados por vírgula):", font=("Arial", 10, "bold"))
        label_materiais.pack()
        self.entry_materiais = Entry(janela)
        self.entry_materiais.pack(padx=5, pady=5, fill=tk.X)
        self.btn_adicionar_projeto = tk.Button(janela, text='ADICIONAR PROJETO', command=self.adicionar_projeto)
        self.btn_adicionar_projeto.pack(pady=10)

    def adicionar_projeto(self):
        nome_projeto = self.entry_nome_projeto.get()
        descricao = self.entry_descricao.get()
        materiais_input = self.entry_materiais.get()
        if not nome_projeto or not descricao or not materiais_input:
            messagebox.showerror('ERRO', 'Todos os campos devem ser preenchidos!')
            self.nova_janela.destroy()
        elif nome_projeto and descricao and materiais_input:
            materiais = [m.strip().capitalize() for m in materiais_input.split(',')] if materiais_input else []
            self.cursor.execute("SELECT MAX(id) FROM projetos")
            maior_id = self.cursor.fetchone()[0] or 0
            id_projeto_novo = maior_id + 1
            self.cursor.execute("INSERT INTO projetos (id, matricula, nome, descricao) VALUES (?, ?, ?, ?)", (id_projeto_novo, self.usuario_logado, nome_projeto, descricao))
            for material in materiais:
                self.cursor.execute("INSERT INTO materiais (id_projeto, material) VALUES (?, ?)", (id_projeto_novo, material))
            self.conexao.commit()
            messagebox.showinfo("SUCESSO", "Projeto adicionado com sucesso!")
            self.nova_janela.destroy()
        else:
            messagebox.showerror('ERRO', 'Projeto não adicionado!')
        self.nova_janela.destroy()

    def abrir_novo_projeto(self):
        if self.tem_cadastro():
            if self.login_aluno_ativo:
                self.nova_janela = tk.Toplevel(self.janela_principal)
                self.nova_janela.title("Adicionar Projeto")
                self.nova_janela.geometry("400x300")
                self.widget_adicionar_projeto(self.nova_janela)
            else:
                messagebox.showerror('ERRO', 'Não é possível adicionar um projeto sem estar logado como aluno!')
        else:
            messagebox.showerror('ERRO', 'Não há nenhum aluno cadastrado!')

    def listar_projetos_aluno(self):
        if self.tem_cadastro():
            if self.login_aluno_ativo:
                self.cursor.execute("SELECT id, nome FROM projetos WHERE matricula = ? ORDER BY id", (self.usuario_logado,))
                projetos = "\n".join([f"{nome}" for id, nome in self.cursor.fetchall()])
                if len(projetos) > 0:
                    messagebox.showinfo("PROJETOS DO ALUNO", projetos)
                else:
                    messagebox.showerror('ERRO', 'Não há nenhum projeto cadastrado!')
            else:
                messagebox.showerror('ERRO', 'Não é possível listar os projetos sem estar logado como aluno!')
        else:
            messagebox.showerror('ERRO', 'Não há nenhum aluno cadastrado!')

    def informacoes_projetos(self):
        if self.tem_cadastro():
            if self.login_aluno_ativo:
                self.cursor.execute("SELECT id, nome, descricao FROM projetos WHERE matricula = ?", (self.usuario_logado,))
                projetos = self.cursor.fetchall()
                if projetos:
                    infos = []
                    for id, nome, descricao in projetos:
                        self.cursor.execute("SELECT material FROM materiais WHERE id_projeto = ?", (id,))
                        materiais = "\n".join([material[0] for material in self.cursor.fetchall()]) or "Nenhum material cadastrado."
                        infos.append(f"Projeto: {nome}\nDescrição: {descricao}\nMateriais:\n{materiais}")
                    messagebox.showinfo("INFORMAÇÕES DOS PROJETOS", "\n\n".join(infos))
                else:
                    messagebox.showerror("ERRO", "Nenhum projeto encontrado.")
            else:
                messagebox.showerror('ERRO', 'Não é possível listar as informações dos projetos sem estar logado como aluno!')
        else:
            messagebox.showerror('ERRO', 'Não há nenhum aluno cadastrado!')

    def abrir_remover_projeto(self):
        if self.tem_cadastro():
            if not self.login_aluno_ativo:
                messagebox.showerror('ERRO', 'Não é possível remover projetos sem estar logado como aluno!')
            else:
                self.nova_janela = tk.Toplevel(self.janela_principal)
                self.nova_janela.title("Remover Projetos")
                self.nova_janela.geometry("300x400")
                self.widgets_remover_projeto(self.nova_janela)
        else:
            messagebox.showerror('ERRO', 'Não há nenhum aluno cadastrado!')

    def widgets_remover_projeto(self, janela):
        label_remover_projeto = tk.Label(janela, text="Selecione os Projetos para Remover", font=("Arial", 10, "bold"))
        label_remover_projeto.pack(pady=10, padx=10)
        self.listbox_projetos = tk.Listbox(janela, selectmode=tk.MULTIPLE)
        self.listbox_projetos.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        self.cursor.execute('SELECT id, nome FROM projetos WHERE matricula=?', (self.usuario_logado,))
        projetos = self.cursor.fetchall()
        self.projeto_ids = {}
        for projeto in projetos:
            self.listbox_projetos.insert(tk.END, projeto[1])
            self.projeto_ids[projeto[1]] = projeto[0]
        button_confirmar_remocao = tk.Button(janela, text="Remover Selecionados", command=self.remover_projeto)
        button_confirmar_remocao.pack(pady=20, padx=10)

    def remover_projeto(self):
        if self.tem_cadastro():
            if self.login_aluno_ativo:
                selecoes = self.listbox_projetos.curselection()
                projetos_selecionados = [self.listbox_projetos.get(i) for i in selecoes]
                if not projetos_selecionados:
                    messagebox.showerror('ERRO', 'Você deve selecionar pelo menos um projeto para remover!')
                else:
                    for projeto in projetos_selecionados:
                        projeto_id = self.projeto_ids[projeto]
                        self.cursor.execute('DELETE FROM projetos WHERE id=?', (projeto_id,))
                        self.cursor.execute("DELETE FROM materiais WHERE id_projeto = ?", (projeto_id,))
                    self.conexao.commit()
                    print(f"Projetos removidos: {projetos_selecionados}")
                    messagebox.showinfo('SUCESSO', 'Projetos removidos com sucesso!')
                    self.nova_janela.destroy()
            else:
                messagebox.showerror('ERRO', 'Não é possível remover projetos sem estar logado como aluno!')
        else:
            messagebox.showerror('ERRO', 'Não há nenhum aluno cadastrado!')

    def widgets_alterar_dados(self, janela):
        dias= [dia for dia in range(1, 32)]
        meses = [mes for mes in range(1, 13)]
        anos = [ano for ano in range(1980, datetime.now().year + 1)]
        label_nome = tk.Label(janela, text="Novo Nome:", font=("Arial", 10, "bold"))
        label_nome.pack()
        self.entry_nome = tk.Entry(janela)
        self.entry_nome.pack(padx=5, pady=5, fill=tk.X)
        label_email = tk.Label(janela, text="Novo Email:", font=("Arial", 10, "bold"))
        label_email.pack(pady=10, padx=10)
        self.entry_email = tk.Entry(janela)
        self.entry_email.pack(padx=5, pady=5, fill=tk.X)
        label_idade = tk.Label(janela, text="Idade:", font=("Arial", 10, "bold"))
        label_idade.pack() 
        frame_idade_labels = tk.Frame(janela)
        frame_idade_labels.pack(padx=5, pady=5)
        frame_idade_entries = tk.Frame(janela)
        frame_idade_entries.pack(padx=5, pady=5, fill=tk.X)
        label_dia = tk.Label(frame_idade_labels, text="Dia", width=5, anchor='center')
        label_dia.pack(side="left", padx=5)
        label_mes = tk.Label(frame_idade_labels, text="Mês", width=8, anchor='center')
        label_mes.pack(side="left", padx=5)
        label_ano = tk.Label(frame_idade_labels, text="Ano", width=5, anchor='center')
        label_ano.pack(side="left", padx=5)
        self.combo_dia = ttk.Combobox(frame_idade_entries, values=dias, width=5)
        self.combo_dia.pack(side="left", padx=5)
        self.combo_mes = ttk.Combobox(frame_idade_entries, values=meses, width=5)
        self.combo_mes.pack(side="left", padx=5)
        self.combo_ano = ttk.Combobox(frame_idade_entries, values=anos, width=8)
        self.combo_ano.pack(side="left", padx=5)
        label_sexo = Label(janela, text="Sexo:", font=("Arial", 10, "bold"))
        label_sexo.pack()
        self.combo_sexo = ttk.Combobox(janela, values=["Masculino", "Feminino", "Outro"])
        self.combo_sexo.pack(padx=5, pady=5, fill=tk.X)
        button_alterar_dados = tk.Button(janela, text="Alterar Dados", command=self.alterar_dados)
        button_alterar_dados.pack(pady=10)

    def alterar_dados(self):
        novo_nome = self.entry_nome.get()
        novo_email = self.entry_email.get()
        novo_dia = self.combo_dia.get()
        novo_mes = self.combo_mes.get()
        novo_ano = self.combo_ano.get()
        novo_sexo = self.combo_sexo.get()
        if novo_nome and novo_email and novo_dia and novo_mes and novo_ano and novo_sexo:
            try:
                nova_idade = self.calcular_idade(novo_dia, novo_mes, novo_ano)
                self.cursor.execute('UPDATE alunos SET nome=?, email=?, idade=?, sexo=? WHERE matricula = ?', (novo_nome, novo_email, nova_idade, novo_sexo, self.usuario_logado))
                self.conexao.commit()
                messagebox.showinfo("Sucesso", "Dados alterados com sucesso!")
                self.nova_janela.destroy()
            except ValueError:
                messagebox.showerror("ERRO", "Data de nascimento inválida!")
        else:
            messagebox.showerror("ERRO", "Todos os campos devem ser preenchidos!")

    def abrir_alterar_dados(self):
        if self.tem_cadastro():
            if self.login_aluno_ativo:
                self.nova_janela = tk.Toplevel(self.janela_principal)
                self.nova_janela.title("Alterar Dados")
                self.nova_janela.geometry("200x400")
                self.widgets_alterar_dados(self.nova_janela)
            else:
                messagebox.showerror('ERRO', 'Faça login como aluno primeiro!')
        else:
            messagebox.showerror('ERRO', 'Não existe nenhum aluno cadastrado!')

    def remover_aluno(self):
        if self.tem_cadastro():
            if self.login_aluno_ativo:
                confirmar = messagebox.askyesno("REMOVER ALUNO", "Tem certeza que deseja remover o(a) aluno(a)?")
                if confirmar:
                    self.cursor.execute("DELETE FROM alunos WHERE matricula = ?", (self.usuario_logado,))
                    self.cursor.execute("DELETE FROM projetos WHERE matricula = ?", (self.usuario_logado,))
                    self.cursor.execute("DELETE FROM materiais WHERE id_projeto IN (SELECT id FROM projetos WHERE matricula = ?)", (self.usuario_logado,))
                    self.conexao.commit()
                    self.login_aluno_ativo = False
                    messagebox.showinfo("Sucesso", "Aluno removido com sucesso!")
            else:
                messagebox.showerror('ERRO', 'Faça login como aluno primeiro!')
        else:
            messagebox.showerror('ERRO', 'Não há nenhum aluno cadastrado!')

    def fazer_logout(self):
        if not self.login_adm_ativo and not self.login_aluno_ativo:
            messagebox.showerror('ERRO', 'Nenhum aluno ou administrador logado!')
        else:
            confirmar = messagebox.askyesno("LOGOUT", "Tem certeza que deseja fazer logout?")
            if not confirmar:
                pass
            else:
                self.login_adm_ativo = False
                self.login_aluno_ativo = False
                messagebox.showinfo("SUCESSO", "Logout efetuado com sucesso!")

    def limpar_banco_de_dados(self):
        if self.login_adm_ativo == True:
            confirmar = messagebox.askyesno("LIMPAR BANCO DE DADOS", "Tem certeza que deseja limpar todo o banco de dados?.")
            if confirmar:
                novo_aviso = messagebox.askyesno("AVISO!", "Esta ação é irreversível.")
                if novo_aviso:
                    self.cursor.execute("DELETE FROM projetos")
                    self.cursor.execute("DELETE FROM materiais")
                    self.cursor.execute("DELETE FROM alunos")
                    self.conexao.commit()
                    self.cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'projetos'")
                    self.cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'materiais'")
                    self.conexao.commit()
                    messagebox.showinfo("SUCESSO", "Banco de dados limpo com sucesso!")
                else:
                    pass
            else:
                pass
        else:
            messagebox.showerror('ERRO', 'Faça login como administrador primeiro!')

    def tocar_musica(self):
        nome_musica = 'Contato.mp3'
        pygame.mixer.music.load(nome_musica)
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

    def alternar_musica(self):
        if self.tocando_musica:
            pygame.mixer.music.pause()
            self.tocando_musica = False
            self.botao_play_pause.config(text="TOCAR MÚSICA")
        else:
            pygame.mixer.music.unpause()
            self.tocando_musica = True
            self.botao_play_pause.config(text="PAUSAR MÚSICA")

    def sair(self):
        sair = messagebox.askyesno('SAIR', 'Tem certeza que deseja sair?')
        if sair:
            self.janela_principal.quit()

    def aluno_existe(self, instituicao, matricula):
        self.cursor.execute("SELECT nome FROM alunos WHERE (instituicao, matricula) = (?, ?)", (instituicao, matricula))
        return self.cursor.fetchone() is not None

    def obter_nome_aluno(self, matricula, instituicao):
        self.cursor.execute("SELECT nome FROM alunos WHERE (matricula, instituicao) = (?, ?)", (matricula, instituicao))
        return self.cursor.fetchone()[0]

    def tem_cadastro(self):
        self.cursor.execute('SELECT COUNT(*) FROM alunos')
        resultado = self.cursor.fetchone()
        if resultado[0] > 0:
            return True
        else:
            return False

    def instituicao_existe(self, instituicao):
        self.cursor.execute("SELECT instituicao FROM alunos WHERE instituicao = ?", (instituicao,))
        return self.cursor.fetchone() is not None

    def instituicao_aluno(self):
        self.cursor.execute("SELECT instituicao FROM alunos WHERE matricula = ?", (self.usuario_logado,))
        return self.cursor.fetchone()[0]

    def matricula_aluno(self):
        self.cursor.execute("SELECT matricula FROM alunos WHERE matricula = ?", (self.usuario_logado,))
        return self.cursor.fetchone()[0]

    def senha_aluno(self, matricula, instituicao):
        self.cursor.execute("SELECT senha FROM alunos WHERE (matricula, instituicao) = (?, ?)", (matricula, instituicao))
        return self.cursor.fetchone()[0]

    def senha_adm(self):
        senha = 'pe-de-moleque'
        return senha

    def usuario_adm(self):
        usuario = 'Admin'
        return usuario

    def nome_instituicoes(self):
        self.cursor.execute("SELECT DISTINCT instituicao FROM alunos")
        return self.cursor.fetchall()

if __name__ == "__main__":
    SoftLab()