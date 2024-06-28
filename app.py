from tkinter import Frame
import customtkinter
import requests
from CTkTable import *
from CTkMessagebox import CTkMessagebox
from telas import *
from PIL import Image, ImageTk

class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.usuario = {"id":16,"nome":123}
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
        self.janela_conta = None
        self.janela_transacao = None
        
        # Caminhos dos ícones
        icon_categoria_path = r"C:\Users\Rafael\Desktop\teste interface\telas\icon\categoria.png"
        icon_meta_path = r"C:\Users\Rafael\Desktop\teste interface\telas\icon\meta.png"
        icon_conta_path = r"C:\Users\Rafael\Desktop\teste interface\telas\icon\conta.png"
        icon_transacao_path = r"C:\Users\Rafael\Desktop\teste interface\telas\icon\transacao.png"
        icon_icon_path = r"C:\Users\Rafael\Desktop\teste interface\telas\icon\1.png"
        
        # Carregar ícones
        icon_categoria = Image.open(icon_categoria_path).resize((30, 30), Image.LANCZOS)
        icon_icon = Image.open(icon_icon_path).resize((70, 70), Image.LANCZOS)
        
        # Converter ícones para ImageTk.PhotoImage
        self.icon_categoria_photo = ImageTk.PhotoImage(icon_categoria)
        self.icon_icon_photo = ImageTk.PhotoImage(icon_icon)
        

        # self.titulo.place(x=10, y=10)
        
        # Criar um frame para o menu lateral
        self.menu_lateral = Frame(self, bg="lightgray", width=300, height=self.winfo_height())
        self.menu_lateral.pack(side="left", fill="y")
        
        self.titulo = customtkinter.CTkLabel(self.menu_lateral, image=self.icon_icon_photo, compound="left", font=("Arial", 18))
        self.titulo.pack(padx=10, pady=30)
        
        #Gerenciamento de categorias botão
        self.categoria_btn = customtkinter.CTkButton(self.menu_lateral, image=self.icon_categoria_photo, compound="left", text="Categoria",command=self.categorias)
        self.categoria_btn.pack(padx=10, pady=10)
        self.meta_btn = customtkinter.CTkButton(self.menu_lateral, image=self.icon_categoria_photo, compound="left", text="Meta",command=self.metas)
        self.meta_btn.pack(side="top", padx=10, pady=10)
        self.conta_btn = customtkinter.CTkButton(self.menu_lateral, image=self.icon_categoria_photo, compound="left", text="Conta",command=self.contas)
        self.conta_btn.pack(side="top", padx=10, pady=10)
        self.transacao_btn = customtkinter.CTkButton(self.menu_lateral, image=self.icon_categoria_photo, compound="left", 
                                                     text="Transação",command=self.transacoes)
        self.transacao_btn.pack(side="top", padx=10, pady=10)
        
         # Frame para conteúdo principal
        self.conteudo_principal = Frame(self, bg="white", width=self.winfo_width(), height=self.winfo_height())
        self.conteudo_principal.pack(side="left", fill="both", expand=True)
        
        
        self.loginWindow()
        

    # Chamar a janela de login
    def loginWindow(self):
        self.withdraw()
        self.janela_login = Login(self, self.onLoginSuccess)
        self.janela_login.protocol("WM_DELETE_WINDOW", lambda: self.destroy())

    # Função a ser chamada se o login for executado com sucesso
    def onLoginSuccess(self,usuario):
        self.usuario={"id":usuario["usuario_id"], "nome":usuario["nome"]}
        # self.usuario = usuario
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
            
    def contas(self):
        if self.janela_conta is None or not self.janela_conta.winfo_exists():
            # Limpar o conteúdo atual do frame de conteúdo principal
            for widget in self.conteudo_principal.winfo_children():
                widget.destroy()
            
            # Adicionar o conteúdo da tela Conta ao frame de conteúdo principal
            self.janela_conta = Conta(self.conteudo_principal,self.usuario)
            self.janela_conta.pack(fill="both", expand=True)
    
    def transacoes(self):
        if self.janela_transacao is None or not self.janela_transacao.winfo_exists():
            # Limpar o conteúdo atual do frame de conteúdo principal
            for widget in self.conteudo_principal.winfo_children():
                widget.destroy()
            self.janela_transacao = Transacao(self.conteudo_principal,self.usuario)
            self.janela_transacao.pack(fill="both", expand=True)
        
app = App()
app.mainloop()
