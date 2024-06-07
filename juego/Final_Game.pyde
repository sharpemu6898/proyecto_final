movimiento = 300
movimientoEnemigos = 0
movimientoEnemigosX = 0
veloci = 2
proyectil = [[-1, -1] for _ in range(10)] 
ultimo_tiro = 0
cooldown = 1000
aliens = [[[-1, -1] for _ in range(5)] for _ in range(8)]  
Lifes = 3
Score = 0
estado = "menu"
dificultad = "EASY"
doble_disparo = False
jefe = False
boss_hp = 400
boss_pos = 250
boss_vel = 4
boss_img = None 

tiempo_doble_disparo = 0
proyectiles_enemigos = [[-1, -1] for _ in range(20)]  
frecuencia_disparo_enemigo = 0.001
estrellas = []

ultimo_tiro_hilera = 0
cooldown_hilera = 2000
hilera_y = -60  
bossProyectil_activa = False
hilera_x = 0  

def setup():
    global img, mi_fuente, nave_img, boss_img
    size(680, 480)
    img = loadImage("alien22.png")
    mi_fuente = createFont("Starjedi.ttf", 32)
    nave_img = loadImage("NaveFinal.png")
    boss_img = loadImage("FBOSS.png")
    if boss_img is None:
        println("Error: No se pudo cargar la imagen del jefe")
    textFont(mi_fuente)
    background(0)
    textSize(20)
    generar_estrellas()
    println("Imágenes cargadas correctamente")

def draw():
    global estado
    background(0)
    if estado == "menu":
        mostrar_menu()
    elif estado == "juego":
        jugar()
    elif estado == "seleccionar_dificultad":
        mostrar_dificultades()
    elif estado == "game_over":
        mostrar_game_over()
    elif estado == "nivel_superado":
        mostrar_nivel_superado()

    if estado == "nivel_superado" and keyPressed:
        estado = "menu"

def dibujar_estrellas():
    fill(255)
    for estrella in estrellas:
        ellipse(estrella[0], estrella[1], 2, 2)

def dibujar_fuego():
    for _ in range(10):
        for _ in range(5):
            fill(255, random(100, 255), 0, 150)
            noStroke()
            ellipse(random(width), random(height), random(10, 60), random(10, 60))
            delay(50)

def dibujar_fireworks():
    for _ in range(20):
        x = random(width)
        y = random(height)
        for _ in range(10):
            fill(random(255), random(255), random(255))
            noStroke()
            ellipse(x + random(-50, 50), y + random(-50, 50), 10, 10)
            delay(40)  

def dibujar_estrella(x, y, size):
    fill(255, 255, 0)  
    beginShape()
    for i in range(5):
        angle = TWO_PI * i / 5 - HALF_PI
        x_i = x + cos(angle) * size
        y_i = y + sin(angle) * size
        vertex(x_i, y_i)
        angle += TWO_PI / 10
        x_i = x + cos(angle) * (size / 2)
        y_i = y + sin(angle) * (size / 2)
        vertex(x_i, y_i)
    endShape(CLOSE)

def generar_estrellas():
    global estrellas
    estrellas = [[random(width), random(height)] for _ in range(100)]

def mostrar_menu():
    textAlign(CENTER)
    fill(255, 255, 0)  
    textSize(50)
    text("STAR", width / 2 - 100, height / 2 - 100)  
    text("SIEGE", width / 2 + 150, height / 2 - 100)  
    textSize(30)
    text("Press 'S' to Start", width / 2, height / 2)
    dibujar_estrellas()  
    dibujar_estrella(width / 2, height / 2 - 100, 20)  

def mostrar_dificultades():
    textAlign(CENTER)
    fill(255)
    textSize(30)
    text("SELECT DiFFiCULTY", width / 2, height / 2 - 100)
    text("1: EASY", width / 2, height / 2)
    text("2: MEDiUM", width / 2, height / 2 + 40)
    text("3: TRYHARD", width / 2, height / 2 + 80)
    text("4: ????", width / 2, height / 2 + 120)
    dibujar_estrellas()

