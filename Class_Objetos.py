import pygame
import random
from configuraciones import *
from Class_Personaje import *

class Moneda(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0,):
        super().__init__()
        self.monedas_animacion = [
            pygame.image.load(r"Sprites\OBJECTOS\MONEDA\1.png"),
            pygame.image.load(r"Sprites\OBJECTOS\MONEDA\5.png"),
            pygame.image.load(r"Sprites\OBJECTOS\MONEDA\6.png"),
            pygame.image.load(r"Sprites\OBJECTOS\MONEDA\7.png"),
            pygame.image.load(r"Sprites\OBJECTOS\MONEDA\8.png"),
            pygame.image.load(r"Sprites\OBJECTOS\MONEDA\9.png"),
            pygame.image.load(r"Sprites\OBJECTOS\MONEDA\10.png"),
            pygame.image.load(r"Sprites\OBJECTOS\MONEDA\11.png"),
        ]
        
        self.indice_animacion = 0
        self.image = self.monedas_animacion[self.indice_animacion]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.reescalar_animacion(30, 30)

    def reescalar_animacion(self, ancho, alto):
        self.monedas_animacion = [pygame.transform.scale(img, (ancho, alto)) for img in self.monedas_animacion]

    
    def actualizar_animacion(self):
        self.indice_animacion = (self.indice_animacion + 1) % len(self.monedas_animacion)
        self.image = self.monedas_animacion[self.indice_animacion]

    def update(self, personaje):
        self.actualizar_animacion()
        if self.rect.colliderect(personaje.rectangulo_principal):
            personaje.score += random.randint(1,5)
            moneda_sonido.play()
            self.kill()
        if not self.alive():
            return