from tkinter import *

menu = Tk()
menu.title('Titulo')

#dimensoes da janela
largura = 500
altura = 300

# resolução do sistema

largura_screen = menu.winfo_screenwidth()
altura_screen = menu.winfo_screenheight()

#posicionamento da janela
posx = largura_screen/2 - largura/2
posy = altura_screen/2 - altura/2

#definir geometry
menu.geometry("%dx%d+%d+%d" % (largura, altura, posx, posy))

menu.mainloop()