def mostrar_game_over():
    dibujar_fuego()
    textAlign(CENTER)
    fill(200, 150, 255)
    textSize(50)
    text("GAME oVER", width / 2, height / 2)
    textSize(30)
    text("Press 'R' to Restart", width / 2, height / 2 + 60)
    dibujar_estrellas()

def mostrar_nivel_superado():
    dibujar_fireworks()
    textAlign(CENTER)
    fill(0, 255, 0)
    textSize(50)
    text("LEVEL CoMPLETE", width / 2, height / 2)
    textSize(30)
    text("Congratulations!", width / 2, height / 2 + 60)
    text("You defeated all enemies!", width / 2, height / 2 + 100)
    text("Press 'M' to return to Main Menu", width / 2, height / 2 + 140)
    dibujar_estrellas()

def keyPressed():
    global estado
    if estado == "menu" and (key == 's' or key == 'S'):
        estado = "seleccionar_dificultad"
    
    if estado == "seleccionar_dificultad":
        if key == '1':
            configurar_dificultad("EASY")
        elif key == '2':
            configurar_dificultad("MEDIUM")
        elif key == '3':
            configurar_dificultad("TRYHARD")
        elif key == '4':
            configurar_dificultad("????")
    
    if estado == "game_over" and key == 'r':
        reiniciar_juego()
        
    if estado == "nivel_superado" and key == 'm':

        reiniciar_juego()

def configurar_dificultad(nueva_dificultad):
    global dificultad, estado, cooldown, veloci, Lifes, frecuencia_disparo_enemigo, Score, aliens, jefe
    dificultad = nueva_dificultad
    estado = "juego"
    Score = 0  
    if dificultad == "EASY":
        cooldown = 1500
        veloci = 1
        Lifes = 5
        frecuencia_disparo_enemigo = 0.0005
        generar_aliens()
    elif dificultad == "MEDIUM":
        cooldown = 1000
        veloci = 2
        Lifes = 3
        frecuencia_disparo_enemigo = 0.001
        generar_aliens()
    elif dificultad == "TRYHARD":
        cooldown = 500
        veloci = 4
        Lifes = 1
        frecuencia_disparo_enemigo = 0.002
        generar_aliens()
    elif dificultad == "????":
        cooldown = 1000
        veloci = 2
        Lifes = 3
        frecuencia_disparo_enemigo = 0.001
        aliens = [[[-1, -1] for _ in range(5)] for _ in range(8)]  
        jefe = True


def reiniciar_juego():
    global movimiento, movimientoEnemigos, movimientoEnemigosX, veloci, proyectil, ultimo_tiro, cooldown, aliens, Lifes, Score, doble_disparo, tiempo_doble_disparo, proyectiles_enemigos, frecuencia_disparo_enemigo, estado, jefe, boss_hp, boss_pos, boss_vel, ultimo_tiro_hilera, hilera_y, bossProyectil_activa, hilera_x
    movimiento = 300
    movimientoEnemigos = 0
    movimientoEnemigosX = 0
    veloci = 2
    proyectil = [[-1, -1] for _ in range(10)]
    ultimo_tiro = 0
    cooldown = 1000
    Lifes = 3
    Score = 0
    doble_disparo = False
    tiempo_doble_disparo = 3000
    proyectiles_enemigos = [[-1, -1] for _ in range(20)]
    frecuencia_disparo_enemigo = 0.001
    estado = "menu"
    dificultad = "EASY"  
    jefe = False
    boss_hp = 400
    boss_pos = 250
    boss_vel = 10
    ultimo_tiro_hilera = 0
    hilera_y = -60
    bossProyectil_activa = False
    hilera_x = 0
    generar_aliens()

