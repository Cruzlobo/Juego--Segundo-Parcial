import pygame
import csv
pygame.mixer.init()
COLOR_NEGRO = (0, 0, 0)
def dibujar_texto(texto, fuente, color,x,y,PANTALLA):
        img = fuente.render(texto, True, color)
        PANTALLA.blit(img,(x,y))
def crear_plataforma(path, ancho, alto, x, y, es_visible):
    plataforma = {}
    
    if es_visible:
        plataforma["imagen"] = pygame.image.load(path)
        plataforma["imagen"] = pygame.transform.scale(plataforma["imagen"], (ancho, alto))
    else:
        plataforma["imagen"] = pygame.Surface((ancho, alto))
        
    plataforma["rectangulo"] = plataforma["imagen"].get_rect() 
    plataforma["rectangulo"].x = x
    plataforma["rectangulo"].y = y
    
    return plataforma

def girar_imagenes(lista_original, flip_x, flip_y):
    lista_girada = [pygame.transform.flip(imagen, flip_x, flip_y) for imagen in lista_original]
    return lista_girada

def girar_imagenes2(lista_original, angulo):
    lista_girada = [pygame.transform.rotate(imagen, angulo) for imagen in lista_original]
    return lista_girada

def reescalar_imagenes(diccionario_animaciones, ancho, alto):
    for clave in diccionario_animaciones:
        img = diccionario_animaciones[clave]
        if isinstance(img, pygame.Surface):  
            diccionario_animaciones[clave] = pygame.transform.scale(img, (ancho, alto))
        else: 
            diccionario_animaciones[clave] = [pygame.transform.scale(img, (ancho, alto)) for img in img]

def obtener_rectangulos(x, y, width, height):
    diccionario = {
        "main": pygame.Rect(x, y, width, height),
        "bottom": pygame.Rect(x, y + height - 10, width, 10),
        "right": pygame.Rect(x + width - 10, y , 10, height),
        "left": pygame.Rect(x, y , 10, height),
        "top": pygame.Rect(x, y, width, 10)
    }
    return diccionario

def cargar_puntajes(puntaje):
    try:
        with open(puntaje, mode='r') as file:
            reader = csv.DictReader(file)
            puntajes = [fila for fila in reader]
        return puntajes
    except FileNotFoundError:
        return []

