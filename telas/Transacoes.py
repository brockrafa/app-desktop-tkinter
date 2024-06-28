import customtkinter
import requests
import json
from CTkTable import *
from CTkMessagebox import CTkMessagebox
from PIL import Image, ImageTk

class Transacao(customtkinter.CTkFrame):
    def __init__(self,parent,usuario):
        super().__init__(parent)    
        
        #inicializar variaveis
        self.table = None
        self.usuario=usuario
        #Construir tela
        self.buildUi()
        
    def editarApagar(self,row):
        print(row['row'])
        
    def loadTransacoes(self):
        if self.table and self.table.winfo_exists():
            self.table.destroy()
            
        url = f'http://localhost:5000/transacao'
        headers = {"Authorization":f'{self.usuario["id"]}'}

        #Faz a requisição
        response = requests.get(url,headers=headers)
        headers = ["Id","Descrição", "Conta", "Categoria", "Tipo", "Valor", "Data"]

        # Inicializa value com os cabeçalhos
        value = [headers]
        # Itera sobre as categorias
        for transacao in response.json():
            # Extrai os valores correspondentes para cada linha
            row = [
                transacao['transacao_id'],
                transacao['descricao'],
                transacao['conta'],
                transacao['categoria'],
                transacao['tipo'],
                'R$ '+str(transacao['valor']),
                transacao['data']
            ]
            # Adiciona a linha à lista value
            value.append(row)
            
        self.table = CTkTable(master=self, values=value, command=self.editarApagar)
        self.table.pack(fill="both", padx=20, pady=20)
        return True
        
    def buildUi(self):
        
                
        # Carregando ícone
        icon_path = r"C:\Users\Rafael\Desktop\teste interface\telas\icon\transacao.png"  # Caminho correto do seu ícone
        icon_image = Image.open(icon_path)
        icon_image = icon_image.resize((50, 50), Image.LANCZOS)   # Redimensiona para o tamanho desejado
        icon_photo = ImageTk.PhotoImage(icon_image)

        self.titulo = customtkinter.CTkLabel(self, text="    Transações", font=("Arial", 20))
        self.titulo.pack(padx=10, pady=10)
      
        # Adicionando o ícone à label
        self.titulo.icon = icon_photo  # Mantém uma referência para evitar que a imagem seja limpa pela coleta de lixo
        self.titulo.configure(image=self.titulo.icon, compound="left")  # Define o ícone à esquerda do texto
        # self.titulo.place(x=10, y=10)

        self.input_frame = customtkinter.CTkFrame(self)
        self.input_frame.pack(padx=15, pady=15, fill="y")
        
        self.titulo1 = customtkinter.CTkLabel(self.input_frame, text="Cadastrar nova transacao", font=("Arial", 16))
        self.titulo1.grid(row=0, columnspan=2, padx=30, pady=10)
        
        # self.nome_transacao = customtkinter.CTkEntry(self.input_frame, placeholder_text="Nome da categoria")
        # self.nome_transacao.pack(side="left", padx=10, pady=10, expand=True, fill="x")

        # Variável para armazenar o valor selecionado
        self.tipo = customtkinter.StringVar(value="Receita")

        # Radio buttons para "Receita" e "Despesa"
        self.radio_receita = customtkinter.CTkRadioButton(self.input_frame, text="Receita", variable=self.tipo, value="Receita")
        self.radio_receita.grid(row=5, column=0, padx=30, pady=10, sticky="w")

        self.radio_despesa = customtkinter.CTkRadioButton(self.input_frame, text="Despesa", variable=self.tipo, value="Despesa")
        self.radio_despesa.grid(row=5, column=1, padx=30, pady=10, sticky="w")
        
        label_descricao = customtkinter.CTkLabel(self.input_frame, text="Descrição:")
        label_descricao.grid(row=1, column=0, padx=30, pady=5, sticky="w")
        
        label_valor = customtkinter.CTkLabel(self.input_frame, text="Valor:")
        label_valor.grid(row=2, column=0, padx=30, pady=5, sticky="w")
        
        label_conta = customtkinter.CTkLabel(self.input_frame, text="Conta:")
        label_conta.grid(row=3, column=0, padx=30, pady=5, sticky="w")
        
        label_categoria = customtkinter.CTkLabel(self.input_frame, text="Categoria:")
        label_categoria.grid(row=4, column=0, padx=30, pady=5, sticky="w")
        
        # Campos de entrada
        self.valor = customtkinter.CTkEntry(self.input_frame, placeholder_text="Ex.: 250.00")
        self.valor.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        self.descricao = customtkinter.CTkEntry(self.input_frame, placeholder_text="Ex.: Conta de luz")
        self.descricao.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        
        #Select Contas
        contas = self.loadContas()
        self.combobox = customtkinter.CTkOptionMenu(self.input_frame,
                                       values=contas)
        self.combobox.grid(row=3, column=1, padx=10, pady=10)
        

        #Select categorias
        self.categorias_values = self.loadCategorias()
        self.combobox_categoria = customtkinter.CTkOptionMenu(self.input_frame,
                                       values=self.categorias_values)
        self.combobox_categoria.grid(row=4, column=1, padx=10, pady=10)
        
        self.adicionar = customtkinter.CTkButton(self.input_frame, text="Adicionar",command=self.adicionarTransacao)
        self.adicionar.grid(row=6, columnspan=2, padx=30, pady=20)

        values = self.loadTransacoes()
       
    def loadContas(self):
            
        url = f'http://localhost:5000/conta'
        headers = {"Authorization":f'{self.usuario["id"]}'}

        #Faz a requisição
        response = requests.get(url,headers=headers)
        # Inicializa value com os cabeçalhos
        values = ["Selecione uma conta"]

        # Itera sobre as categorias
        for conta in response.json():
            values.append(str(conta['conta_id'])+'-'+conta['nome_conta'])
        
        return values

        # self.table = CTkTable(master=self, values=value, command=self.editarApagar)
        # self.table.pack(fill="both", padx=20, pady=20)
        # return True    
    
    def loadCategorias(self):
            
        url = f'http://localhost:5000/categoria'
        headers = {"Authorization":f'{self.usuario["id"]}'}

        #Faz a requisição
        response = requests.get(url,headers=headers)
        # Inicializa value com os cabeçalhos
        values = ["Selecione uma categoria"]

        # Itera sobre as categorias
        for categoria in response.json():
            values.append(str(categoria['categoria_id'])+'-'+categoria['nome_categoria'])
        
        return values
           
    def adicionarTransacao(self):
        url = f'http://localhost:5000/transacao'
        data = {
            'usuario_id': self.usuario['id'],
            'descricao': self.descricao.get(),
            'conta_id':self.combobox.get().split('-')[0],
            'categoria_id':self.combobox_categoria.get().split('-')[0],
            'tipo':self.tipo.get(),
            'valor':self.valor.get(),
        }
        response = requests.post(url,data,timeout=10)
        if response.status_code == 200:
            self.loadTransacoes()
            CTkMessagebox(title="Transacao cadastrada", message="Transacao cadastrada com sucesso!!", icon="check")
            self.id_transacao.delete(0,customtkinter.END)
        else:
            erros = response.json()['errors']
            error_message = '\n'.join([f"{', '.join(msgs)}" for field, msgs in erros.items()])
            CTkMessagebox(title="Erro ao cadastrar transacao", message=error_message, icon="cancel")

    def editarApagar(self,row):
        #obter os dados da tabela
        self.dados=self.table.select_row(row['row'])
        #Id da transacao
        self.id_transacao_edit=self.dados[0]
        self.conta_id_edit=self.dados[2]
        self.valor_edit=self.dados[5].replace("R$","")
        self.tipo_edit = self.dados[4]
        
        self.formAdd = customtkinter.CTkToplevel(self) 
        self.formAdd.title("Editar transacao")
        self.formAdd.geometry("400x300")
        self.formAdd.after(100, self.formAdd.lift) 
        
        self.input_frame_edit = customtkinter.CTkFrame(self.formAdd)
        self.input_frame_edit.pack(padx=15, pady=15, fill="y")
        
        label_nome_transacao_edit = customtkinter.CTkLabel(self.input_frame_edit, text="Descrição da transacao:")
        label_nome_transacao_edit.grid(row=0, column=0, padx=30, pady=5, sticky="w")
        
        self.descricao_transacao_edit = customtkinter.CTkEntry(self.input_frame_edit, placeholder_text="Descrição da transacao")
        self.descricao_transacao_edit.insert(0, self.dados[1])
        self.descricao_transacao_edit.grid(row=1, column=0, padx=30, pady=5, sticky="w")
        
        label_categoria_edit = customtkinter.CTkLabel(self.input_frame_edit, text="Categoria:")
        label_categoria_edit.grid(row=2, column=0, padx=30, pady=5, sticky="w")
        
        self.combobox_categoria_edit = customtkinter.CTkOptionMenu(self.input_frame_edit,
                                       values=self.categorias_values)
        self.combobox_categoria_edit.grid(row=3, column=0, padx=10, pady=10)
        valor_encontrado = None
        for indice, valor in enumerate(self.categorias_values):
            if self.dados[3] in valor:
                valor_encontrado = valor
        self.combobox_categoria_edit.set(valor_encontrado)
        
        self.adicionar_edit = customtkinter.CTkButton(self.input_frame_edit, text="Atualizar",command=self.atualizartransacao)
        self.adicionar_edit.grid(row=8, column=0, padx=30, pady=20, sticky="w")

    def atualizartransacao(self):
        url = f'http://localhost:5000/transacao/{self.id_transacao_edit}'
        data = {
            'usuario_id': self.usuario['id'],
            'descricao': self.descricao_transacao_edit.get(),
            'conta_id':self.conta_id_edit,
            'categoria_id':self.combobox_categoria_edit.get().split('-')[0],
            'tipo':self.tipo_edit,
            'valor':self.valor_edit,
        }
        response = requests.put(url,data)
        if response.status_code == 200:
            self.loadTransacoes()
            CTkMessagebox(title="Transacao atualizada", message="Transacao atualizada com sucesso!!", icon="info")
            self.formAdd.destroy()
        else:
            erros = response.json()['errors']
            error_message = '\n'.join([f"{', '.join(msgs)}" for field, msgs in erros.items()])
            CTkMessagebox(title="Erro ao atualizado transacao", message=error_message, icon="cancel")