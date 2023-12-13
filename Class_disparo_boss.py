import pygame
from configuraciones import *

class DisparoBoss(pygame.sprite.Sprite):
    def __init__(self, x, y, direccion):
        super().__init__()
        self.animacion_disparo = disparo_boss
        self.rect = self.animacion_disparo[0].get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidad = 10 
        self.direccion = direccion
        self.current_frame = 0
        self.velocidad = 5

        self.image = self.animacion_disparo[self.current_frame]

    def actualizar(self):
        if self.direccion == "right":
            self.rect.x += self.velocidad
        elif self.direccion == "left":
            self.rect.x -= self.velocidad

    def animate(self):
        self.current_frame = (self.current_frame + 1) % len(self.animacion_disparo)
        self.image = self.animacion_disparo[self.current_frame]

    