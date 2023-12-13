import pygame

class DisparoEnemigo:
    def __init__(self, x, y, direccion):
        try:
            self.superficie = pygame.image.load(r"Sprites\disparo\495.png")
            self.superficie = pygame.transform.scale(self.superficie, (20, 20))
        except pygame.error as e:
            print(f"Error cargando la imagen del disparo: {e}")
        self.rectangulo = self.superficie.get_rect()
        self.rectangulo.center = (x, y)
        self.direccion = direccion
        self.velocidad = 10 if direccion == "izquierda" else -10

    def actualizar(self):
        self.rectangulo.x -= self.velocidad