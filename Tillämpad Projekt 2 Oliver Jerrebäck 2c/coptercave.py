# File name: coptercave.py
# Author: Oliver Jerrebäck
# Date:2024-02-08
# Description: Ett helikopter spel som går ut på att inte stöta in i kanterna och överleva så länge så möjligt.


import random  # Importera random modulen för slumpmässiga operationer
import pygame  # Importera pygame modulen för spelutveckling

pygame.init()  # Initialisera pygame modulen

# Skärminställningar
height = 600
screen_width = 1000
screen = pygame.display.set_mode([screen_width, height])  # Skapa en skärm med given bredd och höjd
pygame.display.set_caption('Copter_cave!')  # Sätt fönstertitel

# Textinställningar
font = pygame.font.Font('freesansbold.ttf', 20)

# Spelvariabler
fps = 60  # Frames per second
timer = pygame.time.Clock()
new_map = True
map_rects = []
rect_width = 10
total_rects = screen_width // rect_width
spacer = 10
player_x = 100
player_y = 300
star_x = 150    
star_y = 300    
flying_up = False
flying_down = False
y_speed = 10 
map_speed = 2
score = 0
high_score = 0
active = True
stars = []
star_width = 30
min_star_distance = 100

# Ladda bilder
heli = pygame.transform.scale(pygame.image.load('helicopter.png'), (60, 60))
star = pygame.transform.scale(pygame.image.load('star.png'), (0, 0))  

# Funktion för att generera nya hinder
def generate_new():
    global player_y
    rects = []
    top_height = random.randint(0, 300)
    player_y = top_height + 150
    for i in range(total_rects):
        top_height = random.randint(top_height - spacer, top_height + spacer)
        if top_height < 0:
            top_height = 0
        elif top_height > 300:
            top_height = 300
        top_rect = pygame.draw.rect(screen, 'green', [i * rect_width, 0, rect_width, top_height])
        bot_rect = pygame.draw.rect(screen, 'green', [i * rect_width, top_height + 300, rect_width, height])
        rects.append(top_rect)
        rects.append(bot_rect)
    return rects

# Funktion för att rita ut hinder
def draw_map(rects):
    for i in range(len(rects)):
        pygame.draw.rect(screen, 'green', rects[i])
    pygame.draw.rect(screen, 'dark gray', [0, 0, screen_width, height], 12)

# Funktion för att rita ut spelaren
def draw_player():
    player = pygame.draw.circle(screen, 'black', (player_x, player_y), 20)
    screen.blit(heli, (player_x - 40, player_y - 30))
    return player

# Funktion för att generera en ny stjärna
def generate_star():
    while True:
        star_x = random.randint(screen_width, screen_width + min_star_distance)
        star_y = random.randint(300, height - 300)
        star_rect = pygame.Rect(star_x, star_y, star_width, star_width)
        return star_rect

# Funktion för att rita ut stjärnorna
def draw_stars():
    for star_rect in stars:
        pygame.draw.rect(screen, 'yellow', star_rect)
        screen.blit(star, (star_rect.x - 15, star_rect.y - 15))

# Funktion för att flytta stjärnorna
def move_stars():
    global stars
    for i in range(len(stars)):
        stars[i] = stars[i].move(-map_speed, 0)
        if stars[i].right < 0:
            stars.pop(i)
            stars.append(generate_star())

# Funktion för att kontrollera kollision med stjärnorn
def check_star_collision(player_circle, act):
    global stars, score
    for star_rect in stars:
        if player_circle.colliderect(star_rect):
            star_rect.x = -1000
            star_rect.y = -100
            score += 50
            if score > 1000:
                score += 100
    return act

# Funktion för att flytta spelaren
def move_player(y_pos, speed, fly_up, fly_down):
    if fly_up:
        speed = -5
    elif fly_down:
        speed = 5
    else:
        speed = 0
    y_pos += speed
    return y_pos, speed

# Funktion för att flytta hinder
def move_rects(rects):
    global score
    for i in range(len(rects)):
        rects[i] = (rects[i][0] - map_speed, rects[i][1], rect_width, rects[i][3])
        if rects[i][0] + rect_width < 0:
            rects.pop(1)
            rects.pop(0)
            top_height = random.randint(rects[-2][3] - spacer, rects[-2][3] + spacer)
            if top_height < 0:
                top_height = 0
            elif top_height > 300:
                top_height = 300
            rects.append((rects[-2][0] + rect_width, 0, rect_width, top_height))
            rects.append((rects[-2][0] + rect_width, top_height + 300, rect_width, height))
            score += 1
    return rects

# Funktion för att kontrollera kollision med hinder
def check_collision(rects, circle, act):
    for i in range(len(rects)):
        if circle.colliderect(rects[i]):
            act = False
    return act

# Huvudloop för spelet
run = True
while run:
    screen.fill('black')  # Fyll skärmen med svart färg
    timer.tick(fps)  # Uppdatera klockan
    
    # Generera nya hinder vid behov
    if new_map:
        map_rects = generate_new()
        stars = [generate_star() for _ in range(1)] 
        new_map = False

    # Rita ut hinder, stjärnor och spelare
    draw_map(map_rects)
    draw_stars()
    player_circle = draw_player()
    
    # Flytta spelare och hinder om spelet är aktivt
    if active:
        player_y, y_speed = move_player(player_y, y_speed, flying_up, flying_down)
        map_rects = move_rects(map_rects)
        move_stars()

    # Kontrollera kollisioner
    active = check_collision(map_rects, player_circle, active)
    active = check_star_collision(player_circle, active)

    # Hantera knapptryckningar
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_d:  # Upp för tangetbord respektive joystick i den ordningen
                flying_up = True
            elif event.key == pygame.K_s or event.key == pygame.K_a:  # Ner för tangentbord respektive joysticken i den ordningen
                flying_down = True
            if event.key == pygame.K_RETURN or event.key == pygame.K_e:  # knapp/tangent för att Starta om spelet
                if not active:
                    new_map = True
                    active = True
                    y_speed = 0
                    map_speed = 2
                    if score > high_score:
                        high_score = score
                    score = 0
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_d: # ifall kanppen för att åka upp släpps kommer inte helikoptern åka upp mer detta gäller även för joystick
                flying_up = False
            elif event.key == pygame.K_s or event.key == pygame.K_a: # ifall kanppen för att åka ner släpps kommer inte helikopern åka ner mer detta gäller även för joystick
                flying_down = False

    # Justera hastigheten och spacer baserat på poängen även sätter en hastighetsgräns 
    map_speed = 5 + score // 75 
    if score >= 1430:
        map_speed = 19
    spacer = 10 + score // 100

    # Visa poäng och meddelande om spelet är slut
    screen.blit(font.render(f'Score: {score}', True, 'black'), (20, 15))
    screen.blit(font.render(f'High Score: {high_score}', True, 'black'), (20, 565))
    if not active:
        screen.blit(font.render('Tryck ner knappen eller på ENTER för att starta om', True, 'black'), (275, 15))
        screen.blit(font.render('Tryck ner knappen eller på ENTER för att starta om', True, 'black'), (275, 565))
    pygame.display.flip()  # Uppdatera skärmen

pygame.quit()  # Avsluta pygame
