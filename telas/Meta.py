import customtkinter
import requests
from CTkTable import *
from CTkMessagebox import CTkMessagebox
from PIL import Image, ImageTk


class Meta(customtkinter.CTkFrame):
    def __init__(self,parent,usuario, *args, **kwargs):
        super().__init__(parent, *args, **kwargs) 
        self.usuario = usuario    
        largura_screen = self.winfo_screenwidth()
        altura_screen = self.winfo_screenheight()
        self.table = None
        self.buildUi()
        
        
    def loadMetas(self):
        if self.table and self.table.winfo_exists():
            self.table.destroy()
            
        url = f'http://localhost:5000/meta'
        
        headers = {"Authorization":f'{self.usuario["id"]}'}
        
        #Faz a requisição
        response = requests.get(url,headers=headers)
        headers = ['Id',"Nome", "Valor da Meta", "Data Limite", "Total Acumulado"]
        
        # Inicializa value com os cabeçalhos
        value = [headers]
        # Itera sobre as metas
        for meta in response.json():
            # Extrai os valores correspondentes para cada linha
            row = [
                meta['meta_id'],
                meta['nome_meta'],
                "R$ " + str(meta['valor_meta']),
                meta['data_limite'],
                "R$ " + str(meta['valor_acumulado'])
            ]
            # Adiciona a linha à lista value
            value.append(row)
            
        self.table = CTkTable(master=self, values=value, command=self.editarApagar)
        self.table.pack(fill="both", padx=20, pady=20)
        return True
    
            
    def buildUi(self):
        
        # Carregando ícone
        icon_path = r"C:\Users\Rafael\Desktop\teste interface\telas\icon\meta.png"  # Caminho correto do seu ícone
        icon_image = Image.open(icon_path)
        icon_image = icon_image.resize((50, 50), Image.LANCZOS)   # Redimensiona para o tamanho desejado
        icon_photo = ImageTk.PhotoImage(icon_image)

        self.titulo = customtkinter.CTkLabel(self, text="    Metas", font=("Arial", 20))
        self.titulo.pack(padx=10, pady=10)
      
        # Adicionando o ícone à label
        self.titulo.icon = icon_photo  # Mantém uma referência para evitar que a imagem seja limpa pela coleta de lixo
        self.titulo.configure(image=self.titulo.icon, compound="left")  # Define o ícone à esquerda do texto
        # self.titulo.place(x=10, y=10)
        
        self.titulo = customtkinter.CTkLabel(self, text="Cadastrar nova meta", font=("Arial", 16))
        self.titulo.pack(padx=10, pady=10)
        
        self.input_frame = customtkinter.CTkFrame(self)
        self.input_frame.pack(fill='y')

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
            
            
    def editarApagar(self,row):
        self.dados=self.table.select_row(row['row'])
        self.id_meta_edit=self.dados[0]
        
        self.janela_opcoes = customtkinter.CTkToplevel(self) 
        self.janela_opcoes.after(100, self.janela_opcoes.lift) 
        
        self.btn_adicionar_edit = customtkinter.CTkButton(self.janela_opcoes, text="Editar",command=self.janelaAtualizarMeta)
        self.btn_excluir_edit = customtkinter.CTkButton(self.janela_opcoes, text="Excluir",command=self.deletarMeta)
        self.btn_adicionar_edit.pack(padx=20,pady=10)
        self.btn_excluir_edit.pack(padx=20,pady=10)
       
    def janelaAtualizarMeta(self):
        self.janela_opcoes.destroy()
        self.formAdd = customtkinter.CTkToplevel(self) 
        self.formAdd.title("Editar Meta")
        self.formAdd.geometry("400x500")
        self.formAdd.after(100, self.formAdd.lift) 
        
        self.input_frame_edit = customtkinter.CTkFrame(self.formAdd)
        self.input_frame_edit.pack(padx=15, pady=15, fill="y")
        
        label_nome_meta_edit = customtkinter.CTkLabel(self.input_frame_edit, text="Nome da meta:")
        label_nome_meta_edit.grid(row=0, column=0, padx=30, pady=5, sticky="w")
        self.nome_meta_edit = customtkinter.CTkEntry(self.input_frame_edit, placeholder_text="Nome da meta")
        self.nome_meta_edit.insert(0, self.dados[1])
        self.nome_meta_edit.grid(row=1, column=0, padx=30, pady=5, sticky="w")
        
        label_valor_meta_edit = customtkinter.CTkLabel(self.input_frame_edit, text="Valor da meta:")
        label_valor_meta_edit.grid(row=2, column=0, padx=30, pady=5, sticky="w")
        self.saldo_meta_edit = customtkinter.CTkEntry(self.input_frame_edit, placeholder_text="Valor da meta")
        self.saldo_meta_edit.insert(0, self.dados[2].replace("R$",""))
        self.saldo_meta_edit.grid(row=3, column=0, padx=30, pady=5, sticky="w")
        
        label_data_meta_edit = customtkinter.CTkLabel(self.input_frame_edit, text="Data limite da meta:")
        label_data_meta_edit.grid(row=4, column=0, padx=30, pady=5, sticky="w")
        self.data_limite_edit = customtkinter.CTkEntry(self.input_frame_edit, placeholder_text="Data limite")
        self.data_limite_edit.insert(0, self.dados[3])
        self.data_limite_edit.grid(row=5, column=0, padx=30, pady=5, sticky="w")
        
        label_valor_acumulado_meta_edit = customtkinter.CTkLabel(self.input_frame_edit, text="Valor acumulado:")
        label_valor_acumulado_meta_edit.grid(row=6, column=0, padx=30, pady=5, sticky="w")
        self.total_acumulado_edit = customtkinter.CTkEntry(self.input_frame_edit, placeholder_text="Total acumulado")
        self.total_acumulado_edit.insert(0, self.dados[4].replace("R$",""))
        self.total_acumulado_edit.grid(row=7, column=0, padx=30, pady=5, sticky="w")
        
        self.adicionar_edit = customtkinter.CTkButton(self.input_frame_edit, text="Atualizar meta",command=self.atualizarMeta)
        self.adicionar_edit.grid(row=8, column=0, padx=30, pady=20, sticky="w")
                   
    def atualizarMeta(self):
        url = f'http://localhost:5000/meta/{self.id_meta_edit}'
        data = {
            'usuario_id': self.usuario['id'],
            'nome_meta':self.nome_meta_edit.get(),
            'valor_meta':self.saldo_meta_edit.get(),
            'data_limite':self.data_limite_edit.get(),
            'valor_acumulado':self.total_acumulado_edit.get()
        }
        response = requests.put(url,data)
        if response.status_code == 200:
            self.loadMetas()
            CTkMessagebox(title="Meta atualizada", message="Meta atualizada com sucesso!!", icon="info")
            self.formAdd.destroy()
        else:
            erros = response.json()['errors']
            error_message = '\n'.join([f"{', '.join(msgs)}" for field, msgs in erros.items()])
            CTkMessagebox(title="Erro ao atualizado Meta", message=error_message, icon="cancel")
            
    def deletarMeta(self):
        url = f'http://localhost:5000/meta/{self.id_meta_edit}'

        response = requests.delete(url)
        if response.status_code == 200:
            self.loadMetas()
            CTkMessagebox(title="Meta excluída", message="Meta excluída com sucesso!!", icon="cancel")
            self.janela_opcoes.destroy()
        else:
            erros = response.json()['errors']
            error_message = '\n'.join([f"{', '.join(msgs)}" for field, msgs in erros.items()])
            CTkMessagebox(title="Erro ao excluír Meta", message=error_message, icon="cancel")