def jugar():
    global movimiento, movimientoEnemigos, movimientoEnemigosX, veloci, Lifes, Score, doble_disparo, tiempo_doble_disparo, estado, jefe, hilera_y, ultimo_tiro_hilera, bossProyectil_activa, hilera_x
    background(0)
    dibujar_estrellas()
    textSize(20)
    text("Lifes:" + str(Lifes), 10, 475)
    text("Score:" + str(Score), 580, 475)
    image(nave_img, movimiento, 420, 80, 20)  # Dibujar la nave usando la imagen
    controles()
    if dificultad != "????":
        show_aliens()
        movimientoEnemigos += 0.01
        movimientoEnemigosX += veloci
        disparar_enemigos()
        actualizar_disparo_enemigos()
    else:
        mostrar_boss()  # Dibujar el jefe
        boss_life()
        actualizar_boss()
        if millis() - ultimo_tiro_hilera >= cooldown_hilera and boss_pos <= movimiento + 70 and boss_pos + 180 >= movimiento:
            hilera_y = 50
            hilera_x = boss_pos + 90
            bossProyectil_activa  = True
            ultimo_tiro_hilera = millis()
        if bossProyectil_activa:
            drawColumn(hilera_x, hilera_y, 10, 10, 20)
            hilera_y += 10
            if hilera_y > height:
                bossProyectil_activa = False
            if colision_con_jugador(hilera_x, hilera_y):
                Lifes -= 1
                bossProyectil_activa = False
                if Lifes <= 0:
                    estado = "game_over"

    actualizar_disparo()
    dibujar_barra_recarga()

    if movimientoEnemigosX > 100 or movimientoEnemigosX < -100:
        veloci *= -1

    if Score >= 400 and dificultad != "????":
        estado = "nivel_superado"

    if Score >= 100 and not doble_disparo:
        doble_disparo = True
        tiempo_doble_disparo = millis()

    if doble_disparo and millis() - tiempo_doble_disparo >= 10000:
        doble_disparo = False


def dibujar_barra_recarga():
    global ultimo_tiro, cooldown
    fill(255)
    rect(10, 10, 100, 10)  
    tiempo_restante = millis() - ultimo_tiro
    ancho_barra = constrain(map(tiempo_restante, 0, cooldown, 0, 100), 0, 100)
    fill(0, 255, 0)
    rect(10, 10, ancho_barra, 10) 

def controles():
    global movimiento, ultimo_tiro, doble_disparo
    if keyPressed:
        if (key == 'a') and movimiento > 10:
            movimiento -= 10
        elif (key == 'd') and movimiento < 610:
            movimiento += 10
        elif key == ' ' and millis() - ultimo_tiro >= cooldown:
            shoot_proyectile()
            ultimo_tiro = millis()
            if doble_disparo: 
                shoot_proyectile()

def generar_aliens():
    global aliens
    spaces = 10
    for i in range(8):
        for j in range(5):
            x = 110 + i * (50 + spaces)
            y = 11 + j * (20 + spaces)
            aliens[i][j] = [x, y]

def show_aliens():
    fill(0, 0, 124)
    for i in range(8):
        for j in range(5):
            if aliens[i][j][0] != -1:
                image(img, aliens[i][j][0] + movimientoEnemigosX, aliens[i][j][1] + movimientoEnemigos, 70, 40)

def mostrar_boss():
    global boss_img, boss_pos, boss_vel
    boss_width = 180
    boss_height = 90
    boss_x = boss_pos - boss_width / 2  
    boss_y = 40
    if boss_img is not None:
        image(boss_img, boss_x, boss_y, boss_width, boss_height)
    boss_pos += boss_vel
    if boss_pos > width - 180 or boss_pos < 0:
        boss_vel *= -1

