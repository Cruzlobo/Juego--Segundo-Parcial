import pygame

class Disparo:
    def __init__(self, x, y, direccion):
        self.superficie = pygame.image.load(r"Sprites\\disparo\495.png")
        self.superficie = pygame.transform.scale(self.superficie, (20, 20))
        self.rectangulo = pygame.Rect(x - self.superficie.get_width() // 2, y, self.superficie.get_width(), self.superficie.get_height())
        self.direccion = direccion

    def actualizar(self):
        if self.direccion in ["Derecha","Quieto"]:
            self.rectangulo.x += 10
        elif self.direccion in ["Izquierda","Quieto_izquierda"]:
            self.rectangulo.x -= 10
