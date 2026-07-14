# main.py
from tkinter import *
from tkinter import ttk, colorchooser

# Importa as classes e funções necessárias do nosso módulo local
from figuras import Linha, Rabisco, Retângulo, Círculo, Oval, Poligono
# Função auxiliar para o fechamento do polígono baseado na distância do ponto inicial
def perto_do_inicio(ponto, inicio, tol=30):
    return ((ponto[0] - inicio[0]) ** 2 + (ponto[1] - inicio[1]) ** 2) ** 0.5 <= tol


# Quando mouse é pressionado
def iniciar_figura_nova(event):
    global figura_nova, ponto_previo_poligono
    ferramenta = tipo_figura_var.get()
    
    if ferramenta == 'Linha':
        fig = Linha(event.x, event.y, event.x, event.y)
    elif ferramenta == 'Retângulo':
        fig = Retângulo(event.x, event.y, event.x, event.y)
    elif ferramenta == 'Oval':
        fig = Oval(event.x, event.y, event.x, event.y)
    elif ferramenta == 'Círculo (Centro)':
        fig = Círculo(event.x, event.y, 0)
    elif ferramenta == 'Polígono':
        # Cada clique fixa um novo vértice do polígono.
        if figura_nova and type(figura_nova[0]).__name__ == 'Poligono':
            fig = figura_nova[0]
            if len(fig.pontos) >= 3 and perto_do_inicio((event.x, event.y), fig.pontos[0]):
                if fig.fechar():
                    figuras.append((fig, cor_contorno, cor_preenchimento))
                    figura_nova = None
                    ponto_previo_poligono = None
                    desenhar_figuras()
                    return
                ponto_previo_poligono = None
                desenhar_figuras()
                desenhar_figura_nova()
                return
            fig.adicionar((event.x, event.y))
        else:
            fig = Poligono([(event.x, event.y)])
        ponto_previo_poligono = None
    else:
        fig = Rabisco([event.x, event.y])
        
    figura_nova = (fig, cor_contorno, cor_preenchimento)
    desenhar_figuras()
    desenhar_figura_nova()


# Quando mouse é movido com o botão pressionado
def atualizar_figura_nova(event):
    global figura_nova, ponto_previo_poligono
    if not figura_nova:
        return
    fig, c_contorno, c_preench = figura_nova[0], figura_nova[1], figura_nova[2]
    nome = type(fig).__name__
    
    if nome == 'Rabisco':
        fig.lista.extend([event.x, event.y])
        figura_nova = (Rabisco(fig.lista), c_contorno, c_preench)
    elif nome == 'Retângulo':
        figura_nova = (Retângulo(fig.valor_x, fig.valor_y, event.x, event.y), c_contorno, c_preench)
    elif nome == 'Oval':
        figura_nova = (Oval(fig.valor_x, fig.valor_y, event.x, event.y), c_contorno, c_preench)
    elif nome == 'Linha':
        figura_nova = (Linha(fig.valor_x, fig.valor_y, event.x, event.y), c_contorno, c_preench)
    elif nome == 'Círculo':
        figura_nova = (Círculo(fig.valor_x, fig.valor_y, ((fig.valor_x - event.x) ** 2 + (fig.valor_y - event.y) ** 2) ** 0.5), c_contorno, c_preench)
    elif nome == 'Poligono':
        # Mantém a linha elástica ativa até a posição atual do mouse.
        ponto_previo_poligono = (event.x, event.y)
        
    desenhar_figuras()
    desenhar_figura_nova()


# Quando mouse é solto
def incluir_figura_nova(event):
    global figura_nova
    if figura_nova and type(figura_nova[0]).__name__ != 'Poligono':
        if not incompleta(figura_nova[0]):
            figuras.append(figura_nova)
        figura_nova = None
        desenhar_figuras()


def finalizar_poligono(event=None):
    global figura_nova, ponto_previo_poligono
    if figura_nova and type(figura_nova[0]).__name__ == 'Poligono':
        fig = figura_nova[0]
        if event is not None and len(fig.pontos) >= 3 and perto_do_inicio((event.x, event.y), fig.pontos[0]):
            if fig.fechar():
                figuras.append((fig, cor_contorno, cor_preenchimento))
        elif len(fig.pontos) >= 3 and ponto_previo_poligono is not None and perto_do_inicio(ponto_previo_poligono, fig.pontos[0]):
            if fig.fechar():
                figuras.append((fig, cor_contorno, cor_preenchimento))
        figura_nova = None
        ponto_previo_poligono = None
        desenhar_figuras()


