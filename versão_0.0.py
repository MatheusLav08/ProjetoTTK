<<<<<<< Updated upstream
=======
from abc import ABC
>>>>>>> Stashed changes
from tkinter import *
from tkinter import ttk, colorchooser

<<<<<<< Updated upstream
cor_contorno = 'black'
cor_preenchimento = 'white'
ponto_previo_poligono = None


def orientacao(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def ponto_no_segmento(a, b, p):
    return min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1]) and orientacao(a, b, p) == 0


def segmentos_se_cruzam(a, b, c, d):
    o1, o2, o3, o4 = orientacao(a, b, c), orientacao(a, b, d), orientacao(c, d, a), orientacao(c, d, b)
    return (o1 == 0 and ponto_no_segmento(a, b, c)) or (o2 == 0 and ponto_no_segmento(a, b, d)) or (o3 == 0 and ponto_no_segmento(c, d, a)) or (o4 == 0 and ponto_no_segmento(c, d, b)) or ((o1 > 0) != (o2 > 0) and (o3 > 0) != (o4 > 0))


def aresta_valida_para_poligono(vertices, novo_ponto):
    if len(vertices) < 2:
        return True
    return all(not segmentos_se_cruzam(vertices[-1], novo_ponto, vertices[i], vertices[i + 1]) for i in range(len(vertices) - 2))


def fechamento_valido_para_poligono(vertices):
    if len(vertices) < 3:
        return False
    return all(not segmentos_se_cruzam(vertices[-1], vertices[0], vertices[i], vertices[i + 1]) for i in range(1, len(vertices) - 2))


def iniciar_figura_nova(event):
    global figura_nova, ponto_previo_poligono

    tipo = tipo_figura_var.get()

    if tipo == 'Linha':
        figura_nova = ("linha", (event.x, event.y, event.x, event.y), cor_contorno, cor_preenchimento)
    elif tipo == 'Retângulo':
        figura_nova = ("retangulo", (event.x, event.y, event.x, event.y), cor_contorno, cor_preenchimento)
    elif tipo == 'Oval':
        figura_nova = ("oval", (event.x, event.y, event.x, event.y), cor_contorno, cor_preenchimento)
    elif tipo == 'Círculo (Centro)':
        figura_nova = ("circulo", (event.x, event.y, 0), cor_contorno, cor_preenchimento)
    elif tipo == 'Polígono':
        if not figura_nova or figura_nova[0] != 'poligono':
            figura_nova = ("poligono", [(event.x, event.y)], cor_contorno, cor_preenchimento)
        else:
            vertices = list(figura_nova[1])
            novo_ponto = (event.x, event.y)
            if novo_ponto not in vertices and aresta_valida_para_poligono(vertices, novo_ponto):
                vertices.append(novo_ponto)
                figura_nova = ("poligono", vertices, cor_contorno, cor_preenchimento)
        ponto_previo_poligono = (event.x, event.y)
    else:
        figura_nova = ("rabisco", [(event.x, event.y)], cor_contorno, cor_preenchimento)

    desenhar_figuras()
    desenhar_figura_nova()


def atualizar_figura_nova(event):
    global figura_nova, ponto_previo_poligono
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
        ini_x, ini_y = valores[0], valores[1]
        raio = ((ini_x - event.x) ** 2 + (ini_y - event.y) ** 2) ** 0.5
        figura_nova = ("circulo", (ini_x, ini_y, raio), c_contorno, c_preench)

    if tipo == "poligono":
        ponto_previo_poligono = (event.x, event.y)

    desenhar_figuras()
    desenhar_figura_nova()


def incluir_figura_nova(event):
    global figura_nova
    if figura_nova and figura_nova[0] != "poligono":
        if not incompleta(figura_nova):
=======
class Figuras(ABC):
    def __init__(self, x=0, y=0, xf=0, yf=0):
        self.valor_x, self.valor_y, self.valor_xf, self.valor_yf = x, y, xf, yf

class Linha(Figuras):
    pass

