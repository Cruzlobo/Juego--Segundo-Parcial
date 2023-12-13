import pygame, sys
import csv
from pygame.locals import *
from Class_Personaje import *
from Class_Enemigo import *
from configuraciones import *
from Class_colisiones import *
from Class_Objetos import *
from Modo import *
from Clase_Items import *


##############################INICIALIZACIONES##########################################

#############Pantalla##########
#ANCHO W - ALTO H
W,H = 1920,1080
FPS = 20

pygame.init()

RELOJ = pygame.time.Clock()  
PANTALLA = pygame.display.set_mode((W, H))

#Fondo
fondo = pygame.image.load(r"Sprites\MAPA_NOCHE\0.png").convert()
fondo.set_colorkey([248, 0, 248])
fondo = pygame.transform.scale(fondo, (W,H))

fuente = pygame.font.Font( "fonts\monogram.ttf", 60)
fuente2 = pygame.font.Font( "fonts\monogram.ttf", 40)

#PERSONAJE

diccionario = {}
diccionario["Quieto"] = personaje_quieto
diccionario["Quieto_izquierda"] = personaje_quieto_izquierda
diccionario["Derecha"] = personaje_corre
diccionario["Izquierda"] = personaje_corre_izquierda
diccionario["Salta"] = personaje_salta
diccionario["Salta_izquierda"] = personaje_salta_izquierda
diccionario["Arrastra"] = personaje_arrastra
diccionario["Dispara"] = personaje_dispara
diccionario["Dispara_izquierda"] = personaje_dispara_izquierda
diccionario["Empujon"] = personaje_empujon
diccionario["Empujon_derecha"] = personaje_empujon_derecha

personaje = Personaje(diccionario, (130,100), 50,850,10, 5)

monedas = pygame.sprite.Group()  
moneda = Moneda(700, 600)
moneda2 = Moneda(250, 300) 
moneda3 = Moneda(500, 700) 
moneda4 = Moneda(1350, 320) 
monedas.add(moneda4,moneda3,moneda2,moneda)



items = pygame.sprite.Group()
botella = Item(550, 430) 
botella2 = Item(1650, 487)
items.add(botella,botella2)
################PLATAFORMAS#####################
menu = pygame.image.load(r"Sprites\niveles\0.png")

menu = pygame.transform.scale(menu,(455,220))


imagen_plataforma = pygame.image.load(r"Sprites\OBJECTOS\PLATAFORMA\0.png")


imagen_plataforma= pygame.transform.scale(imagen_plataforma,(200,9))


imagen_score = pygame.image.load(r"Sprites\niveles\2.png")

imagen_temporizador = pygame.image.load(r"Sprites\niveles\2.png")

imagen_temporizador = pygame.transform.scale(imagen_temporizador,(140,50))
imagen_score = pygame.transform.scale(imagen_score,(220,50))
puerta_imagen = pygame.image.load(r"Sprites\PUERTAS\0.png")
puerta_imagen =pygame.transform.scale(puerta_imagen,(130,130))

piso = crear_plataforma("",W,100,0,0,False)
piso2 = crear_plataforma("",W,50,0,970,False)
piso["rectangulo"].top = personaje.rectangulo_principal.bottom
plataforma_puerta = crear_plataforma(r"Sprites\PUERTAS\0.png", 130,130,0,0,True)
plataforma_puerta["rectangulo"].x = 1920
plataforma_puerta["rectangulo"].bottom = piso["rectangulo"].top 
plataforma_invisible = crear_plataforma("", 440, 30, 748 , 490, False)      
plataforma_invisible1 = crear_plataforma("", 10, 30, 758 , 480, False)
plataforma_invisible2 = crear_plataforma("", 10, 30, 1180 , 480, False)
plataforma_invisible3 = crear_plataforma("", 200, 10, 1280 , 660, False)
plataforma_invisible4 = crear_plataforma("", 200, 10, 1550 , 500, False)
plataforma_invisible5 = crear_plataforma("", 200, 10, 600 , 715, False)
plataforma_invisible6 = crear_plataforma("", 200, 10, 133 , 390, False)
plataforma_invisible6 = crear_plataforma("", 200, 10, 400, 800, False)
plataforma_invisible7 = crear_plataforma("", 200, 10, 200, 600, False)
plataforma_invisible8 = crear_plataforma("", 200, 10, 453, 490, False)


plataformas = [piso, plataforma_puerta, plataforma_invisible,
            plataforma_invisible1,plataforma_invisible2,
            plataforma_invisible3,plataforma_invisible4,
            plataforma_invisible5,plataforma_invisible6,
            plataforma_invisible7,plataforma_invisible8,
            piso2]

##############ENEMIGOS##########################

