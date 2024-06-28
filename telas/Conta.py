import customtkinter
import requests
import json
from CTkTable import *
from CTkMessagebox import CTkMessagebox
from PIL import Image, ImageTk
 
class Conta(customtkinter.CTkFrame):
    def __init__(self,parent,usuario, *args, **kwargs):
        super().__init__(parent, *args, **kwargs) 
        self.usuario = usuario    
        largura_screen = self.winfo_screenwidth()
        altura_screen = self.winfo_screenheight()
        self.table = None
        self.buildUi()
        
    def loadContas(self):
        if self.table and self.table.winfo_exists():
            self.table.destroy()
            
        url = f'http://localhost:5000/conta'
        
        headers = {"Authorization":f'{self.usuario["id"]}'}
        
        #Faz a requisição
        response = requests.get(url,headers=headers)
        headers = ['Id',"Nome", "Saldo"]
        
        # Inicializa value com os cabeçalhos
        value = [headers]
        # Itera sobre as contas
        for conta in response.json():
            # Extrai os valores correspondentes para cada linha
            row = [
                conta['conta_id'],
                conta['nome_conta'],
                "R$ " + str(conta['saldo_inicial'])
            ]
            # Adiciona a linha à lista value
            value.append(row)
            
            
        self.table = CTkTable(master=self, values=value, command=self.editarApagar)
        self.table.pack(fill="both", padx=20, pady=20)
        return True
    
    def buildUi(self):
        
        # Carregando ícone
        icon_path = r"C:\Users\Rafael\Desktop\teste interface\telas\icon\conta.png"  # Caminho correto do seu ícone
        icon_image = Image.open(icon_path)
        icon_image = icon_image.resize((50, 50), Image.LANCZOS)   # Redimensiona para o tamanho desejado
        icon_photo = ImageTk.PhotoImage(icon_image)

        self.titulo = customtkinter.CTkLabel(self, text="    Contas", font=("Arial", 20))
        self.titulo.pack(padx=10, pady=10)
      
        # Adicionando o ícone à label
        self.titulo.icon = icon_photo  # Mantém uma referência para evitar que a imagem seja limpa pela coleta de lixo
        self.titulo.configure(image=self.titulo.icon, compound="left")  # Define o ícone à esquerda do texto
        # self.titulo.place(x=10, y=10)
        
        self.titulo = customtkinter.CTkLabel(self, text="Cadastrar nova conta", font=("Arial", 16))
        self.titulo.pack(padx=10, pady=10)
        
        self.input_frame = customtkinter.CTkFrame(self)
        self.input_frame.pack(fill='y')
        
        label_nome_conta = customtkinter.CTkLabel(self.input_frame, text="Nome da conta:")
        label_nome_conta.grid(row=0, column=0, padx=30, pady=5, sticky="w")
        
        label_valor_conta = customtkinter.CTkLabel(self.input_frame, text="Valor da conta:")
        label_valor_conta.grid(row=2, column=0, padx=30, pady=5, sticky="w")
        
        # Campos de entrada
        self.nome_conta = customtkinter.CTkEntry(self.input_frame, placeholder_text="Ex.: Nubank")
        self.nome_conta.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        self.valor_conta = customtkinter.CTkEntry(self.input_frame, placeholder_text="Ex.: 200.00")
        self.valor_conta.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        
        # Botão de adicionar
        self.adicionar = customtkinter.CTkButton(self.input_frame, text="Adicionar",  command=self.adicionarConta)
        self.adicionar.grid(row=3,  columnspan=2, padx=10, pady=10)
        # self.adicionar.pack(padx=10,pady=10)
        values = self.loadContas()
        
    def adicionarConta(self):
        url = f'http://localhost:5000/conta'
        data = {
            'usuario_id': self.usuario['id'],
            'nome_conta': self.nome_conta.get(),
            'saldo_inicial':self.valor_conta.get()
        }
        response = requests.post(url,data,timeout=10)
        if response.status_code == 200:
            self.loadContas()
            CTkMessagebox(title="Conta cadastrada", message="Conta cadastrada com sucesso!!", icon="check")
            self.nome_conta.delete(0,customtkinter.END)
        else:
            erros = response.json()['errors']
            error_message = '\n'.join([f"{', '.join(msgs)}" for field, msgs in erros.items()])
            CTkMessagebox(title="Erro ao cadastrar conta", message=error_message, icon="cancel")
            
    def editarApagar(self,row):
        self.dados=self.table.select_row(row['row'])
        self.id_conta_edit=self.dados[0]
        
        self.janela_opcoes = customtkinter.CTkToplevel(self) 
        self.janela_opcoes.after(100, self.janela_opcoes.lift) 
        
        self.btn_adicionar_edit = customtkinter.CTkButton(self.janela_opcoes, text="Editar",command=self.janelaAtualizarConta)
        self.btn_excluir_edit = customtkinter.CTkButton(self.janela_opcoes, text="Excluir",command=self.deletarConta)
        self.btn_adicionar_edit.pack(padx=20,pady=20)
        self.btn_excluir_edit.pack(padx=20,pady=20)
       
    def janelaAtualizarConta(self):
        self.janela_opcoes.destroy()
        self.formAdd = customtkinter.CTkToplevel(self) 
        self.formAdd.after(100, self.formAdd.lift) 
        self.formAdd.title("Editar conta")
        self.formAdd.geometry("500x100")
        
        self.input_frame_edit = customtkinter.CTkFrame(self.formAdd)
        self.input_frame_edit.pack(padx=15, pady=15, fill="y")
        
        self.nome_conta_edit = customtkinter.CTkEntry(self.input_frame_edit, placeholder_text="Nome da conta")
        self.nome_conta_edit.insert(0, self.dados[1])
        self.nome_conta_edit.pack(side="left", padx=10, pady=10, expand=True, fill="x")
        
        self.saldo_conta_edit = customtkinter.CTkEntry(self.input_frame_edit, placeholder_text="Saldo da conta")
        self.saldo_conta_edit.insert(0, self.dados[2].replace("R$",''))
        self.saldo_conta_edit.pack(side="left", padx=10, pady=10, expand=True, fill="x")
        
        self.adicionar_edit = customtkinter.CTkButton(self.input_frame_edit, text="Atualizar",command=self.atualizarConta)
        self.adicionar_edit.pack(padx=10,pady=10)
                   
    def atualizarConta(self):
        url = f'http://localhost:5000/conta/{self.id_conta_edit}'
        data = {
            'usuario_id': self.usuario['id'],
            'nome_conta':self.nome_conta_edit.get(),
            'saldo_inicial':self.saldo_conta_edit.get()
        }
        response = requests.put(url,data)
        if response.status_code == 200:
            self.loadContas()
            CTkMessagebox(title="Conta atualizada", message="Conta atualizada com sucesso!!", icon="info")
            self.formAdd.destroy()
        else:
            erros = response.json()['errors']
            error_message = '\n'.join([f"{', '.join(msgs)}" for field, msgs in erros.items()])
            CTkMessagebox(title="Erro ao atualizado conta", message=error_message, icon="cancel")
            
    def deletarConta(self):
        url = f'http://localhost:5000/conta/{self.id_conta_edit}'

        response = requests.delete(url)
        if response.status_code == 200:
            self.loadContas()
            CTkMessagebox(title="Conta excluída", message="Conta excluída com sucesso!!", icon="cancel")
            self.janela_opcoes.destroy()
        else:
            erros = response.json()['errors']
            error_message = '\n'.join([f"{', '.join(msgs)}" for field, msgs in erros.items()])
            CTkMessagebox(title="Erro ao excluír conta", message=error_message, icon="cancel")