class Rabisco(Figuras):
    def __init__(self, lista):
        self.lista = lista

class Retângulo(Figuras):
    pass

class Círculo(Figuras):
    def __init__(self, x, y, raio):
        super().__init__(x, y)
        self.raio = raio

class Oval(Figuras):
    pass

class Poligono(Figuras):
    def __init__(self, pontos):
        self.pontos = pontos

    # Adiciona um novo vértice ao polígono, sem permitir repetição
    def adicionar(self, novo):
        if novo in self.pontos:
            return False
        if len(self.pontos) >= 2 and not self.valido(novo):
            return False
        self.pontos.append(novo)
        return True

    # Evita que uma nova aresta cruze uma aresta já existente
    def valido(self, novo):
        return all(not segmentos_se_cruzam(self.pontos[-1], novo, self.pontos[i], self.pontos[i + 1]) for i in range(len(self.pontos) - 2))

    # Valida o fechamento do polígono antes de salvar
    def fechar(self):
        if len(self.pontos) < 3:
            return False
        for i in range(1, len(self.pontos) - 2):
            if segmentos_se_cruzam(self.pontos[-1], self.pontos[0], self.pontos[i], self.pontos[i + 1]):
                return False
        return True


def orientacao(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def ponto_no_segmento(a, b, p):
    return min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1]) and orientacao(a, b, p) == 0


def segmentos_se_cruzam(a, b, c, d):
    o1, o2, o3, o4 = orientacao(a, b, c), orientacao(a, b, d), orientacao(c, d, a), orientacao(c, d, b)
    return (o1 == 0 and ponto_no_segmento(a, b, c)) or (o2 == 0 and ponto_no_segmento(a, b, d)) or (o3 == 0 and ponto_no_segmento(c, d, a)) or (o4 == 0 and ponto_no_segmento(c, d, b)) or ((o1 > 0) != (o2 > 0) and (o3 > 0) != (o4 > 0))


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
    desenhar_figuras(); desenhar_figura_nova()


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
        # Mantém o ponto atual do mouse.
        ponto_previo_poligono = (event.x, event.y)
    desenhar_figuras(); desenhar_figura_nova()


# Quando mouse é solto
def incluir_figura_nova(event):
    global figura_nova
    if figura_nova and type(figura_nova[0]).__name__ != 'Poligono':
        if not incompleta(figura_nova[0]):
>>>>>>> Stashed changes
            figuras.append(figura_nova)
        figura_nova = None
        desenhar_figuras()


def finalizar_poligono(event=None):
    global figura_nova, ponto_previo_poligono
<<<<<<< Updated upstream
    if figura_nova and figura_nova[0] == "poligono":
        vertices = figura_nova[1]
        if len(vertices) >= 3 and fechamento_valido_para_poligono(vertices):
            figuras.append(("poligono", vertices, figura_nova[2], figura_nova[3]))
=======
    if figura_nova and type(figura_nova[0]).__name__ == 'Poligono':
        fig = figura_nova[0]
        if event is not None and len(fig.pontos) >= 3 and perto_do_inicio((event.x, event.y), fig.pontos[0]):
            if fig.fechar():
                figuras.append((fig, cor_contorno, cor_preenchimento))
        elif len(fig.pontos) >= 3 and ponto_previo_poligono is not None and perto_do_inicio(ponto_previo_poligono, fig.pontos[0]):
            if fig.fechar():
                figuras.append((fig, cor_contorno, cor_preenchimento))
>>>>>>> Stashed changes
        figura_nova = None
        ponto_previo_poligono = None
        desenhar_figuras()


def desenhar_figuras():
<<<<<<< Updated upstream
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
            canvas.create_oval(x - r, y - r, x + r, y + r, outline=c_contorno, fill=c_preench)
        elif fig == "poligono" and len(values) >= 3:
            canvas.create_polygon(values, outline=c_contorno, fill=c_preench)
        else:
            canvas.create_line(values, fill=c_contorno)