lista_enemigos = Enemigo.crear_lista(plataformas)

##############COLIPSIONES#######################
colisiones = Colisiones()
duracion_temporizador = 60 * 1000  # 90 segundos
tiempo_inicio = pygame.time.get_ticks()
contador_enemigos_derrotados = 1
flag_dispara = False
tiempo_ultimo_disparo = 0 
mira_Derecha = None
max_enemigos = 7
pygame.mixer.music.load(r'Sonidos\Mapa\Noche.wav')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)
pausa = False
menu_pausa_visible = False
sonido_musica_mute = False
sonido_efectos_mute = False

puntos_por_segundo = 10
csv_file_path = "puntajes2.csv"  
csv_header = ["Jugador", "Puntuacion"] 
def mostrar_menu_pausa():
    global menu_pausa_visible, sonido_musica_mute, sonido_efectos_mute

    menu_pausa_visible = True
    while menu_pausa_visible:
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit(0)
            
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_p:
                    menu_pausa_visible = False
                elif evento.key == pygame.K_m:
                    sonido_musica_mute = not sonido_musica_mute
                    pygame.mixer.music.set_volume(0.0 if sonido_musica_mute else 0.5)
                elif evento.key == pygame.K_e:
                    sonido_efectos_mute = not sonido_efectos_mute
                    golpe_alien_sonido.set_volume(0.0 if sonido_efectos_mute else 0.5)
                    golpe_sonido.set_volume(0.0 if sonido_efectos_mute else 0.5)
                    moneda_sonido.set_volume(0.0 if sonido_efectos_mute else 0.5)
                    arma_sonido.set_volume(0.0 if sonido_efectos_mute else 0.5)
                    muerte_alien_sonido.set_volume(0.0 if sonido_efectos_mute else 0.5)
                    botella_sonido.set_volume(0.0 if sonido_efectos_mute else 0.5)
                    
            PANTALLA.blit(menu,(745,370))
            dibujar_texto(f"Oprime M para mutear Musica",fuente2,(255,255,255),760,450,PANTALLA)
            dibujar_texto(f"Oprime E para mutear Efectos",fuente2,(255,255,255),760,500,PANTALLA)

        pygame.display.update()

