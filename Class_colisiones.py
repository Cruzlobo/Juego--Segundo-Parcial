import pygame 
from configuraciones import *
class Colisiones:
    @staticmethod
    def verificar_colision_personaje_enemigo(personaje, lista_enemigos, pantalla):
        for enemigo in lista_enemigos:
            if enemigo is not None and hasattr(enemigo, 'rectangulo'):
                if personaje.rectangulo_principal.colliderect(enemigo.rectangulo):
                    rectangulos_personaje = obtener_rectangulos(
                        personaje.rectangulo_principal.x,
                        personaje.rectangulo_principal.y,
                        personaje.rectangulo_principal.width,
                        personaje.rectangulo_principal.height
                    )
                    if rectangulos_personaje["right"].colliderect(enemigo.rectangulo):
                        personaje.reducir_vida(direccion_colision="izquierda")
                        direccion_colision="izquierda"
                        personaje.animar_empujon(pantalla,direccion_colision)
                    elif rectangulos_personaje["left"].colliderect(enemigo.rectangulo):
                        personaje.reducir_vida(direccion_colision="derecha")
                        direccion_colision="derecha"
                        personaje.animar_empujon(pantalla,direccion_colision)
                        
    @staticmethod
    def verificar_colision_disparo_personaje(lista_disparos, lista_enemigos,lista_plataformas):
        i = 0
        while i < len(lista_disparos):
            disparo = lista_disparos[i]
            for enemigo in lista_enemigos:
                if enemigo is not None and hasattr(enemigo, 'esta_muriendo') and hasattr(enemigo, 'esta_muerto'):
                    if not enemigo.esta_muriendo and not enemigo.esta_muerto:
                        if disparo.rectangulo.colliderect(enemigo.rectangulo):
                            enemigo.reducir_vida()
                            if enemigo.salud <= 0:
                                enemigo.esta_muriendo = True
                            lista_disparos.pop(i)
                            i -= 1
                            break
            for plataforma in lista_plataformas:
                if disparo.rectangulo.colliderect(plataforma["rectangulo"]):
                    lista_disparos.pop(i)
                    i -= 1
                    break 
            i += 1
    def verificar_colision_disparo_personaje_nivel3(lista_disparos, lista_enemigos):
        for i in range(len(lista_disparos)-1, -1, -1):
            disparo = lista_disparos[i]
            for enemigo in lista_enemigos:
                if enemigo is not None and hasattr(enemigo, 'esta_muriendo') and hasattr(enemigo, 'esta_muerto'):
                    if not enemigo.esta_muriendo and not enemigo.esta_muerto:
                        if disparo.rectangulo.colliderect(enemigo.rectangulo):
                            enemigo.reducir_vida()
                            if enemigo.salud <= 0:
                                enemigo.esta_muriendo = True
                            lista_disparos.pop(i)
                            i -= 1
                            break
    def verificar_colision_disparo_personaje_boss(personaje, boss):
        for disparo_personaje in personaje.lista_proyectiles:
            if boss.rect.colliderect(disparo_personaje.rectangulo):
                boss.reducir_vida(personaje) 
                if disparo_personaje in personaje.lista_proyectiles:
                    personaje.lista_proyectiles.remove(disparo_personaje)
                print(boss.vida)
    def verificar_colision_disparo_enemigo(lista_disparos_enemigos, personaje, pantalla):
        i = 0
        while i < len(lista_disparos_enemigos):
            disparo = lista_disparos_enemigos[i]

            if personaje.rectangulo_principal.colliderect(disparo.rectangulo):
                rectangulos_personaje = obtener_rectangulos(
                    personaje.rectangulo_principal.x,
                    personaje.rectangulo_principal.y,
                    personaje.rectangulo_principal.width,
                    personaje.rectangulo_principal.height
                )

                if rectangulos_personaje["right"].colliderect(disparo.rectangulo):
                    personaje.reducir_vida(direccion_colision="izquierda")
                    direccion_colision = "izquierda"
                    personaje.animar_empujon(pantalla, direccion_colision)
                elif rectangulos_personaje["left"].colliderect(disparo.rectangulo):
                    personaje.reducir_vida(direccion_colision="derecha")
                    direccion_colision = "derecha"
                    personaje.animar_empujon(pantalla, direccion_colision)

                lista_disparos_enemigos.pop(i)
                i -= 1

            i += 1
    def verificar_colision_disparo_boss(personaje, boss, PANTALLA):
        for disparo_boss in boss.lista_disparos:
            if personaje.rectangulo_principal.colliderect(disparo_boss.rect):
                personaje.reducir_vida("izquierda")
                direccion_colision = "izquierda"
                personaje.animar_empujon(PANTALLA, direccion_colision)
                boss.lista_disparos.remove(disparo_boss)
    
    def verificar_colision_personaje_moneda(personaje, lista_monedas):
        for moneda in lista_monedas:
            if moneda and hasattr(moneda, 'rectangulo'):
                if pygame.sprite.collide_rect(personaje, moneda):
                    moneda.verificar_colision_personaje(personaje)
    

    def dibujar_barra_salud(self, pantalla, lista_enemigos):
        for enemigo in lista_enemigos:
            if enemigo is not None and hasattr(enemigo, 'rectangulo'):
                barra_salud_rect = pygame.Rect(enemigo.rectangulo.x, enemigo.rectangulo.y - 10, enemigo.rectangulo.width, 5)
                pygame.draw.rect(pantalla, "white", barra_salud_rect) 
                if enemigo.salud > 0 and enemigo.vida_maxima > 0:
                    barra_salud_rect.width = (enemigo.salud / enemigo.vida_maxima) * enemigo.rectangulo.width
                    pygame.draw.rect(pantalla, "red", barra_salud_rect)
    def dibujar_barra_salud_boss(self, pantalla, boss):
        fuente = pygame.font.Font( "fonts\monogram.ttf", 40)
        if boss is not None and hasattr(boss, 'rect'):
            # Ajusta las coordenadas de la barra de salud a la posición deseada
            barra_salud_rect = pygame.Rect(855, 100, boss.rect.width, 25)
            pygame.draw.rect(pantalla, "white", barra_salud_rect)
            
            if boss.vida > 0 and boss.vida_maxima > 0:
                barra_salud_rect.width = (boss.vida / boss.vida_maxima) * boss.rect.width
                pygame.draw.rect(pantalla, "red", barra_salud_rect)
                dibujar_texto("Xerthrok", fuente,(0,0,0),900,92, pantalla)