def actualizar_boss():
    global boss_pos, boss_vel, boss_hp, estado
    boss_pos += boss_vel
    if boss_pos > width - 180 or boss_pos < 0:
        boss_vel *= -1

    for i in range(len(proyectil)):
        if proyectil[i][0] != -1:
            if proyectil[i][0] > boss_pos and proyectil[i][0] < boss_pos + 180 and proyectil[i][1] > 40 and proyectil[i][1] < 130:
                boss_hp -= 20
                proyectil[i] = [-1, -1]
                if boss_hp <= 0:
                    estado = "nivel_superado"
                    reiniciar_juego()

def boss_life():
    global boss_hp
    fill(250, 255, 5)
    rect(170, 10, boss_hp, 10)

def shoot_proyectile():
    global proyectil, doble_disparo
    for i in range(len(proyectil)):
        if proyectil[i][0] == -1:
            proyectil[i] = [movimiento + 35, 420]
            break
    if doble_disparo:
        for i in range(len(proyectil)):
            if proyectil[i][0] == -1:
                proyectil[i] = [movimiento + 55, 420] 
                break

def actualizar_disparo():
    global proyectil, aliens, Score
    fill(255, 255, 0)
    for i in range(len(proyectil)):
        if proyectil[i][0] != -1:
            proyectil[i][1] -= 10
            if proyectil[i][1] > 0:
                rect(proyectil[i][0], proyectil[i][1], 5, 15)
                for ai in range(8):
                    for aj in range(5):
                        if aliens[ai][aj][0] != -1:
                            if proyectil[i][0] > aliens[ai][aj][0] + movimientoEnemigosX and proyectil[i][0] < aliens[ai][aj][0] + movimientoEnemigosX + 50 and proyectil[i][1] > aliens[ai][aj][1] + movimientoEnemigos and proyectil[i][1] < aliens[ai][aj][1] + movimientoEnemigos + 20:
                                aliens[ai][aj] = [-1, -1]
                                proyectil[i] = [-1, -1]
                                Score += 10
                                break

def disparar_enemigos():
    global proyectiles_enemigos, aliens, frecuencia_disparo_enemigo
    for ai in range(8):
        for aj in range(5):
            if aliens[ai][aj][0] != -1:
                if random(1) < frecuencia_disparo_enemigo:
                    for i in range(len(proyectiles_enemigos)):
                        if proyectiles_enemigos[i][0] == -1:
                            proyectiles_enemigos[i] = [aliens[ai][aj][0] + movimientoEnemigosX, aliens[ai][aj][1] + movimientoEnemigos]
                            break

def actualizar_disparo_enemigos():
    global proyectiles_enemigos, Lifes, estado
    fill(255, 0, 0)
    for i in range(len(proyectiles_enemigos)):
        if proyectiles_enemigos[i][0] != -1:
            proyectiles_enemigos[i][1] += 5
            if proyectiles_enemigos[i][1] < 480:
                rect(proyectiles_enemigos[i][0], proyectiles_enemigos[i][1], 5, 15)
                if proyectiles_enemigos[i][0] > movimiento - 35 and proyectiles_enemigos[i][0] < movimiento + 35 and proyectiles_enemigos[i][1] > 400 and proyectiles_enemigos[i][1] < 440:
                    if Lifes > 0:
                        Lifes -= 1
                        proyectiles_enemigos[i] = [-1, -1]  
                    break
            else:
                proyectiles_enemigos[i] = [-1, -1]
    
    if Lifes <= 0:
        estado = "game_over"

def drawColumn(x, y, w, h, n):
    drawRectangle(x, y, w, h)
    if n > 1:
        drawColumn(x, y + h, w, h, n - 1)

def drawRectangle(x, y, w, h):
    rect(x, y, w, h)

def colision_con_jugador(px, py):
    global movimiento
    jugador_x = movimiento
    jugador_y = 420
    jugador_ancho = 70
    jugador_alto = 22
    return jugador_x <= px <= jugador_x + jugador_ancho and jugador_y <= py <= jugador_y + jugador_alto

def mousePressed():
    if estado == "game_over":
        reiniciar_juego()