while True:
    RELOJ.tick(FPS) 

    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
            sys.exit(0)
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            print(evento.pos)
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_TAB:
                cambiar_modo()
            elif evento.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit(0)
            elif evento.key == pygame.K_p:
                pausa = not pausa
                if pausa:
                    mostrar_menu_pausa()
    if pausa:
        continue  
    tiempo_actual = pygame.time.get_ticks()
    tiempo_transcurrido = tiempo_actual - tiempo_inicio
    tiempo_restante = max(0, duracion_temporizador - tiempo_transcurrido)  

    segundos_restantes = tiempo_restante // 1000
    minutos_restantes = segundos_restantes // 60
    segundos_restantes %= 60

    tiempo_formato = f"{minutos_restantes:02}:{segundos_restantes:02}"
    if tiempo_transcurrido >= duracion_temporizador:
        print("¡Tiempo agotado! Has perdido.")
        tiempo_inicio = pygame.time.get_ticks()
        PANTALLA.fill(COLOR_NEGRO)
        game_over_texto = pygame.font.Font(None, 62).render("!Mision Fallida!", True, (255, 0, 0))
        PANTALLA.blit(game_over_texto, (W // 2 - 100, H // 2 - 50))
        pygame.display.flip()
        pygame.time.wait(1000) 
        personaje = Personaje(diccionario, (150,120), 50,850,10, 5)
        lista_enemigos = Enemigo.crear_lista(plataformas)
        tiempo_inicio = pygame.time.get_ticks()
    keys = pygame.key.get_pressed()

    if keys[pygame.K_l]:
        pygame.mixer.music.set_volume(0.0)
    if keys[pygame.K_d]:
        personaje.que_hace = "Derecha"
        mira_Derecha = True
    elif keys[pygame.K_a]:
        personaje.que_hace = "Izquierda"
        mira_Derecha = False
    else:
        if mira_Derecha:
            personaje.que_hace = "Quieto"
        else:
            personaje.que_hace = "Quieto_izquierda"

    if keys[pygame.K_w] and not personaje.esta_saltando:
        if mira_Derecha:
            personaje.que_hace = "Salta"
        else:
            personaje.que_hace = "Salta_izquierda"
    elif keys[pygame.K_s]:
        personaje.que_hace = "Arrastra"
    

#########################DISPAROS#######################################
    tiempo_actual = pygame.time.get_ticks()
    if keys[pygame.K_SPACE]:
        if not flag_dispara: 
            if tiempo_actual - tiempo_ultimo_disparo >= 500:
                personaje.lanzar_disparos(PANTALLA)
                if mira_Derecha:
                    personaje.que_hace = "Dispara"
                else:
                    personaje.que_hace = "Dispara_izquierda"
                flag_dispara = True
                tiempo_ultimo_disparo = tiempo_actual
                
    else:
        flag_dispara = False
################################################################### 
    

    PANTALLA.blit(fondo, (0, 0))
    PANTALLA.blit(plataforma_puerta["imagen"], plataforma_puerta["rectangulo"])
    PANTALLA.blit(imagen_plataforma,(1280, 660))
    PANTALLA.blit(imagen_plataforma,(1550,500))
    PANTALLA.blit(imagen_plataforma,(600,715))
    PANTALLA.blit(imagen_plataforma,(453,490))
    PANTALLA.blit(imagen_plataforma,(400,800))
    PANTALLA.blit(imagen_plataforma,(200,600))
    PANTALLA.blit(imagen_score,(1680,20))   
    PANTALLA.blit(imagen_temporizador,(890,30))
    dibujar_texto(tiempo_formato, fuente, (255, 0, 0), 900, 30,PANTALLA)

    items.update(personaje)
    items.draw(PANTALLA)
    monedas.update(personaje)
    for moneda in monedas.sprites():
        PANTALLA.blit(moneda.image, moneda.rect)
    personaje.actualizar(PANTALLA, plataformas)
    colisiones.verificar_colision_personaje_enemigo(personaje, lista_enemigos,PANTALLA)
    Colisiones.verificar_colision_disparo_personaje(personaje.lista_proyectiles, lista_enemigos, plataformas)
    Colisiones.verificar_colision_personaje_moneda(personaje, monedas)
    Colisiones.dibujar_barra_salud( None,PANTALLA, lista_enemigos)
    personaje.animar_personaje(PANTALLA)  
    dibujar_texto(f"Score:{personaje.score}", fuente, (255,0,0),1700,20,PANTALLA)
    if personaje.vida <= 0:
        PANTALLA.fill(COLOR_NEGRO)
        game_over_texto = pygame.font.Font(None, 62).render("!!Mision Fallida!!", True, (255, 0, 0))
        dibujar_texto("!!Has muerto en combate!!",fuente,(255,255,255),600,600,PANTALLA)
        dibujar_texto("!!El enemigo se ha apoderado del mundo!!",fuente,(255,255,255),600,650,PANTALLA)
        PANTALLA.blit(game_over_texto, (W // 2 - 100, H // 2 - 50))
        pygame.display.flip()
        pygame.time.wait(5000) 
        personaje = Personaje(diccionario, (150,120), 50,850,10, 5)
        lista_enemigos = Enemigo.crear_lista(plataformas)
    
    for enemigo in lista_enemigos:
        if enemigo is not None and hasattr(enemigo, 'esta_muriendo'):
            if not enemigo.esta_muriendo and not enemigo.esta_muerto:
                enemigo.actualizar(PANTALLA, plataformas)

    for enemigo in lista_enemigos:
        if enemigo is not None and hasattr(enemigo, 'esta_muerto'):
            if enemigo.esta_muerto:
                enemigo.animar(PANTALLA)
                if not enemigo.tiempo_muerte:
                    enemigo.tiempo_muerte = pygame.time.get_ticks()

                tiempo_transcurrido = pygame.time.get_ticks() - enemigo.tiempo_muerte
                if tiempo_transcurrido > enemigo.TIEMPO_ANIMACION_MUERTE:
                    lista_enemigos.remove(enemigo) 
                    personaje.aumentar_puntos()
                    del enemigo
                    contador_enemigos_derrotados +=1
                    if len(lista_enemigos) < max_enemigos:
                        nuevo_enemigo = Enemigo.generar_enemigo_aleatorio(8)
                        lista_enemigos.append(nuevo_enemigo)
    for enemigo in lista_enemigos:
        if enemigo is not None and not enemigo.esta_muerto:
            enemigo.verificar_y_disparar(personaje)
            enemigo.actualizar_disparos()
    for enemigo in lista_enemigos:
        if enemigo is not None and hasattr(enemigo, 'lista_disparos'):
            for disparo in enemigo.lista_disparos:
                PANTALLA.blit(disparo.superficie, disparo.rectangulo)
                Colisiones.verificar_colision_disparo_enemigo(enemigo.lista_disparos, personaje, PANTALLA)
    if contador_enemigos_derrotados == max_enemigos:
        puntos_obtenidos = tiempo_restante * puntos_por_segundo // 1000
        personaje.score += puntos_obtenidos
        puntajes = cargar_puntajes(csv_file_path)
        mostrar_puntajes_final(puntajes, puntos_obtenidos, PANTALLA, W)
        pygame.time.delay(2000)
        PANTALLA.fill((0,0,0))
        dibujar_texto(f"Score obtenido:{personaje.score}", fuente, (255,0,0),730,300,PANTALLA)
        dibujar_texto("Mision completada.",fuente,(255,0,0),750,500,PANTALLA)
        dibujar_texto("El enemigo ha sido derrotado. ¡Gran trabajo, soldado!",fuente,(255,255,255),450,600,PANTALLA)
        dibujar_texto("Regresas a la base para reorganizarte y prepararte...",fuente,(255,255,255),450,700,PANTALLA)
        dibujar_texto("el momento mas importante a llegado es hora de ...",fuente,(255,255,255),450,800,PANTALLA)
        dibujar_texto("... atacar a su lider!!",fuente,(255,255,255),450,900,PANTALLA)
        with open(csv_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)

            if file.tell() == 0:
                writer.writerow(csv_header)

            
            jugador = "Lobo"  
            writer.writerow([jugador, personaje.score])
        
        pygame.display.flip()
        pygame.time.wait(10000)  
        pygame.quit()
        sys.exit(0)
    if get_mode() == True:
        rectangulos_personaje = obtener_rectangulos(
        personaje.rectangulo_principal.x,personaje.rectangulo_principal.y,
        personaje.rectangulo_principal.width,
        personaje.rectangulo_principal.height)

        pygame.draw.rect(PANTALLA, "green", rectangulos_personaje["main"], 2)
        pygame.draw.rect(PANTALLA, "blue", rectangulos_personaje["bottom"],2)
        pygame.draw.rect(PANTALLA, "red", rectangulos_personaje["right"],2)
        pygame.draw.rect(PANTALLA, "red", rectangulos_personaje["left"],2)
        pygame.draw.rect(PANTALLA, "red", rectangulos_personaje["top"],2)
        for plataforma in plataformas:
            rectangulos_plataforma = obtener_rectangulos(plataforma["rectangulo"].x, plataforma["rectangulo"].y, plataforma["rectangulo"].width, plataforma["rectangulo"].height)
            pygame.draw.rect(PANTALLA, "yellow", rectangulos_plataforma["bottom"],1)
            pygame.draw.rect(PANTALLA, "yellow", rectangulos_plataforma["right"],1)
            pygame.draw.rect(PANTALLA, "yellow", rectangulos_plataforma["left"],1)
            pygame.draw.rect(PANTALLA, "black", rectangulos_plataforma["top"],1)
        for enemigo in lista_enemigos:
            if enemigo is not None and hasattr(enemigo, 'rectangulo'):
                enemigo_rectangulos = obtener_rectangulos(
                    enemigo.rectangulo.x,
                    enemigo.rectangulo.y,
                    enemigo.rectangulo.width,
                    enemigo.rectangulo.height)
                if "bottom" in enemigo_rectangulos:
                    pygame.draw.rect(PANTALLA, "white", enemigo_rectangulos["bottom"], 3)
                if "right" in enemigo_rectangulos:
                    pygame.draw.rect(PANTALLA, "white", enemigo_rectangulos["right"], 3)
                if "left" in enemigo_rectangulos:
                    pygame.draw.rect(PANTALLA, "white", enemigo_rectangulos["left"], 3)
                if "top" in enemigo_rectangulos:
                    pygame.draw.rect(PANTALLA, "white", enemigo_rectangulos["top"], 3)
            if enemigo is not None and hasattr(enemigo, 'lista_disparos'):
                for disparo in enemigo.lista_disparos:
                    rectangulo_ajustado = disparo.rectangulo.move(-disparo.rectangulo.width // 8, -disparo.rectangulo.height // 16)
                    pygame.draw.rect(PANTALLA, "yellow", rectangulo_ajustado, 1)
        for disparo in personaje.lista_proyectiles:
            rectangulo_ajustado = disparo.rectangulo.move(disparo.rectangulo.width //2.5, disparo.rectangulo.height //8)
            pygame.draw.rect(PANTALLA, "blue", rectangulo_ajustado, 2)  
        for moneda in monedas:
            rectangulo_moneda = pygame.Rect(moneda.rect.x, moneda.rect.y, moneda.rect.width*2.5, moneda.rect.height*2.5)
            pygame.draw.rect(PANTALLA, "yellow", rectangulo_moneda, 1)
        for item in items:
            rectangulo_item = pygame.Rect(item.rect.x, item.rect.y, item.rect.width, item.rect.height)
            pygame.draw.rect(PANTALLA, "yellow", rectangulo_item, 1)
    
    pygame.display.update()
