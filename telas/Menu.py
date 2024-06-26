import customtkinter
import requests
import json

class Categoria(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)     
        self.geometry("540x287")
        self.title("Settings")
        self.after(100, self.lift)
        
        self.adicionar = customtkinter.CTkButton(self, text="Adicionar",command=self.adicionarCategoria)
        self.adicionar.pack(padx=10,pady=10)
        values = self.loadCategorias()
        
        self.table = CTkTable(master=self, values=values)
        self.table.pack(fill="both", padx=20, pady=20)
        
    def loadCategorias(self):
        url = f'http://localhost:5000/categoria'

        #Faz a requisição
        response = requests.get(url)
        print(response.json())
        
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
        return value
        
        
            
    def adicionarCategoria(self):
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
        
    def saveBanco(self):
        print("aqui")
        #self.table.update_values(self.loadCategorias())