def mostrar_puntajes_final(puntajes, puntaje_actual,PANTALLA,W):
    PANTALLA.fill((0, 0, 0))
    font = pygame.font.Font(None, 36)

    texto_encabezado = font.render("Puntajes Finales", True, (255, 255, 255))
    texto_rect_encabezado = texto_encabezado.get_rect(center=(W // 2, 300))
    PANTALLA.blit(texto_encabezado, texto_rect_encabezado)

    puntajes.append({"Jugador": "", "Puntuacion": puntaje_actual})


    puntajes = sorted(puntajes, key=lambda x: int(x["Puntuacion"]), reverse=True)


    y = 350
    for index, puntaje in enumerate(puntajes):
        texto_puntaje = font.render(f"{index + 1}. {puntaje['Jugador']}: {puntaje['Puntuacion']}", True, (255, 255, 255))
        text_rect_puntaje = texto_puntaje.get_rect(center=(W // 2, y))
        PANTALLA.blit(texto_puntaje, text_rect_puntaje)
        y += 40

    pygame.display.flip()

####################################################################

personaje_quieto = [pygame.image.load(r"Sprites\PLAYER1\QUIETO\0.png")]
personaje_quieto_izquierda = girar_imagenes(personaje_quieto, True, False)

personaje_corre = [pygame.image.load(r"Sprites\PLAYER1\CORRER\13.png"),
                    pygame.image.load(r"Sprites\PLAYER1\CORRER\14.png"),
                    pygame.image.load(r"Sprites\PLAYER1\CORRER\15.png"),
                    pygame.image.load(r"Sprites\PLAYER1\CORRER\16.png")]

personaje_corre_izquierda = girar_imagenes(personaje_corre, True, False)

personaje_salta = [pygame.image.load(r"Sprites\PLAYER1\SALTO\80.png"),
                    pygame.image.load(r"Sprites\PLAYER1\SALTO\81.png"),
                    pygame.image.load(r"Sprites\PLAYER1\SALTO\83.png"),
                    pygame.image.load(r"Sprites\PLAYER1\SALTO\84.png"),
                    pygame.image.load(r"Sprites\PLAYER1\SALTO\85.png"),
                    pygame.image.load(r"Sprites\PLAYER1\SALTO\86.png"),
                    pygame.image.load(r"Sprites\PLAYER1\SALTO\87.png")]

personaje_salta_izquierda = girar_imagenes(personaje_salta,True, False)

personaje_empujon = [pygame.image.load(r"Sprites\PLAYER1\EMPUJON\42.png")]

personaje_empujon_derecha = girar_imagenes(personaje_empujon,True, False)

personaje_arrastra = [pygame.image.load(r"Sprites\PLAYER1\ARRASTARSE\158.png")]

personaje_dispara = [pygame.image.load(r"Sprites/PLAYER1/APUNTAR/33.png")]

personaje_dispara_izquierda= girar_imagenes(personaje_dispara, True, False)
##########################ENEMIGOS#####################################
enemigo_camina = [pygame.image.load(r"Sprites\ENEMIGO1\0.png"),
                    pygame.image.load(r"Sprites\ENEMIGO1\1.png"),
                    pygame.image.load(r"Sprites\ENEMIGO1\2.png"),
                    pygame.image.load(r"Sprites\ENEMIGO1\3.png"),
                    pygame.image.load(r"Sprites\ENEMIGO1\4.png")]

enemigo_camina_derecha = girar_imagenes(enemigo_camina, True, False)

enemigo_aplasta =   [pygame.image.load(r"Sprites\ENEMIGO1\21.png"),
                    pygame.image.load(r"Sprites\ENEMIGO1\22.png"),
                    pygame.image.load(r"Sprites\ENEMIGO1\23.png"),
                    pygame.image.load(r"Sprites\ENEMIGO1\24.png"),
                    pygame.image.load(r"Sprites\ENEMIGO1\25.png"),
                    pygame.image.load(r"Sprites\ENEMIGO1\26.png"),
                    pygame.image.load(r"Sprites\ENEMIGO1\27.png"),
                    pygame.image.load(r"Sprites\ENEMIGO1\28.png"),
                    pygame.image.load(r"Sprites\ENEMIGO1\29.png"),
                    pygame.image.load(r"Sprites\ENEMIGO1\30.png"),
                    pygame.image.load(r"Sprites\ENEMIGO1\31.png"),
                    pygame.image.load(r"Sprites\ENEMIGO1\32.png"),
                    pygame.image.load(r"Sprites\ENEMIGO1\33.png"),
                    pygame.image.load(r"Sprites\ENEMIGO1\34.png"),
                    pygame.image.load(r"Sprites\ENEMIGO1\35.png"),
                    pygame.image.load(r"Sprites\ENEMIGO1\36.png"),
                    pygame.image.load(r"Sprites\ENEMIGO1\37.png"),
                    pygame.image.load(r"Sprites\ENEMIGO1\38.png"),
                    pygame.image.load(r"Sprites\ENEMIGO1\39.png"),
                    pygame.image.load(r"Sprites\ENEMIGO1\40.png"),
                    pygame.image.load(r"Sprites\ENEMIGO1\41.png")]

enemigo2_camina = [pygame.image.load(r"Sprites\ENEMIGO2\0.png"),
                    pygame.image.load(r"Sprites\ENEMIGO2\1.png"),
                    pygame.image.load(r"Sprites\ENEMIGO2\2.png"),
                    pygame.image.load(r"Sprites\ENEMIGO2\3.png"),
                    pygame.image.load(r"Sprites\ENEMIGO2\4.png")]

enemigo2_camina_derecha = girar_imagenes(enemigo2_camina, True, False)

enemigo2_dispara =   [pygame.image.load(r"Sprites\ENEMIGO2\37.png"),
                    pygame.image.load(r"Sprites\ENEMIGO2\38.png"),
                    pygame.image.load(r"Sprites\ENEMIGO2\39.png"),
                    pygame.image.load(r"Sprites\ENEMIGO2\40.png")]

enemigo2_aplasta =   [pygame.image.load(r"Sprites\ENEMIGO2\53.png"),
                    pygame.image.load(r"Sprites\ENEMIGO2\54.png"),
                    pygame.image.load(r"Sprites\ENEMIGO2\55.png"),
                    pygame.image.load(r"Sprites\ENEMIGO2\56.png"),
                    pygame.image.load(r"Sprites\ENEMIGO2\57.png"),
                    pygame.image.load(r"Sprites\ENEMIGO2\58.png"),
                    pygame.image.load(r"Sprites\ENEMIGO2\59.png"),
                    pygame.image.load(r"Sprites\ENEMIGO2\60.png"),
                    pygame.image.load(r"Sprites\ENEMIGO2\61.png"),
                    pygame.image.load(r"Sprites\ENEMIGO2\62.png"),
                    pygame.image.load(r"Sprites\ENEMIGO2\63.png"),
                    pygame.image.load(r"Sprites\ENEMIGO2\64.png"),
                    pygame.image.load(r"Sprites\ENEMIGO2\65.png"),
                    pygame.image.load(r"Sprites\ENEMIGO2\66.png"),
                    pygame.image.load(r"Sprites\ENEMIGO2\67.png"),
                    pygame.image.load(r"Sprites\ENEMIGO2\68.png"),
                    pygame.image.load(r"Sprites\ENEMIGO2\69.png"),
                    pygame.image.load(r"Sprites\ENEMIGO2\70.png"),
                    pygame.image.load(r"Sprites\ENEMIGO2\71.png"),
                    pygame.image.load(r"Sprites\ENEMIGO2\72.png"),
                    pygame.image.load(r"Sprites\ENEMIGO2\73.png"),
                    pygame.image.load(r"Sprites\ENEMIGO2\74.png"),
                    pygame.image.load(r"Sprites\ENEMIGO2\75.png"),
                    pygame.image.load(r"Sprites\ENEMIGO2\76.png"),
                    pygame.image.load(r"Sprites\ENEMIGO2\77.png"),
                    pygame.image.load(r"Sprites\ENEMIGO2\78.png"),
                    pygame.image.load(r"Sprites\ENEMIGO2\79.png")]

boss = [pygame.image.load(r"Sprites\BOSS\1.png"),
                    pygame.image.load(r"Sprites\BOSS\2.png"),
                    pygame.image.load(r"Sprites\BOSS\3.png"),
                    pygame.image.load(r"Sprites\BOSS\4.png"),
                    ]
boss= girar_imagenes2(boss,90)
boss= girar_imagenes(boss,False, True)

disparo_boss = [
            pygame.image.load(r"Sprites\BOSS\563.png"),
            pygame.image.load(r"Sprites\BOSS\562.png"),
        ]
disparo_boss= girar_imagenes(disparo_boss,True,False)



##################SONIDOS##########################
arma_sonido = pygame.mixer.Sound(r"Sonidos\Arma\st3_0C.wav")
moneda_sonido = pygame.mixer.Sound(r"Sonidos\Monedas\S1_C3.wav")
botella_sonido = pygame.mixer.Sound(r"Sonidos\agua\VFX_Tap.wav")
golpe_sonido = pygame.mixer.Sound(r"Sonidos\Golpe\bn021b.wav")
golpe_alien_sonido = pygame.mixer.Sound(r"Sonidos\Alien\OUCH2.wav")
muerte_alien_sonido = pygame.mixer.Sound(r"Sonidos\Alien\OUCH2.wav")
