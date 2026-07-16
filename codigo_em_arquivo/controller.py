# controller.py - Controlador (Orquestra modelo e visão)
from model import (
    Linha, Rabisco, Retângulo, Círculo, Oval, Poligono
)


class PaintController:
    def __init__(self, view):
        self.view = view
        self.figuras = []
        self.figura_nova = None
        self.ponto_previo_poligono = None
        self.cor_contorno = '#000000'
        self.cor_preenchimento = ''
        
        # Conectar eventos do canvas
        self._conectar_eventos()
    
    def _conectar_eventos(self):
        """Conecta os eventos do mouse ao canvas"""
        self.view.canvas.bind('<ButtonPress-1>', self._mouse_press)
        self.view.canvas.bind('<B1-Motion>', self._mouse_motion)
        self.view.canvas.bind('<ButtonRelease-1>', self._mouse_release)
        self.view.canvas.bind('<Double-Button-1>', self._finalizar_poligono)
        self.view.canvas.focus_set()
        self.view.root.bind('<Return>', self._finalizar_poligono)
    
    def _perto_do_inicio(self, ponto, inicio, tol=30):
        """Verifica se o ponto está perto do início (para fechar polígono)"""
        return ((ponto[0] - inicio[0]) ** 2 + (ponto[1] - inicio[1]) ** 2) ** 0.5 <= tol
    
    def _mouse_press(self, event):
        """Inicia uma nova figura quando o botão é pressionado"""
        ferramenta = self.view.obter_ferramenta_selecionada()
        
        if ferramenta == 'Linha':
            fig = Linha(event.x, event.y, event.x, event.y)
        elif ferramenta == 'Retângulo':
            fig = Retângulo(event.x, event.y, event.x, event.y)
        elif ferramenta == 'Oval':
            fig = Oval(event.x, event.y, event.x, event.y)
        elif ferramenta == 'Círculo (Centro)':
            fig = Círculo(event.x, event.y, 0)
        elif ferramenta == 'Polígono':
            # Cada clique fixa um novo vértice do polígono
            if self.figura_nova and type(self.figura_nova[0]).__name__ == 'Poligono':
                fig = self.figura_nova[0]
                if len(fig.pontos) >= 3 and self._perto_do_inicio((event.x, event.y), fig.pontos[0]):
                    if fig.fechar():
                        self.figuras.append((fig, self.cor_contorno, self.cor_preenchimento))
                        self.figura_nova = None
                        self.ponto_previo_poligono = None
                        self._desenhar()
                        return
                    self.ponto_previo_poligono = None
                    self._desenhar()
                    return
                fig.adicionar((event.x, event.y))
            else:
                fig = Poligono([(event.x, event.y)])
            self.ponto_previo_poligono = None
        else:  # Rabisco
            fig = Rabisco([event.x, event.y])
        
        self.figura_nova = (fig, self.cor_contorno, self.cor_preenchimento)
        self._desenhar()
    
    def _mouse_motion(self, event):
        """Atualiza a figura enquanto o mouse se move"""
        if not self.figura_nova:
            return
        
        fig, c_contorno, c_preench = self.figura_nova[0], self.figura_nova[1], self.figura_nova[2]
        nome = type(fig).__name__
        
        if nome == 'Rabisco':
            fig.lista.extend([event.x, event.y])
            self.figura_nova = (Rabisco(fig.lista), c_contorno, c_preench)
        elif nome == 'Retângulo':
            self.figura_nova = (Retângulo(fig.valor_x, fig.valor_y, event.x, event.y), c_contorno, c_preench)
        elif nome == 'Oval':
            self.figura_nova = (Oval(fig.valor_x, fig.valor_y, event.x, event.y), c_contorno, c_preench)
        elif nome == 'Linha':
            self.figura_nova = (Linha(fig.valor_x, fig.valor_y, event.x, event.y), c_contorno, c_preench)
        elif nome == 'Círculo':
            raio = ((fig.valor_x - event.x) ** 2 + (fig.valor_y - event.y) ** 2) ** 0.5
            self.figura_nova = (Círculo(fig.valor_x, fig.valor_y, raio), c_contorno, c_preench)
        elif nome == 'Poligono':
            # Mantém a linha elástica ativa até a posição atual do mouse
            self.ponto_previo_poligono = (event.x, event.y)
        
        self._desenhar()
    
    def _mouse_release(self, event):
        """Finaliza a figura quando o botão é solto"""
        if self.figura_nova and type(self.figura_nova[0]).__name__ != 'Poligono':
            if not self._incompleta(self.figura_nova[0]):
                self.figuras.append(self.figura_nova)
            self.figura_nova = None
            self._desenhar()
    
    def _finalizar_poligono(self, event=None):
        """Finaliza o polígono atual"""
        if self.figura_nova and type(self.figura_nova[0]).__name__ == 'Poligono':
            fig = self.figura_nova[0]
            if event is not None and len(fig.pontos) >= 3 and self._perto_do_inicio((event.x, event.y), fig.pontos[0]):
                if fig.fechar():
                    self.figuras.append((fig, self.cor_contorno, self.cor_preenchimento))
            elif len(fig.pontos) >= 3 and self.ponto_previo_poligono is not None and self._perto_do_inicio(self.ponto_previo_poligono, fig.pontos[0]):
                if fig.fechar():
                    self.figuras.append((fig, self.cor_contorno, self.cor_preenchimento))
            self.figura_nova = None
            self.ponto_previo_poligono = None
            self._desenhar()
    
    def _incompleta(self, figura):
        """Verifica se uma figura está incompleta"""
        nome = type(figura).__name__
        if nome in ['Linha', 'Retângulo', 'Oval']:
            return figura.valor_x == figura.valor_xf and figura.valor_y == figura.valor_yf
        if nome == 'Círculo':
            return figura.raio <= 0
        if nome == 'Rabisco':
            return len(figura.lista) <= 2
        return False
    
    def _desenhar(self):
        """Limpa canvas e redesenha todas as figuras"""
        self.view.limpar_canvas()
        self.view.desenhar_figuras_salvas(self.figuras)
        self.view.desenhar_figura_temporaria(self.figura_nova, self.ponto_previo_poligono)
    
    def mudar_cor_contorno(self):
        """Abre diálogo para escolher cor de contorno"""
        cor = self.view.obter_cor_da_paleta()
        if cor:
            self.cor_contorno = cor
    
    def mudar_cor_preenchimento(self):
        """Abre diálogo para escolher cor de preenchimento"""
        cor = self.view.obter_cor_da_paleta()
        if cor:
            self.cor_preenchimento = cor
