# view.py
from tkinter import *
from tkinter import ttk, colorchooser, filedialog, messagebox

class PaintView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        
        self.root.title('Paint Integrado - Padrão MVC')
        self.frame = Frame(self.root)
        self.paddings = {'padx': 5, 'pady': 5}

        # Menu superior de Ferramentas e Cores
        self.label = ttk.Label(self.frame, text='Selecione a ferramenta de desenho:')
        self.label.grid(column=0, row=0, sticky=W, **self.paddings)

        self.tipo_figura_var = StringVar(self.root)
        self.tipo_figura_var.set('Linha')

        self.option_menu = ttk.OptionMenu(
            self.frame, self.tipo_figura_var, 'Linha', 'Linha', 'Rabisco', 
            'Retângulo', 'Oval', 'Círculo (Centro)', 'Polígono'
        )
        self.option_menu.grid(column=1, row=0, sticky=W, **self.paddings)

        # Botões de cores
        self.btn_outline = ttk.Button(self.frame, text='Cor de Contorno', command=self.controller.mudar_cor_contorno)
        self.btn_fill = ttk.Button(self.frame, text='Cor de Preenchimento', command=self.controller.mudar_cor_preenchimento)
        self.btn_outline.grid(column=2, row=0, sticky=W, **self.paddings)
        self.btn_fill.grid(column=3, row=0, sticky=W, **self.paddings)

        # Botões de salvar/carregar desenho
        self.btn_salvar = ttk.Button(self.frame, text='Salvar Desenho', command=self.controller.salvar_desenho)
        self.btn_carregar = ttk.Button(self.frame, text='Carregar Desenho', command=self.controller.carregar_desenho)
        self.btn_salvar.grid(column=4, row=0, sticky=W, **self.paddings)
        self.btn_carregar.grid(column=5, row=0, sticky=W, **self.paddings)

        # Canvas
        self.canvas = Canvas(self.frame, bg='white', width=1280, height=720)
        self.canvas.grid(column=0, row=1, columnspan=4, sticky=W, **self.paddings)
        self.frame.pack()

    def obter_ferramenta_selecionada(self):
        return self.tipo_figura_var.get()

    def obter_cor_da_paleta(self):
        cor = colorchooser.askcolor(title='Escolha a cor')
        return cor[1]

    def perguntar_caminho_para_salvar(self):
        """Abre o diálogo 'Salvar como' e retorna o caminho escolhido (ou '' se cancelado)."""
        return filedialog.asksaveasfilename(
            title='Salvar desenho',
            defaultextension='.json',
            filetypes=[('Arquivo de desenho (JSON)', '*.json'), ('Todos os arquivos', '*.*')],
        )

    def perguntar_caminho_para_abrir(self):
        """Abre o diálogo 'Abrir arquivo' e retorna o caminho escolhido (ou '' se cancelado)."""
        return filedialog.askopenfilename(
            title='Carregar desenho',
            filetypes=[('Arquivo de desenho (JSON)', '*.json'), ('Todos os arquivos', '*.*')],
        )

    def mostrar_info(self, titulo, mensagem):
        messagebox.showinfo(titulo, mensagem)

    def mostrar_erro(self, titulo, mensagem):
        messagebox.showerror(titulo, mensagem)

    def limpar_canvas(self):
        self.canvas.delete('all')

    def desenhar_figuras_salvas(self, figuras):
        for fig, c_contorno, c_preench in figuras:
            nome = type(fig).__name__
            if nome == 'Linha':
                self.canvas.create_line(fig.valor_x, fig.valor_y, fig.valor_xf, fig.valor_yf, fill=c_contorno)
            elif nome == 'Retângulo':
                self.canvas.create_rectangle(fig.valor_x, fig.valor_y, fig.valor_xf, fig.valor_yf, outline=c_contorno, fill=c_preench)
            elif nome == 'Oval':
                self.canvas.create_oval(fig.valor_x, fig.valor_y, fig.valor_xf, fig.valor_yf, outline=c_contorno, fill=c_preench)
            elif nome == 'Círculo':
                self.canvas.create_oval(fig.valor_x - fig.raio, fig.valor_y - fig.raio, fig.valor_x + fig.raio, fig.valor_y + fig.raio, outline=c_contorno, fill=c_preench)
            elif nome == 'Rabisco' and len(fig.lista) >= 4:
                self.canvas.create_line(fig.lista, fill=c_contorno)
            elif nome == 'Poligono' and len(fig.pontos) >= 3:
                self.canvas.create_polygon(fig.pontos, outline=c_contorno, fill=c_preench)

    def desenhar_figura_temporaria(self, figura_nova, ponto_previo_poligono):
        if not figura_nova:
            return
        fig, c_contorno, c_preench = figura_nova[0], figura_nova[1], figura_nova[2]
        nome = type(fig).__name__

        if nome == 'Linha':
            self.canvas.create_line(fig.valor_x, fig.valor_y, fig.valor_xf, fig.valor_yf, dash=(4, 2), fill=c_contorno)
        elif nome == 'Retângulo':
            self.canvas.create_rectangle(fig.valor_x, fig.valor_y, fig.valor_xf, fig.valor_yf, dash=(4, 2), outline=c_contorno, fill=c_preench)
        elif nome == 'Oval':
            self.canvas.create_oval(fig.valor_x, fig.valor_y, fig.valor_xf, fig.valor_yf, dash=(4, 2), outline=c_contorno, fill=c_preench)
        elif nome == 'Círculo':
            self.canvas.create_oval(fig.valor_x - fig.raio, fig.valor_y - fig.raio, fig.valor_x + fig.raio, fig.valor_y + fig.raio, dash=(4, 2), outline=c_contorno, fill=c_preench)
        elif nome == 'Rabisco' and len(fig.lista) >= 4:
            self.canvas.create_line(fig.lista, dash=(4, 2), fill=c_contorno)
        elif nome == 'Poligono' and len(fig.pontos) >= 1:
            pontos = list(fig.pontos)
            if ponto_previo_poligono is not None:
                pontos.append(ponto_previo_poligono)
            if len(pontos) >= 2:
                self.canvas.create_line([coord for p in pontos for coord in p], dash=(4, 2), fill=c_contorno)
            x0, y0 = fig.pontos[0]
            self.canvas.create_oval(x0 - 4, y0 - 4, x0 + 4, y0 + 4, outline='red', width=2)