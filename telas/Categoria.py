import customtkinter
import requests
import json
from CTkTable import *
from CTkMessagebox import CTkMessagebox

class Categoria(customtkinter.CTkFrame):
    def __init__(self,parent,usuario):
        super().__init__(parent)    
        self.after(100, self.lift)
        #inicializar variaveis
        self.table = None
        self.usuario=usuario
        #Construir tela
        self.buildUi()
        
    def editarApagar(self,row):
        print(row['row'])
        
    def loadCategorias(self):
        if self.table and self.table.winfo_exists():
            self.table.destroy()
            
        url = f'http://localhost:5000/categoria'
        headers = {"Authorization":f'{self.usuario["id"]}'}

        #Faz a requisição
        response = requests.get(url,headers=headers)
        headers = ["id", "categoria", "tipo", "usuario_id"]

        # Inicializa value com os cabeçalhos
        value = [headers]

        # Itera sobre as categorias
        for categoria in response.json():
            # Extrai os valores correspondentes para cada linha
            row = [
                categoria['categoria_id'],
                categoria['nome_categoria'],
                categoria['tipo'],
                categoria['usuario']['usuario_id']
            ]
            # Adiciona a linha à lista value
            value.append(row)
            
        self.table = CTkTable(master=self, values=value, command=self.editarApagar)
        self.table.pack(fill="both", padx=20, pady=20)
        return True
        
    def buildUi(self):
        self.titulo = customtkinter.CTkLabel(self, text="Cadastrar nova categoria", font=("Arial", 16))
        self.titulo.pack(padx=10, pady=10)

        self.input_frame = customtkinter.CTkFrame(self)
        self.input_frame.pack(padx=15, pady=15, fill="y")
        
        self.nome_categoria = customtkinter.CTkEntry(self.input_frame, placeholder_text="Nome da categoria")
        self.nome_categoria.pack(side="left", padx=10, pady=10, expand=True, fill="x")

        # Variável para armazenar o valor selecionado
        self.tipo_categoria = customtkinter.StringVar(value="Receita")

        # Radio buttons para "Receita" e "Despesa"
        self.radio_receita = customtkinter.CTkRadioButton(self.input_frame, text="Receita", variable=self.tipo_categoria, value="Receita")
        self.radio_receita.pack(side="left", padx=10, pady=10)

        self.radio_despesa = customtkinter.CTkRadioButton(self.input_frame, text="Despesa", variable=self.tipo_categoria, value="Despesa")
        self.radio_despesa.pack(side="left", padx=10, pady=10)
        
        self.adicionar = customtkinter.CTkButton(self.input_frame, text="Adicionar",command=self.adicionarCategoria)
        self.adicionar.pack(padx=10,pady=10)
        values = self.loadCategorias()
            
    def adicionarCategoriaOld(self):
        formAdd = customtkinter.CTkToplevel(self) 
        formAdd.after(100, formAdd.lift) 
        
        formAdd.categoria = customtkinter.CTkLabel(formAdd, text="Adicionar Categoria", font=("Arial", 18))
        formAdd.categoria.pack(padx=10, pady=10)
        
        formAdd.nome = customtkinter.CTkEntry(formAdd, placeholder_text="Transporte")
        formAdd.nome.pack(padx=10, pady=10)        
                       
        formAdd.tipo1 = customtkinter.CTkCheckBox(formAdd, text="Entrada", onvalue="on", offvalue="off")
        formAdd.tipo1.pack(padx=10, pady=10, side="left") 
        formAdd.tipo2 = customtkinter.CTkCheckBox(formAdd, text="Saída", onvalue="on", offvalue="off")
        formAdd.tipo2.pack(padx=10, pady=10, side="left")      
        
        formAdd.adicionar = customtkinter.CTkButton(formAdd, text="Adicionar")
        formAdd.adicionar.pack(padx=10,pady=10)
        
    def adicionarCategoria(self):
        url = f'http://localhost:5000/categoria'
        data = {
            'usuario_id': self.usuario['id'],
            'nome_categoria':self.nome_categoria.get(),
            'tipo':self.tipo_categoria.get()
        }
        response = requests.post(url,data,timeout=10)
        if response.status_code == 200:
            # data = response.json()
            # categoria = [data['categoria_id'],data['nome_categoria'],data['tipo'],data['usuario']['usuario_id'] ]
            # self.table.add_row(categoria)
            self.loadCategorias()
            CTkMessagebox(title="Categoria cadastrada", message="Categoria cadastrada com sucesso!!", icon="check")
            self.nome_categoria.delete(0,customtkinter.END)
        else:
            erros = response.json()['errors']
            error_message = '\n'.join([f"{', '.join(msgs)}" for field, msgs in erros.items()])
            CTkMessagebox(title="Erro ao cadastrar categoria", message=error_message, icon="cancel")
