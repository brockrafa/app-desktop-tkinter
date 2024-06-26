from tkinter import *

class MyApp(Tk):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.title('Titulo')

        # Dimensões desejadas da janela
        largura = 800
        altura = 600

        # Resolução do sistema
        largura_screen = self.winfo_screenwidth()
        altura_screen = self.winfo_screenheight()

        # Posicionamento da janela no centro da tela
        posx = (largura_screen - largura) // 2
        posy = (altura_screen - altura) // 2

        # Definir geometry para centralizar a janela
        self.geometry("%dx%d+%d+%d" % (largura, altura, posx, posy))

        # Chamar o método para construir a UI
        self.build_ui()

        # Trazer a janela para frente
        self.after(100, self.lift)

    def build_ui(self):
        # Criar um frame para o menu lateral
        menu_lateral = Frame(self, bg="lightgray", width=200, height=self.winfo_height())
        menu_lateral.pack(side="left", fill="y")

        # Adicionar botões ao menu lateral
        btn1 = Button(menu_lateral, text="Botão 1", command=self.on_button_click)
        btn1.pack(pady=10, padx=10, fill="x")

        btn2 = Button(menu_lateral, text="Botão 2", command=self.on_button_click)
        btn2.pack(pady=10, padx=10, fill="x")

        btn3 = Button(menu_lateral, text="Botão 3", command=self.on_button_click)
        btn3.pack(pady=10, padx=10, fill="x")

        # Criar um frame para o conteúdo principal
        conteudo_principal = Frame(self, bg="white")
        conteudo_principal.pack(side="right", fill="both", expand=True)

        # Adicionar conteúdo ao frame principal
        label = Label(conteudo_principal, text="Conteúdo Principal", bg="white")
        label.pack(pady=20, padx=20)

    def on_button_click(self):
        print("Botão clicado!")

if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
