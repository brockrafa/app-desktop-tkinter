from tkinter import Frame
import customtkinter
import requests
from CTkTable import *
from CTkMessagebox import CTkMessagebox
from telas import *

class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usuario = {"id":2,"nome":123}
        self.autenticado = False  # Estado inicial: não autenticado
        
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")  
            
         # Obter largura e altura da tela do sistema
        largura_screen = self.winfo_screenwidth()
        altura_screen = self.winfo_screenheight()
        
        # Definir geometria da janela principal
        self.geometry(f"{largura_screen}x{altura_screen}+0+0")    
        # self.geometry("800x400")
        
        self.janela_categoria = None
        self.janela_meta = None
        
        # Criar um frame para o menu lateral
        self.menu_lateral = Frame(self, bg="lightgray", width=300, height=self.winfo_height())
        self.menu_lateral.pack(side="left", fill="y")
        
        #Gerenciamento de categorias botão
        self.categoria_btn = customtkinter.CTkButton(self.menu_lateral, text="Categoria",command=self.categorias)
        self.categoria_btn.pack(padx=10, pady=10)
        self.meta_btn = customtkinter.CTkButton(self.menu_lateral, text="Meta",command=self.metas)
        self.meta_btn.pack(side="top", padx=10, pady=10)
        
         # Frame para conteúdo principal
        self.conteudo_principal = Frame(self, bg="white", width=self.winfo_width(), height=self.winfo_height())
        self.conteudo_principal.pack(side="left", fill="both", expand=True)
        
        
        #self.loginWindow()

    # Chamar a janela de login
    def loginWindow(self):
        self.withdraw()
        self.janela_login = Login(self, self.onLoginSuccess)
        self.janela_login.protocol("WM_DELETE_WINDOW", lambda: self.destroy())

    # Função a ser chamada se o login for executado com sucesso
    def onLoginSuccess(self,usuario):
        self.usuarioLogado = usuario
        self.autenticado = True
        self.deiconify()
        
    def categorias(self):
        if self.janela_categoria is None or not self.janela_categoria.winfo_exists():
            # Limpar o conteúdo atual do frame de conteúdo principal
            for widget in self.conteudo_principal.winfo_children():
                widget.destroy()
            self.janela_categoria = Categoria(self.conteudo_principal,self.usuario)
            self.janela_categoria.pack(fill="both", expand=True)
            
    def metas(self):
        if self.janela_meta is None or not self.janela_meta.winfo_exists():
            # Limpar o conteúdo atual do frame de conteúdo principal
            for widget in self.conteudo_principal.winfo_children():
                widget.destroy()
            
            # Adicionar o conteúdo da tela Meta ao frame de conteúdo principal
            self.janela_meta = Meta(self.conteudo_principal,self.usuario)
            self.janela_meta.pack(fill="both", expand=True)
        
app = App()
app.mainloop()
