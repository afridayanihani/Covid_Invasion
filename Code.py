# Import Library 
import math
import pygame
from pygame.locals import *
from random import randint

# Initialize the Game 
pygame.init()
width, height = 800,600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Covid Invassion')

# Key mapping
keys = {
    "top": False, 
    "bottom": False,
    "left": False,
    "right": False 
}

running = True
doctorpos = [120, 500] 

# exit code for game over and win codition
exitcode = 0
EXIT_CODE_GAME_OVER = 0
EXIT_CODE_WIN = 1

score = 0
lives_point = 194
countdown_timer = 90000
syringes = []

virus_timer = 100
viruses = [[width, 1000]]

# Load Game Assets 
# Load Images
doctor = pygame.image.load("assets/pict/doctor.png")
background = pygame.image.load("assets/pict/bg.jpg")
hospital = pygame.image.load("assets/pict/hospital.png")
syringe = pygame.image.load("assets/pict/syringe.png")
virus_img = pygame.image.load("assets/pict/virus.png")
livesbar = pygame.image.load("assets/pict/livesbar.png")
lives = pygame.image.load("assets/pict/lives.png")
gameover = pygame.image.load("assets/pict/gameover.png")
youwin = pygame.image.load("assets/pict/youwin.png")

# Load audio
pygame.mixer.init()
hit_sound = pygame.mixer.Sound("assets/sound/explode.wav")
virus_hit_sound = pygame.mixer.Sound("assets/sound/explosion.wav")
shoot_sound = pygame.mixer.Sound("assets/sound/fire.wav")
gameover_sound = pygame.mixer.Sound ("assets/sound/gameover.wav")
youwin_sound = pygame.mixer.Sound("assets/sound/win.wav")
hit_sound.set_volume(0.10)
virus_hit_sound.set_volume(0.10)
shoot_sound.set_volume(0.10)
gameover_sound.set_volume (0.40)
youwin_sound.set_volume (0.40)


# background music
pygame.mixer.music.load("assets/sound/17Agustus.wav")
pygame.mixer.music.play(+500, 0.0)
pygame.mixer.music.set_volume(0.50)

# The Game Loop 
while(running):
    
    # Clear the screen 
    screen.fill(0)
    
    # Draw the game object 
    # draw the background
    for x in range(int(width/background.get_width()+1)):
      for y in range(int(height/background.get_height()+1)):
            screen.blit(background, (x, y))
    
    # draw the hospital
    screen.blit(hospital, (10 , 80))
    screen.blit(hospital, (10 , 220))
    screen.blit(hospital, (10 , 360))
    screen.blit(hospital, (10 , 500))

    # draw the doctor
    mouse_position = pygame.mouse.get_pos()
    angle = math.atan2(mouse_position[1] - (doctorpos[1]+32), mouse_position[0] - (doctorpos[0]+26))
    doctor_rotation = pygame.transform.rotate(doctor, 360 - angle * 57.29)
    new_doctorpos = (doctorpos[0] - doctor_rotation.get_rect().width / 2, doctorpos[1] - doctor_rotation.get_rect().height / 2)
    screen.blit(doctor_rotation, new_doctorpos)

    # Draw syringe
    for bullet in syringes:
        syringe_index = 0
        velx=math.cos(bullet[0])*10
        vely=math.sin(bullet[0])*10
        bullet[1]+=velx
        bullet[2]+=vely
        if bullet[1] < -64 or bullet[1] > width or bullet[2] < -64 or bullet[2] > height:
            syringes.pop(syringe_index)
        syringe_index += 1
        # draw the syringe
        for projectile in syringes:
            new_syringe = pygame.transform.rotate(syringe, 360-projectile[0]*57.29)
            screen.blit(new_syringe, (projectile[1], projectile[2]))

    # Draw Enemy
    
    virus_timer -= 1
    if virus_timer == 0:
        viruses.append([width, randint(50, height-32)])
        virus_timer = randint(1, 100)

    index = 0
    for virus in viruses:
        virus[0] -= 5
        if virus[0] < -64:
            viruses.pop(index)

        # collision between virus and hospital 
        virus_rect = pygame.Rect(virus_img.get_rect())
        virus_rect.top = virus[1] 
        virus_rect.left = virus[0] 
    
        if virus_rect.left < 64:
            viruses.pop(index)
            lives_point -= randint(5,20)
            hit_sound.play()
            print("We are under attack!")
        
        # Check for collisions between virus and syringes
        index_syringe = 0
        for bullet in syringes:
            bullet_rect = pygame.Rect(syringe.get_rect())
            bullet_rect.left = bullet[1]
            bullet_rect.top = bullet[2]
           
            if virus_rect.colliderect(bullet_rect):
                score += 1
                viruses.pop(index)
                syringes.pop(index_syringe)
                virus_hit_sound.play()
                print("Virus killed")
                print("Score: {}".format(score))
            index_syringe += 1
        index += 1

    # draw virus to the screen
    for virus in viruses:
        screen.blit(virus_img, virus)

    # Draw Lives bar
    screen.blit(livesbar, (5,5))
    for hp in range(lives_point):
        screen.blit(lives, (hp+8, 8))

    # Draw clock
    font = pygame.font.Font(None, 28)
    minutes = int((countdown_timer-pygame.time.get_ticks())/60000) 
    seconds = int((countdown_timer-pygame.time.get_ticks())/1000%60)
    time_text = "{:02}:{:02}".format(minutes, seconds)
    clock = font.render(time_text, True, (254, 3, 3))
    textRect = clock.get_rect()
    textRect.topright = [790, 5]
    screen.blit(clock, textRect)

    # Update the sceeen
    pygame.display.flip()

    # Event Loop
    for event in pygame.event.get():
        # event saat tombol exit diklik
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

        # Fire!!
        if event.type == pygame.MOUSEBUTTONDOWN:
            syringes.append([angle, new_doctorpos[0]+50, new_doctorpos[1]+50])
            shoot_sound.play()

        # chcek the keydown and keyup
        if event.type == pygame.KEYDOWN:
            if event.key == K_UP:
                keys["top"] = True
            elif event.key == K_LEFT:
                keys["left"] = True
            elif event.key == K_DOWN:
                keys["bottom"] = True
            elif event.key == K_RIGHT:
                keys["right"] = True
        if event.type == pygame.KEYUP:
            if event.key == K_UP:
                keys["top"] = False
            elif event.key == K_LEFT:
                keys["left"] = False
            elif event.key == K_DOWN:
                keys["bottom"] = False
            elif event.key == K_RIGHT:
                keys["right"] = False
    # End of event loop

    # Move the doctor
    if keys["top"]:
        doctorpos[1] -= 5 
    elif keys["bottom"]:
        doctorpos[1] += 5
    if keys["left"]:
        doctorpos[0] -= 5 
    elif keys["right"]:
        doctorpos[0] += 5 


    # Win/Lose check
    if pygame.time.get_ticks() > countdown_timer:
        running = False
        exitcode = EXIT_CODE_WIN
        youwin_sound.play ()
    if lives_point <= 0:
        running = False
        exitcode = EXIT_CODE_GAME_OVER
        gameover_sound.play ()

# End of Game Loop 



# Win/gameover display
if exitcode == EXIT_CODE_GAME_OVER:
    screen.blit(gameover, (100, 0))
else:
    screen.blit(youwin, (100, 0))

# Tampilkan score
text = font.render("Score: {}".format(score), True, (254, 3, 3))
textRect = text.get_rect()
textRect.centerx = screen.get_rect().centerx
textRect.centery = screen.get_rect().centery - 280
screen.blit(text, textRect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()
