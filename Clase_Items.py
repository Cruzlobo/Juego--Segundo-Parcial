import pygame
import random
from configuraciones import *
from Class_Personaje import *

class Item(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__()
        self.items_animacion = [
            pygame.image.load(r"Sprites\OBJECTOS\AGUA\Light blue.png"),]

        self.indice_animacion = 0
        self.image = self.items_animacion[self.indice_animacion]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.reescalar_animacion(30, 30)

    def reescalar_animacion(self, ancho, alto):
        self.items_animacion = [pygame.transform.scale(img, (ancho, alto)) for img in self.items_animacion]

    def actualizar_animacion(self):
        self.indice_animacion = (self.indice_animacion + 1) % len(self.items_animacion)
        self.image = self.items_animacion[self.indice_animacion]

    def update(self, personaje):
        self.actualizar_animacion()
        if self.rect.colliderect(personaje.rectangulo_principal):
            personaje.aumentar_vida()
            botella_sonido.play()
            self.kill()
        if not self.alive():
            return