def desenhar_figuras():
    canvas.delete('all')
    for fig, c_contorno, c_preench in figuras:
        nome = type(fig).__name__
        if nome == 'Linha':
            canvas.create_line(fig.valor_x, fig.valor_y, fig.valor_xf, fig.valor_yf, fill=c_contorno)
        elif nome == 'Retângulo':
            canvas.create_rectangle(fig.valor_x, fig.valor_y, fig.valor_xf, fig.valor_yf, outline=c_contorno, fill=c_preench)
        elif nome == 'Oval':
            canvas.create_oval(fig.valor_x, fig.valor_y, fig.valor_xf, fig.valor_yf, outline=c_contorno, fill=c_preench)
        elif nome == 'Círculo':
            canvas.create_oval(fig.valor_x - fig.raio, fig.valor_y - fig.raio, fig.valor_x + fig.raio, fig.valor_y + fig.raio, outline=c_contorno, fill=c_preench)
        elif nome == 'Rabisco' and len(fig.lista) >= 4:
            canvas.create_line(fig.lista, fill=c_contorno)
        elif nome == 'Poligono' and len(fig.pontos) >= 3:
            canvas.create_polygon(fig.pontos, outline=c_contorno, fill=c_preench)


def desenhar_figura_nova():
    if not figura_nova:
        return
    fig, c_contorno, c_preench = figura_nova[0], figura_nova[1], figura_nova[2]
    nome = type(fig).__name__
    
    if nome == 'Linha':
        canvas.create_line(fig.valor_x, fig.valor_y, fig.valor_xf, fig.valor_yf, dash=(4, 2), fill=c_contorno)
    elif nome == 'Retângulo':
        canvas.create_rectangle(fig.valor_x, fig.valor_y, fig.valor_xf, fig.valor_yf, dash=(4, 2), outline=c_contorno, fill=c_preench)
    elif nome == 'Oval':
        canvas.create_oval(fig.valor_x, fig.valor_y, fig.valor_xf, fig.valor_yf, dash=(4, 2), outline=c_contorno, fill=c_preench)
    elif nome == 'Círculo':
        canvas.create_oval(fig.valor_x - fig.raio, fig.valor_y - fig.raio, fig.valor_x + fig.raio, fig.valor_y + fig.raio, dash=(4, 2), outline=c_contorno, fill=c_preench)
    elif nome == 'Rabisco' and len(fig.lista) >= 4:
        canvas.create_line(fig.lista, dash=(4, 2), fill=c_contorno)
    elif nome == 'Poligono' and len(fig.pontos) >= 1:
        pontos = list(fig.pontos)
        if ponto_previo_poligono is not None:
            pontos.append(ponto_previo_poligono)
        if len(pontos) >= 2:
            canvas.create_line([coord for ponto in pontos for coord in ponto], dash=(4, 2), fill=c_contorno)
        x0, y0 = fig.pontos[0]
        canvas.create_oval(x0 - 4, y0 - 4, x0 + 4, y0 + 4, outline='red', width=2)


def incompleta(figura):
    nome = type(figura).__name__
    if nome in ['Linha', 'Retângulo', 'Oval']:
        return figura.valor_x == figura.valor_xf and figura.valor_y == figura.valor_yf
    if nome == 'Círculo':
        return figura.raio <= 0
    if nome == 'Rabisco':
        return len(figura.lista) <= 2
    return False


def mudar_cor(modo):
    global cor_contorno, cor_preenchimento
    cor = colorchooser.askcolor(title='Escolha a cor')
    if cor[1]:
        if modo == 'contorno':
            cor_contorno = cor[1]
        else:
            cor_preenchimento = cor[1]


# Configurações globais e inicialização
figuras = []
figura_nova = None
ponto_previo_poligono = None
cor_contorno = '#000000'
cor_preenchimento = ''

root = Tk()
root.title('Paint Integrado - Linhas, Formas, Círculos e Polígonos')
frame = Frame(root)
paddings = {'padx': 5, 'pady': 5}

label = ttk.Label(frame, text='Selecione a ferramenta de desenho:')
label.grid(column=0, row=0, sticky=W, **paddings)

tipo_figura_var = StringVar(root)
tipo_figura_var.set('Linha')

option_menu = ttk.OptionMenu(frame, tipo_figura_var, 'Linha', 'Linha', 'Rabisco', 'Retângulo', 'Oval', 'Círculo (Centro)', 'Polígono')
option_menu.grid(column=1, row=0, sticky=W, **paddings)

btn_outline = ttk.Button(frame, text='Cor de Contorno', command=lambda: mudar_cor('contorno'))
btn_fill = ttk.Button(frame, text='Cor de Preenchimento', command=lambda: mudar_cor('preenchimento'))
btn_outline.grid(column=2, row=0, sticky=W, **paddings)
btn_fill.grid(column=3, row=0, sticky=W, **paddings)

canvas = Canvas(frame, bg='white', width=1280, height=720)
canvas.grid(column=0, row=1, columnspan=4, sticky=W, **paddings)
frame.pack()

# Eventos de mouse e teclado
canvas.bind('<ButtonPress-1>', iniciar_figura_nova)
canvas.bind('<B1-Motion>', atualizar_figura_nova)
canvas.bind('<ButtonRelease-1>', incluir_figura_nova)
canvas.bind('<Double-Button-1>', finalizar_poligono)
canvas.focus_set()
root.bind('<Return>', finalizar_poligono)

root.mainloop()