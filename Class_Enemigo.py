import random
from configuraciones import *
from Class_Disparo_Enemigo import *

class Enemigo:
    enemigos_generados = 0
    def __init__(self, animaciones, x, y, tipo , vida = 3):
        self.animaciones = animaciones
        reescalar_imagenes(self.animaciones, 150, 120)
        self.rectangulo = self.animaciones["izquierda"][0].get_rect()
        self.rectangulo.x = x
        self.rectangulo.y = y
        self.direccion = 0
        self.desplazamiento_y = 0
        self.desplazamiento_x = 0
        self.contador_pasos = 0
        self.animacion_actual = self.animaciones["izquierda"]
        self.esta_muerto = False
        self.esta_muriendo = False
        self.vida_maxima = vida
        self.salud = vida
        self.VELOCIDAD_ENEMIGO = 3
        self.tiempo_muerte = 0  
        self.TIEMPO_ANIMACION_MUERTE = 500
        self.distancia_disparo = 500  
        self.lista_disparos = [] 
        self.tiempo_entre_disparos = 2000 
        self.ultimo_disparo = pygame.time.get_ticks()
        self.tipo = tipo
        
        

    
    def aplicar_gravedad_enemigo(self, plataformas):
        velocidad_gravedad = 0.5 

        self.desplazamiento_y += velocidad_gravedad
        self.rectangulo.y += self.desplazamiento_y
        self.rectangulo.x += self.desplazamiento_x

        rectangulos_enemigo = obtener_rectangulos(
            self.rectangulo.x, self.rectangulo.y,
            self.rectangulo.width, self.rectangulo.height)

        for pl in plataformas:
            rectangulos_plataforma = obtener_rectangulos(
                pl["rectangulo"].x, pl["rectangulo"].y,
                pl["rectangulo"].width, pl["rectangulo"].height)
            
            if rectangulos_enemigo["bottom"].colliderect(rectangulos_plataforma["top"]):
                self.desplazamiento_y = 0
                self.rectangulo.bottom = pl["rectangulo"].top

            if rectangulos_enemigo["right"].colliderect(rectangulos_plataforma["left"]):
                self.desplazamiento_x = -self.VELOCIDAD_ENEMIGO  
                self.animacion_actual = self.animaciones["izquierda"]
            elif rectangulos_enemigo["left"].colliderect(rectangulos_plataforma["right"]):
                self.desplazamiento_x = self.VELOCIDAD_ENEMIGO  
                self.animacion_actual = self.animaciones["derecha"]

            

            

    def avanzar(self, plataformas):
        limite_izquierdo = 0
        limite_derecho = 1850

        if self.animacion_actual == self.animaciones["izquierda"]:
            self.rectangulo.x -= self.VELOCIDAD_ENEMIGO
            if self.rectangulo.x < limite_izquierdo:
                self.rectangulo.x = limite_izquierdo
                self.desplazamiento_x = self.VELOCIDAD_ENEMIGO  
                self.animacion_actual = self.animaciones["derecha"]

        elif self.animacion_actual == self.animaciones["derecha"]:
            self.rectangulo.x += self.VELOCIDAD_ENEMIGO
            if self.rectangulo.x > limite_derecho:
                self.rectangulo.x = limite_derecho
                self.desplazamiento_x = -self.VELOCIDAD_ENEMIGO  
                self.animacion_actual = self.animaciones["izquierda"]

        self.aplicar_gravedad_enemigo(plataformas)
    def animar(self, pantalla):
        largo = len(self.animacion_actual)
        if self.contador_pasos >= largo:
            self.contador_pasos = 0
        pantalla.blit(self.animacion_actual[self.contador_pasos], self.rectangulo)
        self.contador_pasos +=1

        if self.esta_muriendo and self.contador_pasos == largo:
            self.animacion_actual = self.animaciones["aplasta"]


    def reducir_vida(self):
        self.salud -= 1
        golpe_alien_sonido.play()
        if self.salud <= 0:
            self.esta_muerto = True
            muerte_alien_sonido.play()
            Enemigo.enemigos_generados += 1

        

    def actualizar(self, pantalla, plataformas):
        if not self.esta_muerto:
            self.animar(pantalla)
            if not self.esta_muriendo:
                self.avanzar(plataformas)
            else:
                self.reducir_vida()
    @classmethod
    def generar_enemigo_aleatorio(cls, max_enemigos):
        if cls.enemigos_generados < max_enemigos:
            diccionarios_enemigos = [
                {
                    "izquierda": enemigo_camina,
                    "aplasta": enemigo_aplasta,
                    "derecha": enemigo_camina_derecha
                },
                {
                    "izquierda": enemigo2_camina,
                    "aplasta": enemigo2_aplasta,
                    "derecha": enemigo2_camina_derecha
                }
            ]

            diccionario_enemigo = random.choice(diccionarios_enemigos)
            x = random.randint(0, 1850)
            y = random.randint(0, 50)
            vida = random.randint(2, 3)
            tipo = random.choice(["alien1", "alien2"])
            nuevo_enemigo = cls(diccionario_enemigo, x=x, y=y, vida=vida, tipo=tipo)
            cls.enemigos_generados += 1
            return nuevo_enemigo
        else:
            return None
    @classmethod
    def generar_enemigo_aleatorio_boss(cls):
        diccionarios_enemigos = [
            {
                "izquierda": enemigo_camina,
                "aplasta": enemigo_aplasta,
                "derecha": enemigo_camina_derecha
            },
            {
                "izquierda": enemigo2_camina,
                "aplasta": enemigo2_aplasta,
                "derecha": enemigo2_camina_derecha
            }
        ]

        diccionario_enemigo = random.choice(diccionarios_enemigos)
        x = random.randint(0, 1850)
        y = random.randint(0, 50)
        vida = random.randint(2, 3)
        tipo = random.choice(["alien1", "alien2"])
        nuevo_enemigo = cls(diccionario_enemigo, x=x, y=y, vida=vida, tipo=tipo)
        return nuevo_enemigo
        #statismetoh
    def crear_lista(plataformas):
        diccionario_enemigo = {}
        diccionario_enemigo2 = {}

        diccionario_enemigo["izquierda"] = enemigo_camina
        diccionario_enemigo["aplasta"] = enemigo_aplasta
        diccionario_enemigo["derecha"] = enemigo_camina_derecha

        diccionario_enemigo2["izquierda"] = enemigo2_camina
        diccionario_enemigo2["aplasta"] = enemigo2_aplasta
        diccionario_enemigo2["derecha"] = enemigo2_camina_derecha

        alien = Enemigo(diccionario_enemigo, x=1500, y=600, tipo="alien1", vida=3)

        alien2 = None
        if len(plataformas) > 2:
            alien2 = Enemigo(diccionario_enemigo2, x=plataformas[2]["rectangulo"].x + 50, y=plataformas[2]["rectangulo"].top - 120, tipo="alien2", vida=3)
            alien2.rectangulo.bottom = plataformas[2]["rectangulo"].top

        lista_enemigos = [alien]
        if alien2:
            lista_enemigos.append(alien2)
        
        return lista_enemigos
    def verificar_y_disparar(self, jugador):
        tiempo_actual = pygame.time.get_ticks()
        distancia_x = jugador.rectangulo_principal.x - self.rectangulo.x

        if tiempo_actual - self.ultimo_disparo > self.tiempo_entre_disparos and self.tipo == "alien2":
            if 0 < abs(distancia_x) <= self.distancia_disparo:
                direccion_disparo = "izquierda" if distancia_x < 0 else "derecha"
                self.disparar(direccion_disparo)
                self.ultimo_disparo = tiempo_actual

        self.lista_disparos = [disparo for disparo in self.lista_disparos if 0 < disparo.rectangulo.x < 1920]

    def disparar(self, direccion):
        
        x_disparo = self.rectangulo.x
        y_disparo = self.rectangulo.y + self.rectangulo.height // 2

        nuevo_disparo = DisparoEnemigo(x_disparo, y_disparo, direccion)
        self.lista_disparos.append(nuevo_disparo)

    def actualizar_disparos(self):
        for disparo in self.lista_disparos:
            disparo.actualizar()

        
        self.lista_disparos = [disparo for disparo in self.lista_disparos if 0 < disparo.rectangulo.x < 1920]
