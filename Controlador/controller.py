from abc import ABC, abstractmethod
from Modelo.model import (
    Linha, Rabisco, Retângulo, Círculo, Oval, Poligono,
    salvar_para_arquivo, carregar_de_arquivo
)

# =====================================================================
# 1. INTERFACE BASE DOS ESTADOS (State)
# =====================================================================
class EstadoFerramenta(ABC):
    @abstractmethod
    def mouse_press(self, controller, event):
        pass

    @abstractmethod
    def mouse_motion(self, controller, event):
        pass

    @abstractmethod
    def mouse_release(self, controller, event):
        pass

    def finalizar_poligono(self, controller, event=None):
        # Implementação padrão vazia, já que a maioria das ferramentas ignora isso
        pass


# =====================================================================
# 2. ESTADOS CONCRETOS (Concrete States)
# =====================================================================

class EstadoLinha(EstadoFerramenta):
    def mouse_press(self, controller, event):
        fig = Linha(event.x, event.y, event.x, event.y)
        controller.figura_nova = (fig, controller.cor_contorno, controller.cor_preenchimento)

    def mouse_motion(self, controller, event):
        if not controller.figura_nova: return
        fig, cc, cp = controller.figura_nova
        controller.figura_nova = (Linha(fig.valor_x, fig.valor_y, event.x, event.y), cc, cp)

    def mouse_release(self, controller, event):
        if controller.figura_nova and not controller.figura_nova[0].esta_incompleta():
            controller.figuras.append(controller.figura_nova)
        controller.figura_nova = None


class EstadoRetangulo(EstadoFerramenta):
    def mouse_press(self, controller, event):
        fig = Retângulo(event.x, event.y, event.x, event.y)
        controller.figura_nova = (fig, controller.cor_contorno, controller.cor_preenchimento)

    def mouse_motion(self, controller, event):
        if not controller.figura_nova: return
        fig, cc, cp = controller.figura_nova
        controller.figura_nova = (Retângulo(fig.valor_x, fig.valor_y, event.x, event.y), cc, cp)

    def mouse_release(self, controller, event):
        if controller.figura_nova and not controller.figura_nova[0].esta_incompleta():
            controller.figuras.append(controller.figura_nova)
        controller.figura_nova = None


class EstadoOval(EstadoFerramenta):
    def mouse_press(self, controller, event):
        fig = Oval(event.x, event.y, event.x, event.y)
        controller.figura_nova = (fig, controller.cor_contorno, controller.cor_preenchimento)

    def mouse_motion(self, controller, event):
        if not controller.figura_nova: return
        fig, cc, cp = controller.figura_nova
        controller.figura_nova = (Oval(fig.valor_x, fig.valor_y, event.x, event.y), cc, cp)

    def mouse_release(self, controller, event):
        if controller.figura_nova and not controller.figura_nova[0].esta_incompleta():
            controller.figuras.append(controller.figura_nova)
        controller.figura_nova = None


class EstadoCirculo(EstadoFerramenta):
    def mouse_press(self, controller, event):
        fig = Círculo(event.x, event.y, 0)
        controller.figura_nova = (fig, controller.cor_contorno, controller.cor_preenchimento)

    def mouse_motion(self, controller, event):
        if not controller.figura_nova: return
        fig, cc, cp = controller.figura_nova
        raio = ((fig.valor_x - event.x) ** 2 + (fig.valor_y - event.y) ** 2) ** 0.5
        controller.figura_nova = (Círculo(fig.valor_x, fig.valor_y, raio), cc, cp)

    def mouse_release(self, controller, event):
        if controller.figura_nova and not controller.figura_nova[0].esta_incompleta():
            controller.figuras.append(controller.figura_nova)
        controller.figura_nova = None


class EstadoRabisco(EstadoFerramenta):
    def mouse_press(self, controller, event):
        fig = Rabisco([event.x, event.y])
        controller.figura_nova = (fig, controller.cor_contorno, controller.cor_preenchimento)

    def mouse_motion(self, controller, event):
        if not controller.figura_nova: return
        fig, cc, cp = controller.figura_nova
        nova_lista = list(fig.lista)
        nova_lista.extend([event.x, event.y])
        controller.figura_nova = (Rabisco(nova_lista), cc, cp)

    def mouse_release(self, controller, event):
        if controller.figura_nova and not controller.figura_nova[0].esta_incompleta():
            controller.figuras.append(controller.figura_nova)
        controller.figura_nova = None


