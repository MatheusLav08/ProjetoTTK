from tkinter import *
from tkinter import ttk
from tkinter import colorchooser

cor_contorno = 'black' # cor padrão do contorno
cor_preenchimento = 'black' # cor padrão do preenchimento

# Quando mouse é pressionado
def iniciar_figura_nova(event): 
    global figura_nova
    if tipo_figura_var.get() == 'Linha':
        figura_nova = ("linha", (event.x, event.y, event.x, event.y), cor_preenchimento, cor_contorno)
    elif tipo_figura_var.get() == 'Retângulo':
        figura_nova = ("retangulo", (event.x, event.y, event.x, event.y), cor_preenchimento, cor_contorno)
    else :
        figura_nova = ("rabisco", [(event.x, event.y)], cor_preenchimento, cor_contorno )

# Quando mouse é movido com o botão pressionado
def atualizar_figura_nova(event):
    global figura_nova
    tipo, valores, c_contorno, c_preench = figura_nova
    
    if figura_nova[0] == "rabisco":
        figura_nova[1].append((event.x, event.y))
        figura_nova = (tipo, valores, c_contorno, c_preench)
    elif figura_nova[0] == "retangulo":
        figura_nova = ("retangulo", (figura_nova[1][0], figura_nova[1][1], event.x, event.y), c_contorno, c_preench)
    else : # figura_nova[0] == "linha"
        figura_nova = ("linha", (figura_nova[1][0], figura_nova[1][1], event.x, event.y), c_contorno, c_preench)
    desenhar_figuras()
    desenhar_figura_nova()

# Quando mouse é solto
def incluir_figura_nova(event): 
    if not incompleta(figura_nova): # para evitar incluir figuras incompletas, como uma linha sem comprimento ou um rabisco com um único ponto
        figuras.append(figura_nova) 
    desenhar_figuras()

def desenhar_figuras():
    canvas.delete("all")
    for fig, values, c_contorno, c_preench in figuras:
        if fig == "linha":
            canvas.create_line(values[0], values[1], values[2], values[3], fill = c_contorno)
        elif fig == "retangulo":
            canvas.create_rectangle(values[0], values[1], values[2], values[3], fill = c_contorno)
        else : # fig == "rabisco"
            canvas.create_line(values, fill = c_contorno)

def desenhar_figura_nova():
    fig, values, c_contorno, c_preench = figura_nova
    if fig == "linha":
        canvas.create_line(values[0], values[1], values[2], values[3], dash=(4, 2), fill = c_contorno)
    elif fig == "retangulo":
        canvas.create_rectangle(values[0], values[1], values[2], values[3], dash=(4, 2), fill = c_contorno)
    else : # fig == "rabisco"
        canvas.create_line(values, dash=(4, 2), fill = c_contorno)

def incompleta(figura):
    fig, values, _, _ = figura
    if fig == "linha":
        return (values[0], values[1]) == (values[2], values[3])
    elif fig == "retangulo":
        return (values[0], values[1]) == (values[2], values[3])
    else : # fig == "rabisco"
        return len(values) <= 1

# escolha de cores
def mudar_cor(modo):
    global cor_contorno, cor_preenchimento
    cor = colorchooser.askcolor(title="Escolha a cor")
    if cor[1]: 
        if modo == "contorno":
            cor_contorno = cor[1]
        elif modo == "preenchimento":
            cor_preenchimento = cor[1]


#******* MAIN *******#

figuras = []       # Todas as figuras desenhadas
figura_nova = None # Figura que está sendo desenhada, mas ainda não foi incluída em figuras

root = Tk()
frame = Frame(root)

# Widgets arranjados com Layout grid dentro de frame
paddings = {'padx': 5, 'pady': 5} 

# label
label = ttk.Label(frame,  text='Linha, Rabisco ou Retângulo com cores:')
label.grid(column=0, row=0, sticky=W, **paddings)

# option menu
tipo_figura_var = StringVar(root) # Guarda o tipo de figura selecionado no option menu (linha ou rabisco)
option_menu = ttk.OptionMenu(frame, tipo_figura_var,
                             'Linha', 'Linha', 'Rabisco', 'Retângulo')
option_menu.grid(column=1, row=0, sticky=W, **paddings)

#botões de escolha de cor
option_menu_color_outline = ttk.Button(frame, text='Escolher cor de cortorno', command=lambda: mudar_cor("contorno"))
option_menu_color_fill = ttk.Button(frame, text='Escolher cor de preenchimento', command=lambda: mudar_cor("preenchimento"))
option_menu_color_outline.grid(column=2, row=0, sticky=W, **paddings)
option_menu_color_fill.grid(column=3, row=0, sticky=W, **paddings)

# Área de desenho
canvas = Canvas(frame, bg='white', width=1280, height=720)
canvas.grid(column=0, row=1, columnspan=4, sticky=W, **paddings)

frame.pack()

# Eventos de mouse associados ao canvas - com seus callbacks
canvas.bind('<ButtonPress-1>', iniciar_figura_nova)
canvas.bind('<B1-Motion>', atualizar_figura_nova)
canvas.bind('<ButtonRelease-1>', incluir_figura_nova)

root.mainloop()
