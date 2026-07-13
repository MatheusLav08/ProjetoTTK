from tkinter import *
from tkinter import ttk
from tkinter import colorchooser

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
            figuras.append(figura_nova)
        figura_nova = None
        desenhar_figuras()


def finalizar_poligono(event=None):
    global figura_nova, ponto_previo_poligono
    if figura_nova and figura_nova[0] == "poligono":
        vertices = figura_nova[1]
        if len(vertices) >= 3 and fechamento_valido_para_poligono(vertices):
            figuras.append(("poligono", vertices, figura_nova[2], figura_nova[3]))
        figura_nova = None
        ponto_previo_poligono = None
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
            canvas.create_oval(x - r, y - r, x + r, y + r, outline=c_contorno, fill=c_preench)
        elif fig == "poligono" and len(values) >= 3:
            canvas.create_polygon(values, outline=c_contorno, fill=c_preench)
        else:
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
        canvas.create_oval(x - r, y - r, x + r, y + r, dash=(4, 2), outline=c_contorno, fill=c_preench)
    elif fig == "poligono" and len(values) >= 1:
        pontos = list(values)
        if ponto_previo_poligono is not None:
            pontos.append(ponto_previo_poligono)
        if len(pontos) >= 2:
            canvas.create_line([coord for ponto in pontos for coord in ponto], dash=(4, 2), fill=c_contorno)
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
            cor_contorno = cor[1]
        elif modo == "preenchimento":
            cor_preenchimento = cor[1]


#******* MAIN *******#

figuras = []
figura_nova = None
ponto_previo_poligono = None

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

canvas = Canvas(frame, bg='white', width=1280, height=720)
canvas.grid(column=0, row=1, columnspan=4, sticky=W, **paddings)

frame.pack()

canvas.bind('<ButtonPress-1>', iniciar_figura_nova)
canvas.bind('<B1-Motion>', atualizar_figura_nova)
canvas.bind('<ButtonRelease-1>', incluir_figura_nova)
canvas.bind('<Double-Button-1>', finalizar_poligono)
canvas.focus_set()
root.bind('<Return>', finalizar_poligono)

root.mainloop()
