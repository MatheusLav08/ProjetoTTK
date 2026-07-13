from abc import ABC, abstractmethod
from tkinter import *
from tkinter import ttk
from tkinter import colorchooser

class Figuras(ABC):
    def __init__(self, valor_x, valor_y, valor_xf=0, valor_yf=0):
        self.valor_x = valor_x
        self.valor_y = valor_y
        self.valor_xf = valor_xf
        self.valor_yf = valor_yf

class Linha(Figuras):
    def __init__(self, valor_x, valor_y, valor_xf, valor_yf):
        super().__init__(valor_x, valor_y, valor_xf, valor_yf)

class Rabisco(Figuras):
    def __init__(self, lista):
        # Rabisco guarda uma lista linear de coordenadas: [x1, y1, x2, y2, ...]
        self.lista = lista

class Retângulo(Figuras):
    def __init__(self, valor_x, valor_y, valor_xf, valor_yf):
        super().__init__(valor_x, valor_y, valor_xf, valor_yf)

class Círculo(Figuras):
    def __init__(self, valor_x, valor_y, raio):
        super().__init__(valor_x, valor_y)
        self.raio = raio

class Oval(Figuras):
    def __init__(self, valor_x, valor_y, valor_xf, valor_yf):
        super().__init__(valor_x, valor_y, valor_xf, valor_yf)


# Quando mouse é pressionado
def iniciar_figura_nova(event): 
    global figura_nova, cor_contorno, cor_preenchimento
    
    ferramenta = tipo_figura_var.get()
    
    if ferramenta == 'Linha':
        figura = Linha(event.x, event.y, event.x, event.y)
    elif ferramenta == 'Retângulo':
        figura = Retângulo(event.x, event.y, event.x, event.y)
    elif ferramenta == 'Oval':
        figura = Oval(event.x, event.y, event.x, event.y)
    elif ferramenta == 'Círculo (Centro)':
        figura = Círculo(event.x, event.y, 0)
    else: # Rabisco
        figura = Rabisco([event.x, event.y])
        
    figura_nova = (figura, cor_contorno, cor_preenchimento)

# Quando mouse é movido com o botão pressionado
def atualizar_figura_nova(event):
    global figura_nova
    if not figura_nova:
        return
        
    figura, c_contorno, c_preench = figura_nova[0], figura_nova[1], figura_nova[2]
    nome_classe = type(figura).__name__
    
    if nome_classe == "Rabisco":
        figura.lista.append(event.x)
        figura.lista.append(event.y)
        figura_nova = (Rabisco(figura.lista), c_contorno, c_preench)
    elif nome_classe == "Retângulo":
        figura_nova = (Retângulo(figura.valor_x, figura.valor_y, event.x, event.y), c_contorno, c_preench)
    elif nome_classe == "Oval":
        figura_nova = (Oval(figura.valor_x, figura.valor_y, event.x, event.y), c_contorno, c_preench)
    elif nome_classe == "Linha":
        figura_nova = (Linha(figura.valor_x, figura.valor_y, event.x, event.y), c_contorno, c_preench)
    elif nome_classe == "Círculo":
        ini_x, ini_y = figura.valor_x, figura.valor_y
        raio = ((ini_x - event.x)**2 + (ini_y - event.y)**2) ** 0.5
        figura_nova = (Círculo(ini_x, ini_y, raio), c_contorno, c_preench)
        
    desenhar_figuras()
    desenhar_figura_nova()

# Quando mouse é solto
def incluir_figura_nova(event): 
    global figura_nova
    if figura_nova:
        figura = figura_nova[0]
        if figura and not incompleta(figura): 
            figuras.append(figura_nova) 
    figura_nova = None
    desenhar_figuras()

def desenhar_figuras():
    canvas.delete("all")
    for figura_salva in figuras:
        fig, c_contorno, c_preench = figura_salva[0], figura_salva[1], figura_salva[2]
        nome_classe = type(fig).__name__
        
        if nome_classe == "Linha":
            canvas.create_line(fig.valor_x, fig.valor_y, fig.valor_xf, fig.valor_yf, fill=c_contorno)
        elif nome_classe == "Retângulo":
            canvas.create_rectangle(fig.valor_x, fig.valor_y, fig.valor_xf, fig.valor_yf, outline=c_contorno, fill=c_preench)
        elif nome_classe == "Oval":
            canvas.create_oval(fig.valor_x, fig.valor_y, fig.valor_xf, fig.valor_yf, outline=c_contorno, fill=c_preench)
        elif nome_classe == "Círculo":
            x, y, r = fig.valor_x, fig.valor_y, fig.raio
            canvas.create_oval(x-r, y-r, x+r, y+r, outline=c_contorno, fill=c_preench)
        elif nome_classe == "Rabisco":
            if len(fig.lista) >= 4: # Precisa de pelo menos 2 pontos (x1, y1, x2, y2) para desenhar uma linha
                canvas.create_line(fig.lista, fill=c_contorno)