=======
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
>>>>>>> Stashed changes


def desenhar_figura_nova():
    if not figura_nova:
        return
<<<<<<< Updated upstream
    fig, values, c_contorno, c_preench = figura_nova
    if fig == "linha":
        canvas.create_line(values[0], values[1], values[2], values[3], dash=(4, 2), fill=c_contorno)
    elif fig == "retangulo":
        canvas.create_rectangle(values[0], values[1], values[2], values[3], dash=(4, 2), outline=c_contorno, fill=c_preench)
    elif fig == "oval":
        canvas.create_oval(values[0], values[1], values[2], values[3], dash=(4, 2), outline=c_contorno, fill=c_preench)
    elif fig == "circulo":
        x, y, r = values
        canvas.create_oval(x - r, y - r, x + r, y + r, dash=(4, 2), outline=c_contorno, fill=c_preench)
    elif fig == "poligono" and len(values) >= 1:
        pontos = list(values)
=======
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
        # Desenha os vértices já fixados e, em seguida, a linha que está sendo feita até o mouse.
        pontos = list(fig.pontos)
>>>>>>> Stashed changes
        if ponto_previo_poligono is not None:
            pontos.append(ponto_previo_poligono)
        if len(pontos) >= 2:
            canvas.create_line([coord for ponto in pontos for coord in ponto], dash=(4, 2), fill=c_contorno)
<<<<<<< Updated upstream
    else:
        canvas.create_line(values, dash=(4, 2), fill=c_contorno)


def incompleta(figura):
    fig, values, _, _ = figura
    if fig in ["linha", "retangulo", "oval"]:
        return (values[0], values[1]) == (values[2], values[3])
    elif fig == "circulo":
        return values[2] <= 0
    elif fig == "poligono":
        return len(values) < 3
    else:
        return len(values) <= 1


def mudar_cor(modo):
    global cor_contorno, cor_preenchimento
    cor = colorchooser.askcolor(title="Escolha a cor")
    if cor[1]:
        if modo == "contorno":
=======
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
>>>>>>> Stashed changes
            cor_contorno = cor[1]
        else:
            cor_preenchimento = cor[1]

<<<<<<< Updated upstream

#******* MAIN *******#
=======
>>>>>>> Stashed changes

figuras = []
figura_nova = None
ponto_previo_poligono = None
<<<<<<< Updated upstream

root = Tk()
root.title("Paint Integrado - Linhas, Formas, Círculos e Polígonos")
frame = Frame(root)

paddings = {'padx': 5, 'pady': 5}

label = ttk.Label(frame, text='Selecione a ferramenta de desenho:')
label.grid(column=0, row=0, sticky=W, **paddings)

tipo_figura_var = StringVar(root)
option_menu = ttk.OptionMenu(frame, tipo_figura_var, 'Linha', 'Linha', 'Rabisco', 'Retângulo', 'Oval', 'Círculo (Centro)', 'Polígono')
option_menu.grid(column=1, row=0, sticky=W, **paddings)

btn_outline = ttk.Button(frame, text='Cor de Contorno', command=lambda: mudar_cor("contorno"))
btn_fill = ttk.Button(frame, text='Cor de Preenchimento', command=lambda: mudar_cor("preenchimento"))
btn_outline.grid(column=2, row=0, sticky=W, **paddings)
btn_fill.grid(column=3, row=0, sticky=W, **paddings)

=======
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
>>>>>>> Stashed changes
canvas = Canvas(frame, bg='white', width=1280, height=720)
canvas.grid(column=0, row=1, columnspan=4, sticky=W, **paddings)
frame.pack()
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
canvas.bind('<ButtonPress-1>', iniciar_figura_nova)
canvas.bind('<B1-Motion>', atualizar_figura_nova)
canvas.bind('<ButtonRelease-1>', incluir_figura_nova)
canvas.bind('<Double-Button-1>', finalizar_poligono)
canvas.focus_set()
root.bind('<Return>', finalizar_poligono)
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
root.mainloop()
