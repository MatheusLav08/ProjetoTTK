from abc import ABC

# --- Funções matemáticas de suporte (Regra de Negócio) ---

def orientacao(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def ponto_no_segmento(a, b, p):
    return min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1]) and orientacao(a, b, p) == 0


def segmentos_se_cruzam(a, b, c, d):
    o1, o2, o3, o4 = orientacao(a, b, c), orientacao(a, b, d), orientacao(c, d, a), orientacao(c, d, b)
    return (o1 == 0 and ponto_no_segmento(a, b, c)) or (o2 == 0 and ponto_no_segmento(a, b, d)) or (o3 == 0 and ponto_no_segmento(c, d, a)) or (o4 == 0 and ponto_no_segmento(c, d, b)) or ((o1 > 0) != (o2 > 0) and (o3 > 0) != (o4 > 0))


# --- Classes de Figuras Geométricas ---

class Figuras(ABC):
    def __init__(self, x=0, y=0, xf=0, yf=0):
        self.valor_x, self.valor_y, self.valor_xf, self.valor_yf = x, y, xf, yf

    def esta_incompleta(self):
        return False


class Linha(Figuras):
    def esta_incompleta(self):
        return self.valor_x == self.valor_xf and self.valor_y == self.valor_yf


class Rabisco(Figuras):
    def __init__(self, lista):
        self.lista = lista

    def esta_incompleta(self):
        return len(self.lista) <= 2


class Retângulo(Figuras):
    def esta_incompleta(self):
        return self.valor_x == self.valor_xf and self.valor_y == self.valor_yf


class Círculo(Figuras):
    def __init__(self, x, y, raio):
        super().__init__(x, y)
        self.raio = raio

    def esta_incompleta(self):
        return self.raio <= 0


class Oval(Figuras):
    def esta_incompleta(self):
        return self.valor_x == self.valor_xf and self.valor_y == self.valor_yf


class Poligono(Figuras):
    def __init__(self, pontos):
        self.pontos = pontos

    def adicionar(self, novo):
        if novo in self.pontos:
            return False
        if len(self.pontos) >= 2 and not self.valido(novo):
            return False
        self.pontos.append(novo)
        return True

    def valido(self, novo):
        return all(not segmentos_se_cruzam(self.pontos[-1], novo, self.pontos[i], self.pontos[i + 1]) for i in range(len(self.pontos) - 2))

    def fechar(self):
        if len(self.pontos) < 3:
            return False
        for i in range(1, len(self.pontos) - 2):
            if segmentos_se_cruzam(self.pontos[-1], self.pontos[0], self.pontos[i], self.pontos[i + 1]):
                return False
        return True


# --- Estado Geral do Desenho ---

class DesenhoModel:
    def __init__(self):
        self.figuras = []               # Lista de tuplas (figura, cor_contorno, cor_preenchimento)
        self.figura_nova = None         # Tupla temporária (figura, cor_contorno, cor_preenchimento)
        self.ponto_previo_poligono = None
        self.cor_contorno = '#000000'
        self.cor_preenchimento = ''