def desenhar_figura_nova():
    if not figura_nova:
        return
    fig, c_contorno, c_preench = figura_nova[0], figura_nova[1], figura_nova[2]
    nome_classe = type(fig).__name__
    
    if nome_classe == "Linha":
        canvas.create_line(fig.valor_x, fig.valor_y, fig.valor_xf, fig.valor_yf, dash=(4, 2), fill=c_contorno)
    elif nome_classe == "Retângulo":
        canvas.create_rectangle(fig.valor_x, fig.valor_y, fig.valor_xf, fig.valor_yf, dash=(4, 2), outline=c_contorno, fill=c_preench)
    elif nome_classe == "Oval":
        canvas.create_oval(fig.valor_x, fig.valor_y, fig.valor_xf, fig.valor_yf, dash=(4, 2), outline=c_contorno, fill=c_preench)
    elif nome_classe == "Círculo":
        x, y, r = fig.valor_x, fig.valor_y, fig.raio
        canvas.create_oval(x-r, y-r, x+r, y+r, dash=(4, 2), outline=c_contorno, fill=c_preench)
    elif nome_classe == "Rabisco":
        if len(fig.lista) >= 4:
            canvas.create_line(fig.lista, dash=(4, 2), fill=c_contorno)

def incompleta(figura):
    nome_classe = type(figura).__name__
    if nome_classe in ["Linha", "Retângulo", "Oval"]:
        return (figura.valor_x == figura.valor_xf) and (figura.valor_y == figura.valor_yf)
    elif nome_classe == "Círculo":
        return figura.raio <= 0
    elif nome_classe == "Rabisco":
        return len(figura.lista) <= 2
    return False

# Escolha de cores
def mudar_cor(modo):
    global cor_contorno, cor_preenchimento
    cor = colorchooser.askcolor(title="Escolha a cor")
    if cor[1]: 
        if modo == "contorno":
            cor_contorno = cor[1]
        elif modo == "preenchimento":
            cor_preenchimento = cor[1]

#******* MAIN *******#

figuras = []       # Todas as figuras definitivas salvas
figura_nova = None # Figura temporária que está sendo arrastada

# Cores padrão iniciais
cor_contorno = "#000000"       # Preto por padrão
cor_preenchimento = ""         # Vazio (transparente) por padrão

root = Tk()
root.title("Paint Integrado - Linhas, Formas e Círculos")
frame = Frame(root)

paddings = {'padx': 5, 'pady': 5} 

# Label descritivo
label = ttk.Label(frame, text='Selecione a ferramenta de desenho:')
label.grid(column=0, row=0, sticky=W, **paddings)

# Menu de opções atualizado com a nova ferramenta de círculo
tipo_figura_var = StringVar(root)
tipo_figura_var.set('Linha') # Define o valor inicial visível do menu
option_menu = ttk.OptionMenu(frame, tipo_figura_var, 'Linha', 'Linha', 'Rabisco', 'Retângulo', 'Oval', 'Círculo (Centro)')
option_menu.grid(column=1, row=0, sticky=W, **paddings)

# Botões de paleta de cores
btn_outline = ttk.Button(frame, text='Cor de Contorno', command=lambda: mudar_cor("contorno"))
btn_fill = ttk.Button(frame, text='Cor de Preenchimento', command=lambda: mudar_cor("preenchimento"))
btn_outline.grid(column=2, row=0, sticky=W, **paddings)
btn_fill.grid(column=3, row=0, sticky=W, **paddings)

# Área de desenho padronizada para tamanho grande
canvas = Canvas(frame, bg='white', width=1280, height=720)
canvas.grid(column=0, row=1, columnspan=4, sticky=W, **paddings)

frame.pack()

# Eventos do mouse unificados
canvas.bind('<ButtonPress-1>', iniciar_figura_nova)
canvas.bind('<B1-Motion>', atualizar_figura_nova)
canvas.bind('<ButtonRelease-1>', incluir_figura_nova)

root.mainloop()