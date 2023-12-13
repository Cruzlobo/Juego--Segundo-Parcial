import pygame, sys
import subprocess

pygame.init()
NEGRO= (0,0,0)
W=1200
H= 720

PANTALLA = pygame.display.set_mode((W,H))
pygame.display.set_caption("Invasion alienigena en el Desierto Egipcio")
fondo = pygame.image.load(r"Sprites\niveles\fondo_menu.png").convert()
fondo = pygame.transform.scale(fondo, (W,H))
juego_empezado = False
imagen_menu = pygame.image.load(r"Sprites\niveles\menu.png").convert()
imagen_menu = pygame.transform.scale(imagen_menu, (500,500))
boton_1 = pygame.image.load(r"Sprites\niveles\boton_1.png").convert()
boton_1= pygame.transform.scale(boton_1,(100,100))
boton_2 = pygame.image.load(r"Sprites\niveles\boton_2.png").convert()
boton_2= pygame.transform.scale(boton_2,(100,100))
boton_3 = pygame.image.load(r"Sprites\niveles\boton_3.png").convert()
boton_3= pygame.transform.scale(boton_3,(100,100))
boton_config = pygame.image.load(r"Sprites\niveles\boton_config.png").convert()
boton_config= pygame.transform.scale(boton_config,(100,100))
opciones= pygame.image.load(r"Sprites\niveles\0.png")
opciones = pygame.transform.scale(opciones,(800,800))
advertencia= pygame.image.load(r"Sprites\niveles\2.png")
advertencia= pygame.transform.scale(advertencia,(700,200))
mostrar_opciones = False
#FUENTES
fuente = pygame.font.Font( "fonts\monogram.ttf", 60)
fuente2 = pygame.font.Font( "fonts\monogram.ttf", 30)
fuente3 = pygame.font.Font( "fonts\monogram.ttf", 100)

VOLUMEN_MENU = 1
pygame.mixer.music.set_volume(VOLUMEN_MENU)
volumen_menu_actual = VOLUMEN_MENU 
def reproducir_musica_menu():
    pygame.mixer.music.load(r"Sonidos\Menu\menu.mp3")
    pygame.mixer.music.set_volume(VOLUMEN_MENU)
    pygame.mixer.music.play(-1)
reproducir_musica_menu()
reproducir_musica = True
color_fuente = (255,255,255)
def dibujar_texto(texto, fuente, color,x,y):
        img = fuente.render(texto, True, color)
        PANTALLA.blit(img,(x,y))
nivel_1_superado = False
nivel_2_superado = False
advertencia_nivel1 = False
advertencia_nivel2 = False
flag = True
while flag:
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                            juego_empezado = True
            if event.type == pygame.QUIT:
                        flag= False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if juego_empezado:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if 420 <= mouse_x <= 520 and 175 <= mouse_y <= 275:
                        pygame.mixer.music.stop()
                        subprocess.run(["python", "nivel_1.py"])
                        reproducir_musica_menu() 
                        nivel_1_superado = True
                    elif 420 <= mouse_x <= 520 and 280 <= mouse_y <= 380:
                        if nivel_1_superado:
                            pygame.mixer.music.stop()
                            subprocess.run(["python", "nivel_2.py"])
                            reproducir_musica_menu()
                            nivel_2_superado = True
                        else: 
                            advertencia_nivel1 = True
                    elif 420 <= mouse_x <= 520 and 380 <= mouse_y <= 480: 
                        if nivel_2_superado:
                            pygame.mixer.music.stop()
                            subprocess.run(["python", "nivel_3.py"])
                        else:
                            advertencia_nivel2 = True
                    elif 420 <= mouse_x <= 520 and 485 <= mouse_y <= 585:
                        mostrar_opciones = not mostrar_opciones
                        reproducir_musica_menu() 
                        print("Haz clic en el botón opcion")
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    if reproducir_musica:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                    reproducir_musica = not reproducir_musica
                elif event.key == pygame.K_y:
                    if mostrar_opciones:
                        mostrar_opciones = False
                    advertencia_nivel1 = False
                    advertencia_nivel2 = False
        PANTALLA.blit(fondo,(0,0))
        dibujar_texto("Invasion alienigena en el Desierto Egipcio",fuente2,color_fuente, 600, 650)
        dibujar_texto("Por: Cruz Lobo",fuente2,color_fuente, 730, 680)
        if juego_empezado:
                PANTALLA.blit(imagen_menu,(400,100))
                PANTALLA.blit(boton_1,(420,175))
                dibujar_texto("FACIL",fuente3,color_fuente, 550,180)
                PANTALLA.blit(boton_2,(420,280))
                dibujar_texto("MEDIO",fuente3,color_fuente, 550,280)
                PANTALLA.blit(boton_3,(420,380))
                dibujar_texto("DIFICIL",fuente3,color_fuente, 550,380)
                PANTALLA.blit(boton_config,(420,485))
                dibujar_texto("OPCIONES",fuente3,color_fuente, 550,485)
                if mostrar_opciones:
                    PANTALLA.blit(opciones, (200, 0))
                    dibujar_texto("CONTROLES:", fuente, color_fuente, 240, 235)
                    dibujar_texto("A - MOVERSE IZQUIERDA", fuente, color_fuente, 240, 280)
                    dibujar_texto("D - MOVERSE DERECHA", fuente, color_fuente, 240, 315)
                    dibujar_texto("W - SALTAR", fuente, color_fuente, 240, 350)
                    dibujar_texto("S - AGACHARSE", fuente, color_fuente, 240, 390)
                    dibujar_texto("ESPACIO - DISPARAR", fuente, color_fuente, 240, 440)
                    dibujar_texto("P - PAUSA", fuente, color_fuente, 240, 490)
                    dibujar_texto("M - MUTEAR MUSICA MENU", fuente, color_fuente, 240, 530)
                    dibujar_texto("Y - REGRESAR", fuente, (255,0,0), 700, 600)
                if advertencia_nivel1:
                    PANTALLA.blit(fondo,(0,0))
                    PANTALLA.blit(advertencia, (300, 250))
                    mensaje=("COMPLETA EL NIVEL 1 PRIMERO")
                    dibujar_texto(mensaje, fuente, (255, 0, 0), 330, 300) 
                    dibujar_texto("Y - REGRESAR", fuente, (255,0,0), 500, 370)
                if advertencia_nivel2:
                    PANTALLA.blit(fondo,(0,0))
                    PANTALLA.blit(advertencia, (300, 250))
                    mensaje=("COMPLETA EL NIVEL 2 PRIMERO")
                    dibujar_texto(mensaje, fuente, (255, 0, 0), 330, 300) 
                    dibujar_texto("Y - REGRESAR", fuente, (255,0,0), 500, 370)
                    
        else:
            dibujar_texto("Presiona ESPACIO para empezar",fuente,color_fuente, 300, 300)
            

        
        pygame.display.update()

pygame.quit()