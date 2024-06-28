import customtkinter
import requests
from CTkMessagebox import CTkMessagebox
import json

class Login(customtkinter.CTkToplevel):
    def __init__(self, parent,onLoginSuccess, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.onLoginSuccess = onLoginSuccess
        
        self.geometry("540x287")
        self.title("Realizar Login")
        
        self.after(100, self.lift)  # Workaround for bug where main window takes focus
        
        self.texto = customtkinter.CTkLabel(self, text="Fazer Login", font=("Arial", 18))
        self.texto.pack(padx=10, pady=10)
        
        self.email = customtkinter.CTkEntry(self, placeholder_text="joao@email.com")
        self.email.pack(padx=10, pady=10)

        self.senha = customtkinter.CTkEntry(self, placeholder_text="***********", show="*")
        self.senha.pack(padx=10, pady=10)

        self.botao = customtkinter.CTkButton(self, text="Login", command=self.login)
        self.botao.pack(padx=10, pady=10)

        self.botao_cadastro = customtkinter.CTkButton(self, text="Registre-se", command=self.janelaRegistrar,fg_color="#cc0000",hover_color="#ff0000")
        self.botao_cadastro.pack(padx=10, pady=10)
        
        # self.button_2 = customtkinter.CTkButton(self, text="fff toplevel", command=self.open_toplevel)
        # self.button_2.pack(side="top", padx=20, pady=20)
    
    def janelaRegistrar(self):
        self.formAdd = customtkinter.CTkToplevel(self) 
        self.formAdd.title("Registrar usuario")
        self.formAdd.after(100, self.formAdd.lift) 
        self.formAdd.geometry("400x350")
        
        self.input_frame_edit = customtkinter.CTkFrame(self.formAdd)
        self.input_frame_edit.pack(padx=15, pady=15, fill="y")
        
        label_nome_usuario_edit = customtkinter.CTkLabel(self.input_frame_edit, text="Nome de usuario:")
        label_nome_usuario_edit.grid(row=0, column=0, padx=30, pady=5, sticky="w")
        self.nome_usuario_edit = customtkinter.CTkEntry(self.input_frame_edit, placeholder_text="Nome de usuario")
        self.nome_usuario_edit.grid(row=1, column=0, padx=30, pady=5, sticky="w")
        
        label_email_usuario_edit = customtkinter.CTkLabel(self.input_frame_edit, text="Email:")
        label_email_usuario_edit.grid(row=2, column=0, padx=30, pady=5, sticky="w")
        self.email_usuario_edit = customtkinter.CTkEntry(self.input_frame_edit, placeholder_text="Email")
        self.email_usuario_edit.grid(row=3, column=0, padx=30, pady=5, sticky="w")
        
        label_senha_edit = customtkinter.CTkLabel(self.input_frame_edit, text="Senha:")
        label_senha_edit.grid(row=4, column=0, padx=30, pady=5, sticky="w")
        self.senha_edit = customtkinter.CTkEntry(self.input_frame_edit, placeholder_text="senha")
        self.senha_edit.grid(row=5, column=0, padx=30, pady=5, sticky="w")
        
        self.botao_cadastro_edit = customtkinter.CTkButton(self.input_frame_edit, text="Registre-se", command=self.registrar)
        self.botao_cadastro_edit.grid(row=6, column=0, padx=30, pady=20, sticky="w")
        
        
    def registrar(self):
        url = f'http://localhost:5000/usuario'
        data = {
            'nome': self.nome_usuario_edit.get(),
            'email': self.email_usuario_edit.get(),
            'senha':self.senha_edit.get() 
        }
        response = requests.post(url,data)
        if response.status_code == 200:
            CTkMessagebox(title="Usuario cadastrado", message="Usuario cadastrado com sucesso!!", icon="check")
            self.formAdd.destroy()
        else:
            erros = response.json()['errors']
            error_message = '\n'.join([f"{', '.join(msgs)}" for field, msgs in erros.items()])
            CTkMessagebox(title="Erro ao cadastrar usuario", message=error_message, icon="cancel")
            
            
    def login(self):    
        # self.destroy()
        # self.onLoginSuccess({'id':1,'nome':"Rafael","emai":"rafael@hotmail.com"})
        # pass
        url = f'http://localhost:5000/usuario/login'
        data = {
            "email":self.email.get(),
            'senha':self.senha.get()
        }

        #Faz a requisição
        response = requests.post(url,data)
        
        if response.status_code == 200:
            usuario = response.json()
            self.destroy()
            self.onLoginSuccess(usuario["usuario"])
        else:
            CTkMessagebox(title="Usuário invalido", message="Não foi possivel encontrar um usuário com as credenciais informadas", icon="cancel")

