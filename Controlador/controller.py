from abc import ABC, abstractmethod
from Modelo.model import (
    Linha, Rabisco, Retângulo, Círculo, Oval, Poligono
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


