import customtkinter
import requests
import json
from CTkTable import *
from CTkMessagebox import CTkMessagebox


class Meta(customtkinter.CTkFrame):
    def __init__(self,parent,usuario, *args, **kwargs):
        super().__init__(parent, *args, **kwargs) 
        self.usuario = usuario    
        largura_screen = self.winfo_screenwidth()
        altura_screen = self.winfo_screenheight()
        # self.geometry("%dx%d+0+0" % (largura_screen, altura_screen))
        # self.title("Settings")
        self.after(100, self.lift)
        
        self.table = None
        self.buildUi()
        
        
    def loadMetas(self):
        if self.table and self.table.winfo_exists():
            self.table.destroy()
            
        url = f'http://localhost:5000/meta'
        
        headers = {"Authorization":f'{self.usuario["id"]}'}
        
        #Faz a requisição
        response = requests.get(url,headers=headers)
        headers = ["Nome", "Valor da Meta", "Data Limite", "Total Acumulado"]
        
        # Inicializa value com os cabeçalhos
        value = [headers]
        
        # Itera sobre as metas
        for meta in response.json():
            # Extrai os valores correspondentes para cada linha
            row = [
                meta['nome_meta'],
                meta['valor_meta'],
                meta['data_limite'],
                meta['valor_acumulado']
            ]
            # Adiciona a linha à lista value
            value.append(row)
            
        
            
        self.table = CTkTable(master=self, values=value)
        self.table.pack(fill="both", padx=20, pady=20)
        return True
    
            
    def buildUi(self):
        self.titulo = customtkinter.CTkLabel(self, text="Cadastrar nova meta", font=("Arial", 16))
        self.titulo.pack(padx=10, pady=10)
        
        self.input_frame = customtkinter.CTkFrame(self)
        self.input_frame.pack(fill='x')
        

        label_nome_meta = customtkinter.CTkLabel(self.input_frame, text="Nome da meta:")
        label_nome_meta.grid(row=0, column=0, padx=30, pady=5, sticky="w")
        
        label_valor_meta = customtkinter.CTkLabel(self.input_frame, text="Valor da meta:")
        label_valor_meta.grid(row=1, column=0, padx=30, pady=5, sticky="w")
        
        label_data_limite = customtkinter.CTkLabel(self.input_frame, text="Data Limite:")
        label_data_limite.grid(row=2, column=0, padx=30, pady=5, sticky="w")
        
        label_valor_acumulado = customtkinter.CTkLabel(self.input_frame, text="Total Acumulado:")
        label_valor_acumulado.grid(row=3, column=0, padx=30, pady=5, sticky="w")
        
        # Campos de entrada
        self.nome_meta = customtkinter.CTkEntry(self.input_frame, placeholder_text="Ex.: Viagem")
        self.nome_meta.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        self.valor_meta = customtkinter.CTkEntry(self.input_frame, placeholder_text="Ex.: 200.00")
        self.valor_meta.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        self.data_limite = customtkinter.CTkEntry(self.input_frame, placeholder_text="Ex.: 2024-09-01")
        self.data_limite.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        
        self.valor_acumulado = customtkinter.CTkEntry(self.input_frame, placeholder_text="Ex.: 50.00")
        self.valor_acumulado.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
        
        # Botão de adicionar
        self.adicionar = customtkinter.CTkButton(self.input_frame, text="Adicionar", command=self.adicionarMeta)
        self.adicionar.grid(row=4, columnspan=2, padx=10, pady=10)

        
        values = self.loadMetas()
        
    def adicionarMeta(self):
        url = f'http://localhost:5000/meta'
        data = {
            'usuario_id': self.usuario['id'],
            'nome_meta': self.nome_meta.get(),
            'valor_meta':self.valor_meta.get(),
            'data_limite':self.data_limite.get(),
            'valor_acumulado':self.valor_acumulado.get()
        }
        response = requests.post(url,data,timeout=10)
        if response.status_code == 200:
            self.loadMetas()
            CTkMessagebox(title="Meta cadastrada", message="Meta cadastrada com sucesso!!", icon="check")
            self.nome_meta.delete(0,customtkinter.END)
        else:
            erros = response.json()['errors']
            error_message = '\n'.join([f"{', '.join(msgs)}" for field, msgs in erros.items()])
            CTkMessagebox(title="Erro ao cadastrar meta", message=error_message, icon="cancel")