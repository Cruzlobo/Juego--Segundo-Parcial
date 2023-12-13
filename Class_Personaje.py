import random
from Class_Disparo import Disparo
from configuraciones import *
class Personaje:
    def __init__(self, animaciones, tamaño, pos_x, pos_y, velocidad, vida = 2,
            tiempo_invulnerabilidad=3000, tiempo_animacion = 100):
        self.animaciones = animaciones
        reescalar_imagenes(self.animaciones, *tamaño)
        self.animaciones["Arrastra"] = [pygame.transform.scale(img, (90,100))
                        for img in self.animaciones["Arrastra"]]
        self.rectangulo_principal = animaciones["Quieto"][0].get_rect()
        self.rectangulo_principal.x = pos_x
        self.rectangulo_principal.y = pos_y
        self.bottom_width = 100
        self.velocidad = velocidad
        self.contador_pasos = 0
        self.que_hace = "Quieto"
        self.animacion_actual = self.animaciones["Quieto"]
        self.direccion = 1
        self.puerta_abierta = False
        self.lista_proyectiles = []
        self.desplazamiento_y = 0 
        self.potencia_salto = -18
        self.limite_velocidad_salto = 18
        self.esta_saltando = False
        self.gravedad = 1 
        self.vida_maxima= vida
        self.vida = vida
        self.tiempo_invulnerabilidad = tiempo_invulnerabilidad
        self.tiempo_invulnerable_inicio = pygame.time.get_ticks()
        self.tiempo_empujon = 500  
        self.tiempo_empujon_inicio = 0
        self.tiempo_animacion = tiempo_animacion
        self.tiempo_animacion_inicio = pygame.time.get_ticks()
        self.score = 0
        self.imagen_corazon_lleno = pygame.image.load("Sprites\OBJECTOS\VIDA\\3.png")
        self.imagen_corazon_lleno = pygame.transform.scale(self.imagen_corazon_lleno,
                                (50, 50))
        self.imagen_corazon_vacio = pygame.image.load("Sprites\OBJECTOS\VIDA\\0.png")
        self.imagen_corazon_vacio = pygame.transform.scale(self.imagen_corazon_vacio,
                                (50, 50))

    def caminar(self, pantalla):
        velocidad_actual =  self.velocidad
        if self.que_hace == "Izquierda":
            velocidad_actual *= -1
            
        nueva_posicion = self.rectangulo_principal.x + velocidad_actual
        if nueva_posicion > 0 and nueva_posicion <= (pantalla.get_width()
                                - self.rectangulo_principal.width):
            self.rectangulo_principal.x += velocidad_actual

    def animar_personaje(self, pantalla):
        tiempo_actual = pygame.time.get_ticks()
        tiempo_pasado = tiempo_actual - self.tiempo_animacion_inicio
        largo = len(self.animacion_actual)
        if tiempo_pasado >= self.tiempo_animacion:
            self.contador_pasos += 1
            self.tiempo_animacion_inicio = tiempo_actual
            if self.contador_pasos >= largo:
                self.contador_pasos = 0
        if 0 <= self.contador_pasos < largo:
            pantalla.blit(self.animacion_actual[self.contador_pasos],
                        self.rectangulo_principal)

    def animar_empujon(self, pantalla, direccion_empujon):
        tiempo_actual = pygame.time.get_ticks()
        
        if tiempo_actual - self.tiempo_empujon_inicio < self.tiempo_empujon:
            if direccion_empujon == "izquierda":
                self.animacion_actual = self.animaciones["Empujon"]
            elif direccion_empujon == "derecha":
                self.animacion_actual = self.animaciones["Empujon_derecha"]

            self.animar_personaje(pantalla)
        else:
            self.siendo_empujado = False
            self.que_hace = "Quieto"
            self.animacion_actual = self.animaciones["Quieto"]
            self.animar_personaje(pantalla)
    
    def animar_disparos(self, pantalla):
        for disparo in self.lista_proyectiles:
            pantalla.blit(disparo.superficie, disparo.rectangulo)

    def mostrar_vida(self, pantalla):
        ancho_corazon = 20
        for i in range(self.vida_maxima):
            x = i * (ancho_corazon + 20 ) 
            y = 25 
            if i < self.vida:
                pantalla.blit(self.imagen_corazon_lleno, (x, y))
            else:
                pantalla.blit(self.imagen_corazon_vacio, (x, y))

    def reducir_vida(self, direccion_colision):
        tiempo_actual = pygame.time.get_ticks()

        if (tiempo_actual - self.tiempo_invulnerable_inicio
            > self.tiempo_invulnerabilidad):
            self.vida -= 1
            self.score -= random.randint(1,7)
            self.tiempo_invulnerable_inicio = tiempo_actual

            if self.vida <= 0:
                print("Game Over: El personaje ha muerto")
            else:
                golpe_sonido.play()
                distancia_empujon = 100 
                if direccion_colision == "izquierda":
                    self.que_hace == "Empujon"
                    self.animacion_actual = self.animaciones["Empujon"]
                    self.rectangulo_principal.x -= distancia_empujon
                elif direccion_colision == "derecha":
                    self.rectangulo_principal.x += distancia_empujon
                self.tiempo_empujon_inicio = tiempo_actual

    def aumentar_puntos(self):
        self.score += random.randint(5,15)
    def aumentar_vida (self):
        self.vida += 1
        if self.vida >=5:
            self.vida = 5
    def actualizar(self, pantalla, plataformas):
        match self.que_hace:
            case "Derecha":
                if not self.esta_saltando:
                    self.animacion_actual = self.animaciones["Derecha"]
                    self.animar_personaje(pantalla)
                self.caminar(pantalla)
            case "Izquierda":
                if not self.esta_saltando:
                    self.animacion_actual = self.animaciones["Izquierda"]
                    self.animar_personaje(pantalla)
                self.caminar(pantalla)
            case "Salta":
                if not self.esta_saltando:
                    self.esta_saltando = True
                    self.desplazamiento_y = self.potencia_salto
                    self.animacion_actual = self.animaciones["Salta"]
            case "Salta_izquierda":
                if not self.esta_saltando:
                    self.esta_saltando = True
                    self.desplazamiento_y = self.potencia_salto
                    self.animacion_actual = self.animaciones["Salta_izquierda"]
            case "Arrastra":
                if not self.esta_saltando:
                    self.animacion_actual = self.animaciones["Arrastra"]
                    
                    self.animar_personaje(pantalla)
                    
            case "Quieto":
                if not self.esta_saltando:
                    self.animacion_actual = self.animaciones["Quieto"]
                    self.animar_personaje(pantalla)
            case "Quieto_izquierda":
                if not self.esta_saltando:
                    self.animacion_actual = self.animaciones["Quieto_izquierda"]
                    self.animar_personaje(pantalla)
            case "Dispara":
                if not self.esta_saltando:
                    self.animacion_actual = self.animaciones["Dispara"]
                    self.animar_personaje(pantalla)
            case "Dispara_izquierda":
                self.animacion_actual = self.animaciones["Dispara_izquierda"]
                self.animar_personaje(pantalla)
                self.actualizar_disparos(pantalla)
            case "Empujon":
                self.animacion_actual = self.animaciones["Empujon"]
                self.animar_personaje(pantalla)
        self.actualizar_disparos(pantalla)
        self.mostrar_vida(pantalla)
        self.aplicar_gravedad(pantalla, plataformas)

    def aplicar_gravedad(self, pantalla, plataformas):
        if self.esta_saltando:
            self.animar_personaje(pantalla)
            self.rectangulo_principal.y += self.desplazamiento_y
            if (self.desplazamiento_y + self.gravedad 
                < self.limite_velocidad_salto):
                self.desplazamiento_y += self.gravedad

        if self.rectangulo_principal.y < 0:
            self.rectangulo_principal.y = 0
            self.desplazamiento_y = 0
            self.esta_saltando = False  
        rectangulos_personaje = obtener_rectangulos(self.rectangulo_principal.x,
                self.rectangulo_principal.y,
                self.rectangulo_principal.width,
                self.rectangulo_principal.height)
        rectangulos_personaje["bottom"].width = self.bottom_width

        for pl in plataformas:
            rectangulos_plataforma = obtener_rectangulos(pl["rectangulo"].x,
                        pl["rectangulo"].y,
                        pl["rectangulo"].width,
                        pl["rectangulo"].height)
            rectangulos_plataforma["left"].inflate_ip(2, 0)  
            rectangulos_plataforma["right"].inflate_ip(2, 0)
            if rectangulos_personaje["bottom"].colliderect(rectangulos_plataforma["top"]):
                if self.desplazamiento_y >= 0:  
                    self.esta_saltando = False
                    self.desplazamiento_y = 0
                    self.rectangulo_principal.bottom = pl["rectangulo"].top
                break
            if rectangulos_personaje["right"].colliderect(rectangulos_plataforma["left"]):
                self.rectangulo_principal.right = pl["rectangulo"].left
                self.rectangulo_principal.x -= self.velocidad
            if rectangulos_personaje["left"].colliderect(rectangulos_plataforma["right"]):
                self.rectangulo_principal.left = pl["rectangulo"].right
                self.rectangulo_principal.x += self.velocidad
        else:
            if not self.esta_saltando:
                self.esta_saltando = True

    def romper_objecto(self, lista_plataformas, flor):
        for plataforma in lista_plataformas:
            if plataforma["premio"]:
                if self.rectangulo_principal.colliderect(plataforma["rectangulo"]):
                    flor["descubierta"] = True
                    plataforma["premio"] = False

    def lanzar_disparos(self,pantalla):
        x = None
        margen = 10
        
        y = self.rectangulo_principal.centery - 10
        if self.que_hace == "Derecha" or self.que_hace == "Quieto":
            self.animacion_actual = self.animaciones["Dispara"]
            x = self.rectangulo_principal.right - margen
        elif self.que_hace in ["Izquierda", "Quieto_izquierda"] :
            self.animacion_actual = self.animaciones["Dispara_izquierda"]
            x = self.rectangulo_principal.left - 50 + margen
        if x is not None:
            self.lista_proyectiles.append(Disparo(x, y, self.que_hace))
            self.animar_disparos(pantalla)  
        arma_sonido.play()
    def actualizar_disparos(self, pantalla):
        i = 0
        while i < len(self.lista_proyectiles):
            p = self.lista_proyectiles[i]
            pantalla.blit(p.superficie, p.rectangulo)
            p.actualizar()
            if p.rectangulo.right < 0 or p.rectangulo.left > pantalla.get_width():
                print("Disparo eliminado:", p.rectangulo.x, p.rectangulo.y)
                self.lista_proyectiles.pop(i)
            else:
                i += 1