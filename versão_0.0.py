from tkinter import *
from tkinter import ttk
from tkinter import colorchooser

cor_contorno = 'black'       # Cor padrão do contorno
cor_preenchimento = 'white'   # Cor padrão do preenchimento

# Quando mouse é pressionado
def iniciar_figura_nova(event): 
    global figura_nova
    
    tipo = tipo_figura_var.get()
    
    if tipo == 'Linha':
        figura_nova = ("linha", (event.x, event.y, event.x, event.y), cor_contorno, cor_preenchimento)
    elif tipo == 'Retângulo':
        figura_nova = ("retangulo", (event.x, event.y, event.x, event.y), cor_contorno, cor_preenchimento)
    elif tipo == 'Oval':
        figura_nova = ("oval", (event.x, event.y, event.x, event.y), cor_contorno, cor_preenchimento)
    elif tipo == 'Círculo (Centro)':
        # Guarda o centro (x, y) e o raio inicial (0)
        figura_nova = ("circulo", (event.x, event.y, 0), cor_contorno, cor_preenchimento)
    else:
        figura_nova = ("rabisco", [(event.x, event.y)], cor_contorno, cor_preenchimento)

# Quando mouse é movido com o botão pressionado
def atualizar_figura_nova(event):
    global figura_nova
    if not figura_nova:
        return
        
    tipo, valores, c_contorno, c_preench = figura_nova
    
    if tipo == "rabisco":
        valores.append((event.x, event.y))
        figura_nova = (tipo, valores, c_contorno, c_preench)
    elif tipo == "retangulo":
        figura_nova = ("retangulo", (valores[0], valores[1], event.x, event.y), c_contorno, c_preench)
    elif tipo == "oval":
        figura_nova = ("oval", (valores[0], valores[1], event.x, event.y), c_contorno, c_preench)
    elif tipo == "linha":
        figura_nova = ("linha", (valores[0], valores[1], event.x, event.y), c_contorno, c_preench)
    elif tipo == "circulo":
        # Calcula o raio baseado na distância geométrica do clique inicial até o mouse
        ini_x, ini_y = valores[0], valores[1]
        raio = ((ini_x - event.x)**2 + (ini_y - event.y)**2) ** 0.5
        figura_nova = ("circulo", (ini_x, ini_y, raio), c_contorno, c_preench)
        
    desenhar_figuras()
    desenhar_figura_nova()

# Quando mouse é solto
def incluir_figura_nova(event): 
    global figura_nova
    if figura_nova and not incompleta(figura_nova): 
        figuras.append(figura_nova) 
    figura_nova = None
    desenhar_figuras()

def desenhar_figuras():
    canvas.delete("all")
    for fig, values, c_contorno, c_preench in figuras:
        if fig == "linha":
            canvas.create_line(values[0], values[1], values[2], values[3], fill=c_contorno)
        elif fig == "retangulo":
            canvas.create_rectangle(values[0], values[1], values[2], values[3], outline=c_contorno, fill=c_preench)
        elif fig == "oval":
            canvas.create_oval(values[0], values[1], values[2], values[3], outline=c_contorno, fill=c_preench)
        elif fig == "circulo":
            x, y, r = values
            canvas.create_oval(x-r, y-r, x+r, y+r, outline=c_contorno, fill=c_preench)
        else: # rabisco
            canvas.create_line(values, fill=c_contorno)

def desenhar_figura_nova():
    if not figura_nova:
        return
    fig, values, c_contorno, c_preench = figura_nova
    if fig == "linha":
        canvas.create_line(values[0], values[1], values[2], values[3], dash=(4, 2), fill=c_contorno)
    elif fig == "retangulo":
        canvas.create_rectangle(values[0], values[1], values[2], values[3], dash=(4, 2), outline=c_contorno, fill=c_preench)
    elif fig == "oval":
        canvas.create_oval(values[0], values[1], values[2], values[3], dash=(4, 2), outline=c_contorno, fill=c_preench)
    elif fig == "circulo":
        x, y, r = values
        canvas.create_oval(x-r, y-r, x+r, y+r, dash=(4, 2), outline=c_contorno, fill=c_preench)
    else: # rabisco
        canvas.create_line(values, dash=(4, 2), fill=c_contorno)

def incompleta(figura):
    fig, values, _, _ = figura
    if fig in ["linha", "retangulo", "oval"]:
        return (values[0], values[1]) == (values[2], values[3])
    elif fig == "circulo":
        return values[2] <= 0 # Incompleto se o raio for zero
    else: # rabisco
        return len(values) <= 1

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

root = Tk()
root.title("Paint Integrado - Linhas, Formas e Círculos")
frame = Frame(root)

paddings = {'padx': 5, 'pady': 5} 

# Label descritivo
label = ttk.Label(frame, text='Selecione a ferramenta de desenho:')
label.grid(column=0, row=0, sticky=W, **paddings)

# Menu de opções atualizado com a nova ferramenta de círculo
tipo_figura_var = StringVar(root)
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
