#import tkinter as tk  # Importa a biblioteca tkinter para criar interfaces gráficas
from tkinter import BOTTOM, Label, BOTH, Tk, ttk, messagebox, simpledialog  # Importa módulos específicos do tkinter
import os  # Importa a biblioteca os para interagir com o sistema operacional

class SistemaLaboratorio:
    def __init__(self):  # Método inicializador da classe
        self.alunos = {}  # Dicionário para armazenar os alunos
        self.projetos = {}  # Dicionário para armazenar os projetos dos alunos
        self.arquivo_dados = "dados_laboratorio.txt"  # Nome do arquivo para salvar os dados
        self.login_ativo = False  # Flag para verificar se o login está ativo
        self.usuario_logado = None  # Armazena a matrícula do usuário logado
        self.carregar_dados()  # Carrega os dados do arquivo ao iniciar
        self.root = Tk()  # Cria a janela principal
        self.create_widgets()  # Chama o método para criar os widgets da interface
        self.root.title("SOFTLAB")  # Define o título da janela
        self.bottom_text_label = Label(self.root, text="Por Felipe Cidade Soares e Ivy Oliveira dos Reis", font=("Arial", 10), fg="black", anchor="w")
        self.bottom_text_label.pack(side=BOTTOM, pady=10, fill="x")
        self.root.geometry("400x630")  # Define o tamanho da janela
        

    def carregar_dados(self):  # Método para carregar os dados do arquivo
        if os.path.exists(self.arquivo_dados):  # Verifica se o arquivo existe
            with open(self.arquivo_dados, 'r') as arquivo:  # Abre o arquivo em modo de leitura
                secao_atual = None  # Inicializa a variável de seção atual
                for linha in arquivo:  # Itera sobre cada linha do arquivo
                    linha = linha.strip()  # Remove espaços em branco das extremidades
                    if linha.startswith("###"):  # Verifica se a linha indica uma nova seção
                        secao_atual = linha.replace("#", "").strip()  # Define a seção atual
                    elif linha:  # Se a linha não estiver vazia
                        if secao_atual == "Alunos":  # Se estiver na seção de alunos
                            matricula, nome = linha.split(',')  # Divide a linha em matrícula e nome
                            self.alunos[matricula] = nome  # Adiciona ao dicionário de alunos
                        elif secao_atual == "Projetos":  # Se estiver na seção de projetos
                            matricula, projetos_str = linha.split(':')  # Divide a linha em matrícula e projetos
                            projetos = projetos_str.split(',')  # Divide os projetos em uma lista
                            self.projetos[matricula] = projetos  # Adiciona ao dicionário de projetos

    def salvar_dados(self):  # Método para salvar os dados no arquivo
        with open(self.arquivo_dados, 'w') as arquivo:  # Abre o arquivo em modo de escrita
            arquivo.write("### Alunos ###\n")  # Escreve a seção de alunos
            for matricula, nome in self.alunos.items():  # Itera sobre cada aluno
                arquivo.write(f"{matricula},{nome}\n")  # Escreve a matrícula e o nome no arquivo
            arquivo.write("\n### Projetos ###\n")  # Escreve a seção de projetos
            for matricula, projetos in self.projetos.items():  # Itera sobre cada projeto
                arquivo.write(f"{matricula}:{','.join(projetos)}\n")  # Escreve a matrícula e os projetos no arquivo

    def create_widgets(self):  # Método para criar os widgets da interface
        style = ttk.Style()  # Cria um estilo para os widgets
        style.configure("TButton", padding=15, font=("Arial", 9), foreground="black", background="#add8e6")  # Configura o estilo dos botões
        style.configure("TLabel", padding=10, font=("Arial", 18, "bold"))  # Configura o estilo do título
        self.frame = ttk.Frame(self.root)  # Cria um frame dentro da janela principal
        self.frame.pack(fill=BOTH, expand=True, padx=20, pady=10)  # Adiciona o frame à janela com preenchimento
        self.label_title = ttk.Label(self.frame, text="SOFTLAB", style="TLabel", foreground="blue")  # Cria o rótulo do título
        self.label_title.grid(row=0, column=0, columnspan=2, pady=10)  # Posiciona o rótulo no grid
        self.btn_registrar = ttk.Button(self.frame, text="REGISTRAR NOVO ALUNO", command=self.registrar_aluno, style="TButton", width=30)  # Cria o botão de registrar aluno
        self.btn_registrar.grid(row=1, column=0, pady=5, padx=15)  # Posiciona o botão no grid
        self.btn_login = ttk.Button(self.frame, text="FAZER LOGIN", command=self.fazer_login, style="TButton", width=30)  # Cria o botão de login
        self.btn_login.grid(row=2, column=0, pady=5, padx=5)  # Posiciona o botão no grid
        self.btn_listar = ttk.Button(self.frame, text="LISTAR ALUNOS(AS)", command=self.listar_alunos, style="TButton", width=30)  # Cria o botão de listar alunos
        self.btn_listar.grid(row=3, column=0, pady=5, padx=5)  # Posiciona o botão no grid
        self.btn_adicionar_projeto = ttk.Button(self.frame, text="ADICIONAR ATIVIDADE", command=self.adicionar_projeto, style="TButton", width=30)  # Cria o botão de adicionar projeto
        self.btn_adicionar_projeto.grid(row=4, column=0, pady=5, padx=5)  # Posiciona o botão no grid
        self.btn_listar_projetos = ttk.Button(self.frame, text="LISTAR ATIVIDADE DE UM ALUNO(A)", command=self.listar_projetos_aluno, style="TButton", width=30)  # Cria o botão de listar projetos

        self.btn_listar_projetos.grid(row=5, column=0, pady=5, padx=5)  # Posiciona o botão no grid

        self.btn_alterar = ttk.Button(self.frame, text="ALTERAR DADOS DE UM ALUNO(A)", command=self.alterar_dados_aluno, style="TButton", width=30)  # Cria o botão de alterar dados do aluno
        
        self.btn_alterar.grid(row=6, column=0, pady=5, padx=5)  # Posiciona o botão no grid

        self.btn_remover = ttk.Button(self.frame, text="REMOVER ALUNO(A)", command=self.remover_aluno, style="TButton", width=30)  # Cria o botão de remover aluno
        self.btn_remover.grid(row=7, column=0, pady=5, padx=5)  # Posiciona o botão no grid

        self.btn_sair = ttk.Button(self.frame, text="SAIR", command=self.fechar_janela, style="TButton", width=30)  # Cria o botão de sair
        self.btn_sair.grid(row=8, column=0, pady=5, padx=5)  # Posiciona o botão no grid

    def registrar_aluno(self):  # Método para registrar um novo aluno
        try:
            matricula = simpledialog.askstring("Registrar novo aluno", "Digite a matrícula do aluno:")  # Solicita a matrícula do aluno
            if matricula is None or matricula == "":
                raise ValueError("Operação cancelada pelo usuário.")
                matricula == ""
            if matricula in self.alunos:  # Verifica se a matrícula já existe
                messagebox.showerror("Erro", "Matrícula já existe. Tente novamente.")  # Exibe uma mensagem de erro
                return
        except ValueError:
            messagebox.showerror("Erro",str("Informe uma matrícula."))      
        else:
            if matricula in self.alunos and matricula != "" and matricula not in None:  # Verifica se a matrícula já existe
                messagebox.showerror("Erro", "Matrícula já existe. Tente novamente.")  # Exibe uma mensagem de erro
                return
            try:
                nome = simpledialog.askstring("Registrar novo aluno", "Digite o nome do aluno:")  # Solicita o nome do aluno
                if nome == "" or nome is None:
                    raise ValueError("Operação cancelada pelo usuário.")
                else:
                    self.alunos[matricula] = nome  # Adiciona o aluno ao dicionário
                    self.salvar_dados()  # Salva os dados no arquivo
                    messagebox.showinfo("Sucesso", "Aluno(a) registrado com sucesso!")  # Exibe uma mensagem de sucesso
            except ValueError:
                    messagebox.showerror("Erro",str("Informe o nome do aluno(a)."))
          
    def fazer_login(self):  # Método para fazer login
        matricula = simpledialog.askstring("Fazer login", "Digite sua matrícula:")  # Solicita a matrícula do usuário
        nome = self.alunos.get(matricula)  # Obtém o nome do aluno pela matrícula
        try:
            if matricula is None:
                raise ValueError("Operação cancelada pelo usuário.")
        except ValueError:
                messagebox.showerror("Erro",str("Informe o número de matrícula."))
        else:
            if nome:  # Verifica se o nome foi encontrado
                messagebox.showinfo("Bem-vindo", f"Bem-vindo(a), {nome}!")  # Exibe uma mensagem de boas-vindas
                self.login_ativo = True  # Ativa o login
                self.usuario_logado = matricula  # Armazena a matrícula do usuário logado
            else:
                messagebox.showerror("Erro", "Matrícula não encontrada.")  # Exibe uma mensagem de erro

    def listar_alunos(self):  # Método para listar os alunos
        if not self.alunos:  # Verifica se não há alunos cadastrados
            messagebox.showinfo("Informação", "Nenhum aluno cadastrado.")  # Exibe uma mensagem informativa
        else:
            try:
                alunos_ordenados = sorted(self.alunos.items(), key=lambda item: item[1])  # Ordena os alunos por nome
                lista_alunos = "\n".join([f"Nome: {nome} | Matrícula: {matricula}" for matricula, nome in alunos_ordenados])  # Cria a lista de alunos
                messagebox.showinfo("Alunos cadastrados", lista_alunos)  # Exibe a lista de alunos
            except:
                pass

    def adicionar_projeto(self):  # Método para adicionar um projeto a um aluno
        if not self.login_ativo:  # Verifica se o login está ativo
            messagebox.showerror("Erro", "Faça login primeiro para acessar esta opção.")  # Exibe uma mensagem de erro
            return

        matricula = self.usuario_logado  # Obtém a matrícula do usuário logado
        if matricula not in self.alunos:  # Verifica se a matrícula não está cadastrada
            messagebox.showerror("Erro", "Aluno não encontrado.")  # Exibe uma mensagem de erro
            return

        projetos_disponiveis = ["Programação com Arduino", "Corte a Laser", "Impressão 3D"]  # Lista de projetos disponíveis
        lista_projetos = "\n".join([f"{i+1}. {projeto}" for i, projeto in enumerate(projetos_disponiveis)])  # Cria a lista de projetos com índices

        projeto_escolhido_idx = simpledialog.askinteger("Adicionar atividade", f"Escolha um projeto pelo número:\n{lista_projetos}")  # Solicita o número do projeto escolhido
        if projeto_escolhido_idx is None or projeto_escolhido_idx < 1 or projeto_escolhido_idx > len(projetos_disponiveis):  # Verifica se a escolha é inválida
            messagebox.showerror("Erro", "Escolha inválida.")  # Exibe uma mensagem de erro
            return

        projeto_escolhido = projetos_disponiveis[projeto_escolhido_idx - 1]  # Obtém o projeto escolhido
        descricao_projetos = { "Programação com Arduino": "Sugestões de projetos:\n● Braço robótico com peças impressas na impressora 3D;\n● Interação com os componentes eletrônicos.",
            "Corte a Laser": "Sugestão de projetos:\n● Criação de quebra-cabeças;\n● Criação de jogos de tabuleiro.","Impressão 3D": "Sugestão de projetos:\n● Criação de brinquedos;\n● Produção de peças para outros projetos."}  # Descrições dos projetos

        materiais_projetos = {"Programação com Arduino": ["● Arduino;", "● Fios condutores;", "● Componentes eletrônicos: servomotores, potenciômetros, LEDs e LCDs;", "● Placas protoboards;","Arduino IDE."],"Corte a Laser": ["● Máquina de Corte a Laser;", "● Placas em MDF;","● Software de modelagem."],"Impressão 3D": ["● Impressora 3D;", "● Filamento;","● Software de modelagem 3D."]}  # Materiais necessários para cada projeto

        descricao = descricao_projetos[projeto_escolhido]  # Obtém a descrição do projeto escolhido
        messagebox.showinfo("Sugestões de projetos:\n", f"Projeto escolhido: {projeto_escolhido}\n{descricao}")  # Exibe a descrição do projeto

        mostrar_materiais = messagebox.askyesno("Materiais", "Deseja ver os materiais necessários para este projeto?")  # Pergunta se o usuário quer ver os materiais
        if mostrar_materiais:
            materiais = "\n".join(materiais_projetos[projeto_escolhido])  # Cria a lista de materiais
            messagebox.showinfo("Materiais necessários", f"Materiais para {projeto_escolhido}:\n{materiais}")  # Exibe a lista de materiais

        if matricula not in self.projetos:  # Verifica se a matrícula não tem projetos
            self.projetos[matricula] = []  # Inicializa a lista de projetos para a matrícula

        self.projetos[matricula].append(projeto_escolhido)  # Adiciona o projeto à lista de projetos da matrícula
        self.salvar_dados()  # Salva os dados no arquivo
        messagebox.showinfo("Sucesso", "Atividade adicionada com sucesso!")  # Exibe uma mensagem de sucesso

    def listar_projetos_aluno(self):  # Método para listar os projetos de um aluno
        if not self.login_ativo:  # Verifica se o login está ativo
            messagebox.showerror("Erro", "Faça login primeiro para acessar esta opção.")  # Exibe uma mensagem de erro
            return

        matricula = self.usuario_logado  # Obtém a matrícula do usuário logado
        if matricula not in self.projetos:  # Verifica se a matrícula não tem projetos
            messagebox.showinfo("Informação", "O aluno não possui projetos cadastrados.")  # Exibe uma mensagem informativa
            return

        lista_projetos = "\n".join(self.projetos[matricula])  # Cria a lista de projetos do aluno
        messagebox.showinfo("Atividades do aluno", f"Atividade do aluno {self.alunos[matricula]}:\n{lista_projetos}")  # Exibe a lista de projetos

    def alterar_dados_aluno(self):  # Método para alterar os dados de um aluno
        if not self.login_ativo:  # Verifica se o login está ativo
            messagebox.showerror("Erro", "Faça login primeiro para acessar esta opção.")  # Exibe uma mensagem de erro
            return

        matricula = self.usuario_logado  # Obtém a matrícula do usuário logado
        if matricula not in self.alunos:  # Verifica se a matrícula não está cadastrada
            messagebox.showerror("Erro", "Aluno não encontrado.")  # Exibe uma mensagem de erro
            return

        novo_nome = simpledialog.askstring("Alterar dados de um aluno", f"Digite o novo nome para o aluno {self.alunos[matricula]}:")  # Solicita o novo nome do aluno
        if novo_nome:
            self.alunos[matricula] = novo_nome  # Atualiza o nome do aluno no dicionário
            self.salvar_dados()  # Salva os dados no arquivo
            messagebox.showinfo("Sucesso", "Dados do aluno alterados com sucesso!")  # Exibe uma mensagem de sucesso

    def remover_aluno(self):  # Método para remover um aluno
        if not self.login_ativo:  # Verifica se o login está ativo
            messagebox.showerror("Erro", "Faça login primeiro para acessar esta opção.")  # Exibe uma mensagem de erro
            return
        matricula = self.usuario_logado  # Obtém a matrícula do usuário logado
        if matricula not in self.alunos:  # Verifica se a matrícula não está cadastrada
            messagebox.showerror("Erro", "Aluno não encontrado.")  # Exibe uma mensagem de erro
            return

        confirmar = messagebox.askyesno("Remover aluno", f"Tem certeza que deseja remover o aluno {self.alunos[matricula]}?")  # Solicita confirmação para remover o aluno
        if confirmar:
            del self.alunos[matricula]  # Remove o aluno do dicionário de alunos
            if matricula in self.projetos:
                del self.projetos[matricula]  # Remove os projetos do aluno, se existirem
            self.login_ativo = False  # Desativa o login
            self.usuario_logado = None  # Limpa a matrícula do usuário logado
            self.salvar_dados()  # Salva os dados no arquivo
            messagebox.showinfo("Sucesso", "Aluno removido com sucesso!")  # Exibe uma mensagem de sucesso
        else:
            messagebox.showinfo("Informação", "Operação de remoção cancelada.")  # Exibe uma mensagem informativa

    def fechar_janela(self):  # Método para fechar a janela
        self.salvar_dados()  # Salva os dados no arquivo
        self.root.destroy()  # Fecha a janela principal

    def run(self):  # Método para iniciar o loop principal da interface
        self.root.protocol("WM_DELETE_WINDOW", self.fechar_janela)  # Define o método a ser chamado ao fechar a janela
        self.root.mainloop()  # Inicia o loop principal da interface

def menu_principal():  # Função principal
    sistema = SistemaLaboratorio()  # Cria uma instância do sistema
    sistema.run()  # Executa o sistema

if __name__ == "__main__":  # Verifica se o script está sendo executado diretamente
    menu_principal()  # Chama a função principal