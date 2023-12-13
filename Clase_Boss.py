import pygame
from Class_disparo_boss import DisparoBoss
from configuraciones import *

class Boss(pygame.sprite.Sprite):
    def __init__(self, personaje, boss_group):
        super().__init__()

        self.animaciones = boss
        self.sprite_muerte = pygame.image.load(r"Sprites\BOSS\\40.png").convert_alpha()
        self.sprite_muerte = pygame.transform.scale(self.sprite_muerte, (200, 200))  
        self.rect = self.animaciones[0].get_rect()

        self.rect.x = 1715  
        self.rect.y = 0  

        self.personaje = personaje
        self.speed = 3
        self.current_frame = 0
        self.velocidad = -5
        self.direccion = "right"  
        self.esta_muerto = False
        self.intervalo_disparo = 2000
        self.ultimo_disparo = pygame.time.get_ticks()
        self.vida = 100
        self.vida_maxima = 100
        self.boss_group = boss_group
        self.lista_disparos =[]

    def update(self):
        if not self.esta_muerto:
            self.mover()
            self.animar()

            tiempo = pygame.time.get_ticks()
            if tiempo - self.ultimo_disparo > self.intervalo_disparo:
                self.disparo()
                self.ultimo_disparo = tiempo

            for disparo in self.lista_disparos:
                disparo.actualizar()

            if self.vida <= 0:
                self.image = self.sprite_muerte
                self.esta_muerto = True
        else:
            self.image = self.sprite_muerte
            

    def mover(self):
        if self.direccion == "right":
            self.rect.y += self.speed
            if self.rect.y > 1000 - self.rect.height:
                self.rect.y = 1000 - self.rect.height
                self.direccion = "left"
        elif self.direccion == "left":
            self.rect.y -= self.speed
            if self.rect.y < 0:
                self.rect.y = 0
                self.direccion = "right"

    def animar(self):
        self.current_frame = (self.current_frame + 1) % len(self.animaciones)
        self.image = self.animaciones[self.current_frame]

    def disparo(self):
        x_disparo = self.rect.x
        y_disparo = self.rect.y + self.rect.height // 2
        nuevo_disparo = DisparoBoss(x_disparo, y_disparo, "left") 
        self.lista_disparos.append(nuevo_disparo)
    def reducir_vida(self,personaje):
        if not self.esta_muerto:  
            self.vida -= 5
            personaje.aumentar_puntos()
            golpe_alien_sonido.play()
            if self.vida <= 0:
                self.esta_muerto = True
                muerte_alien_sonido.play()
                