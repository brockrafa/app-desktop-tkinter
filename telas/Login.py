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

        checkbox = customtkinter.CTkCheckBox(self, text="Lembrar Login")
        checkbox.pack(padx=10, pady=10)
        
        # self.button_2 = customtkinter.CTkButton(self, text="fff toplevel", command=self.open_toplevel)
        # self.button_2.pack(side="top", padx=20, pady=20)
    
    def login(self):    
        self.destroy()
        self.onLoginSuccess({'id':1,'nome':"Rafael","emai":"rafael@hotmail.com"})
        pass
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
            self.onLoginSuccess(usuario)
        else:
            CTkMessagebox(title="Usuário invalido", message="Não foi possivel encontrar um usuário com as credenciais informadas", icon="cancel")