class EstadoPoligono(EstadoFerramenta):
    def _perto_do_inicio(self, ponto, inicio, tol=30):
        return ((ponto[0] - inicio[0]) ** 2 + (ponto[1] - inicio[1]) ** 2) ** 0.5 <= tol

    def mouse_press(self, controller, event):
        if controller.figura_nova and isinstance(controller.figura_nova[0], Poligono):
            fig = controller.figura_nova[0]
            if len(fig.pontos) >= 3 and self._perto_do_inicio((event.x, event.y), fig.pontos[0]):
                if fig.fechar():
                    controller.figuras.append((fig, controller.cor_contorno, controller.cor_preenchimento))
                    controller.figura_nova = None
                    controller.ponto_previo_poligono = None
                return
            fig.adicionar((event.x, event.y))
        else:
            fig = Poligono([(event.x, event.y)])
        
        controller.figura_nova = (fig, controller.cor_contorno, controller.cor_preenchimento)
        controller.ponto_previo_poligono = None

    def mouse_motion(self, controller, event):
        if controller.figura_nova:
            controller.ponto_previo_poligono = (event.x, event.y)

    def mouse_release(self, controller, event):
        # Polígonos não fecham no release do clique
        pass

    def finalizar_poligono(self, controller, event=None):
        if controller.figura_nova and isinstance(controller.figura_nova[0], Poligono):
            fig = controller.figura_nova[0]
            if event is not None and len(fig.pontos) >= 3 and self._perto_do_inicio((event.x, event.y), fig.pontos[0]):
                if fig.fechar():
                    controller.figuras.append((fig, controller.cor_contorno, controller.cor_preenchimento))
            elif len(fig.pontos) >= 3 and controller.ponto_previo_poligono is not None and self._perto_do_inicio(controller.ponto_previo_poligono, fig.pontos[0]):
                if fig.fechar():
                    controller.figuras.append((fig, controller.cor_contorno, controller.cor_preenchimento))
            controller.figura_nova = None
            controller.ponto_previo_poligono = None
# =====================================================================
# 3. O CONTEXTO (PaintController)
# =====================================================================
class PaintController:
    def __init__(self, view):
        self.view = view
        self.figuras = []
        self.figura_nova = None
        self.ponto_previo_poligono = None
        self.cor_contorno = '#000000'
        self.cor_preenchimento = ''
        
        # Mapeamento estático de strings para classes de estado
        self._estados = {
            'Linha': EstadoLinha(),
            'Rabisco': EstadoRabisco(),
            'Retângulo': EstadoRetangulo(),
            'Oval': EstadoOval(),
            'Círculo (Centro)': EstadoCirculo(),
            'Polígono': EstadoPoligono()
        }
        
        self._conectar_eventos()
    
    def _obter_estado_atual(self):
        """Busca dinamicamente o estado com base na seleção da View"""
        ferramenta = self.view.obter_ferramenta_selecionada()
        return self._estados.get(ferramenta, EstadoLinha())
    
    def _conectar_eventos(self):
        """Conecta os eventos do mouse ao canvas"""
        self.view.canvas.bind('<ButtonPress-1>', self._mouse_press)
        self.view.canvas.bind('<B1-Motion>', self._mouse_motion)
        self.view.canvas.bind('<ButtonRelease-1>', self._mouse_release)
        self.view.canvas.bind('<Double-Button-1>', self._finalizar_poligono)
        self.view.canvas.focus_set()
        self.view.root.bind('<Return>', self._finalizar_poligono)
    
    # Delegando comportamentos para o estado atual
    def _mouse_press(self, event):
        estado = self._obter_estado_atual()
        estado.mouse_press(self, event)
        self._desenhar()
    
    def _mouse_motion(self, event):
        estado = self._obter_estado_atual()
        estado.mouse_motion(self, event)
        self._desenhar()
    
    def _mouse_release(self, event):
        estado = self._obter_estado_atual()
        estado.mouse_release(self, event)
        self._desenhar()
    
    def _finalizar_poligono(self, event=None):
        estado = self._obter_estado_atual()
        estado.finalizar_poligono(self, event)
        self._desenhar()
    
    def _desenhar(self):
        """Limpa canvas e redesenha todas as figuras"""
        self.view.limpar_canvas()
        self.view.desenhar_figuras_salvas(self.figuras)
        self.view.desenhar_figura_temporaria(self.figura_nova, self.ponto_previo_poligono)
    
    def mudar_cor_contorno(self):
        cor = self.view.obter_cor_da_paleta()
        if cor:
            self.cor_contorno = cor
    
    def mudar_cor_preenchimento(self):
        cor = self.view.obter_cor_da_paleta()
        if cor:
            self.cor_preenchimento = cor

    def salvar_desenho(self):
        """Pede um caminho de arquivo à view e delega ao model salvar o desenho atual nele"""
        caminho = self.view.perguntar_caminho_para_salvar()
        if not caminho:
            return  # usuário cancelou o diálogo
        try:
            salvar_para_arquivo(caminho, self.figuras)
            self.view.mostrar_info('Salvar desenho', 'Desenho salvo com sucesso!')
        except Exception as erro:
            self.view.mostrar_erro('Erro ao salvar', f'Não foi possível salvar o desenho:\n{erro}')

    def carregar_desenho(self):
        """Pede um caminho de arquivo à view e delega ao model carregar o desenho a partir dele"""
        caminho = self.view.perguntar_caminho_para_abrir()
        if not caminho:
            return  # usuário cancelou o diálogo
        try:
            self.figuras = carregar_de_arquivo(caminho)
            self.figura_nova = None
            self.ponto_previo_poligono = None
            self._desenhar()
            self.view.mostrar_info('Carregar desenho', 'Desenho carregado com sucesso!')
        except Exception as erro:
            self.view.mostrar_erro('Erro ao carregar', f'Não foi possível carregar o desenho:\n{erro}')

 


