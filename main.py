# main.py - Ponto de entrada do programa (padrão MVC)
from tkinter import Tk

from view import PaintView
from controller import PaintController


def main():
    root = Tk()

    # PaintView precisa do controller (para os comandos dos botões) e
    # PaintController precisa da view (para o canvas e os binds de mouse).
    # Pra resolver isso criamos o controller
    # (sem rodar __init__), passamos para a view, e só então inicializamos
    # o controller de verdade, já com a view pronta.
    controller = PaintController.__new__(PaintController)
    view = PaintView(root, controller)
    controller.__init__(view)

    root.mainloop()


if __name__ == '__main__':
    main()