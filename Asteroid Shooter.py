'''
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
#####
Ammaar Siddiqui
Asteroids
Version 1.0
This is a simple asteroid game where the asteroids come from the right side of the screen and the user moves their
spaceship up and down, shooting the asteroids. Every time an asteroid is hit they get 100 points. Every time an asteroid
passes them they lose 100 points. If an asteroid hits them they lose one of their three lives. This version also has
high scores sound effects, and speed bonuses.
'''

# Ammaar Siddiqui
# Advanced Computer Programming
# 2/22/19

import pygame
import sys
import time
import random

def start_game():
    global lives
    lives=3

    global score
    score=0

    global asteroid_limit
    asteroid_limit=5

    pygame.init()

    background=(0, 0, 0)
    bgImg = pygame.image.load("space_background.jpg")#loads all files
    shooterImg = pygame.image.load("spaceship.png")
    asteroidImg= pygame.image.load("Asteroid.png")
    laserImg = pygame.image.load("laser.png")
    laser_noise = pygame.mixer.Sound("pew_pew.wav")
    speed_upImg= pygame.image.load("speed_up.png")
    explosion_noise=pygame.mixer.Sound("explosion.wav")
    big_explosion=pygame.mixer.Sound("big_explosion.wav")
    pygame.mixer.music.load("DarkKnight.mp3")
    asteroid_explosion=pygame.mixer.Sound("export.wav")
    pygame.mixer.music.set_volume(0.5)#sets the background music volume
    pygame.mixer.music.play(-1, 0.0)
    entity_color = (255, 255, 255)
    POINTS1 = 0
    POINTS2 = 0
    WHITE = (255, 255, 255)

    laser_list=[]#list for all flying objects
    asteroid_list=[]
    bonus_list=[]

    global asteroid_speed
    asteroid_speed=5

    global extra_lasers
    extra_lasers=0

    score_display = False


    class Entity(pygame.sprite.Sprite):
        """Inherited by any object in the game."""

        def __init__(self, x, y, width, height):
            pygame.sprite.Sprite.__init__(self)

            self.x = x
            self.y = y
            self.width = width
            self.height = height

            # This makes a rectangle around the entity, used for anything
            # from collision to moving around.
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


    class Spaceship(Entity):
        """
        Player controlled or AI controlled, main interaction with
        the game
        """

        def __init__(self, x, y, width, height):
            super(Spaceship, self).__init__(x, y, width, height)

            self.image = shooterImg


    class Player(Spaceship):
        """The player controlled Spaceship"""

        def __init__(self, x, y, width, height):
            super(Player, self).__init__(x, y, width, height)

            # How many pixels the Player Paddle should move on a given frame.
            self.y_change = 0
            # How many pixels the paddle should move each frame a key is pressed.
            self.y_dist = 6

        def MoveKeyDown(self, key):
            global extra_lasers
            """Responds to a key-down event and moves accordingly"""
            if (key == pygame.K_UP):
                self.y_change += -self.y_dist
            elif (key == pygame.K_DOWN):
                self.y_change += self.y_dist
            elif (key == pygame.K_SPACE):
                laser_noise.play()
                x = Laser(spaceship.rect.x + 110, spaceship.rect.y + 27, 44, 5)
                all_sprites_list.add(x)
                laser_list.append(x)
            elif (key==pygame.K_z):#Pressing Z creates a shotgun blast of lasers
                if extra_lasers > 0:
                    w = Laser(spaceship.rect.x+90, spaceship.rect.y+7, 44, 5)
                    all_sprites_list.add(w)
                    laser_list.append(w)
                    x = Laser(spaceship.rect.x+100, spaceship.rect.y+17, 44, 5)
                    all_sprites_list.add(x)
                    laser_list.append(x)
                    y=Laser(spaceship.rect.x+110, spaceship.rect.y+27, 44, 5)
                    all_sprites_list.add(y)
                    laser_list.append(y)
                    z=Laser(spaceship.rect.x+100, spaceship.rect.y+37, 44, 5)
                    all_sprites_list.add(z)
                    laser_list.append(z)
                    v = Laser(spaceship.rect.x+90, spaceship.rect.y+47, 44, 5)
                    all_sprites_list.add(v)
                    laser_list.append(v)
                    extra_lasers-=1

        def MoveKeyUp(self, key):
            global POINTS1
            global POINTS2
            global score_display
            """Responds to a key-up event and stops movement accordingly"""
            if (key == pygame.K_UP):
                self.y_change += self.y_dist
            elif (key == pygame.K_DOWN):
                self.y_change += -self.y_dist


        def update(self):
            """
            Makes sure the spaceship stays in bounds
            """
            # Moves it relative to its current location.
            self.rect.move_ip(0, self.y_change)

            # If the spaceship moves off the screen, put it back on.
            if self.rect.y < 75:
                self.rect.y = 75
            elif self.rect.y > window_height - self.height-5:
                self.rect.y = window_height - self.height-5

    class Laser(Entity):
        def __init__(self, x, y, width, height):
            super(Laser, self).__init__(x, y, width, height)

            self.image=laserImg

        def update(self):
            self.rect.x+=8#moves right at a speed of 8

    class Asteroid(Entity):
        def __init__(self, x, y, width, height):
            super(Asteroid, self).__init__(x, y, width, height)

            self.image=asteroidImg

        def update(self):
            self.rect.x-=asteroid_speed#moves left at an increasing speed


    class Bonus(Entity):
        def __init__(self, x, y, width, height):
            super(Bonus, self).__init__(x, y, width, height)

            self.image=speed_upImg

        def update(self):
            self.rect.x-=asteroid_speed#moves left at the same speed as the asteroids



    def lasast_collide(asteroids, lasers):#checks if the laser has collided with the asteroid
        global asteroid_speed
        global score
        for asteroid in asteroids:
            for laser in lasers:
                if asteroid.rect.colliderect(laser):
                    asteroid.remove(all_sprites_list)
                    if asteroid in asteroids:
                        asteroids.remove(asteroid)
                    laser.remove(all_sprites_list)
                    if laser in lasers:
                        lasers.remove(laser)
                    asteroid_speed+=.1
                    asteroid_explosion.play()
                    score+=100

    def lasbonus_collide(bonuses, lasers):#checks if the laser has collided with the bonus
        global extra_lasers
        for bonus in bonuses:
            for laser in lasers:
                if bonus.rect.colliderect(laser ):
                    bonus.remove(all_sprites_list)
                    if bonus in bonuses:
                        bonuses.remove(bonus)
                    laser.remove(all_sprites_list)
                    if laser in lasers:
                        lasers.remove(laser)
                    extra_lasers+=3


    def astship_collide(asts):#checks if any asteroids have hit the ship
        global lives
        for ast in asts:
            if ast.rect.colliderect(spaceship.rect):
                if ast in asts:
                    asts.remove(ast)
                ast.remove(all_sprites_list)
                lives-=1
                explosion_noise.play()




    window_width = 900
    window_height = 600
    screen = pygame.display.set_mode((window_width, window_height))

    pygame.display.set_caption("Asteroids")

    clock = pygame.time.Clock()

    spaceship = Player(15, window_height / 2, 122, 58)

    all_sprites_list = pygame.sprite.Group()
    all_sprites_list.add(spaceship)


    def update_score():  # function changes score
        global score
        font = pygame.font.SysFont("comicsansms", 25)
        text = font.render(("POINTS:"+str(score)), True, (WHITE))
        return text


    def update_lives():  # function changes lives
        global lives
        font = pygame.font.SysFont("comicsansms", 25)
        text = font.render(("LIVES:"+str(lives)), True, (WHITE))
        return text

    def update_bonuses(): # function changes the amount of bonuses
        global extra_lasers
        font = pygame.font.SysFont("comicsansms", 25)
        text = font.render(("MULTI-LASERS: "+str(extra_lasers)), True, (WHITE))
        return text


    bonus_count=0#counts time so the bonuses and walls come at intervals
    wall_count=0

    start_screen=True

    while(start_screen):#start screen, runs until they click, displays controls and runs pygame event loop to check for click
        screen.fill((0, 0, 0))
        screen.blit(bgImg, (0, 0))
        font1 = pygame.font.SysFont("arialblack", 75)
        title=font1.render("Asteroids", True, (WHITE))
        font2 = pygame.font.SysFont("arialblack", 27)
        control1=font2.render("INSTRUCTIONS:", True, (WHITE))
        control2 = font2.render("ARROW KEYS -- MOVE UP & DOWN", True, (WHITE))
        control3 = font2.render("SPACEBAR -- SHOOT NORMAL LASER", True, (WHITE))
        control4 = font2.render("Z -- SHOOT MULTI-LASER", True, (WHITE))
        instruction1=font2.render("SHOOT ASTEROID -- GAIN 100 POINTS", True, (WHITE))
        instruction2=font2.render("DODGE ASTEROID -- LOSE 100 POINTS", True, (WHITE))
        instruction3=font2.render("SHOOT        -- GET 3 MULTI-LASERS", True, (WHITE))
        click_start = font2.render("CLICK TO START", True, (WHITE))
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==pygame.MOUSEBUTTONUP:
                if event.button==1:
                    start_screen=False
        screen.blit(title, (275, 25))
        screen.blit(control1, (275, 150))
        screen.blit(control2, (275, 200))
        screen.blit(control3, (275, 250))
        screen.blit(control4, (275, 300))
        screen.blit(instruction1, (275, 350))
        screen.blit(instruction2, (275, 400))
        screen.blit(instruction3, (275, 450))
        screen.blit(speed_upImg, (375, 450))
        screen.blit(click_start, (275, 550))
        pygame.display.flip()
        

    while True:
        lasast_collide(asteroid_list, laser_list)
        astship_collide(asteroid_list)
        lasbonus_collide(bonus_list, laser_list)

        if bonus_count==30:#adds a bonus every time 30 asteroids are shot
            y = Bonus(window_width, random.randint(75, 500), 81, 48)
            bonus_list.append(y)
            all_sprites_list.add(y)
            bonus_count=0

        if wall_count==50:#adds a wall every 40 asteroids
            asteroid_limit=35
            wall_count=-30

        if len(asteroid_list)>30:#resets the asteroid limit if there are too many astroids on screen
            asteroid_limit=5

        if len(asteroid_list) < asteroid_limit :#adds an asteroid if they have less then a certain number of asteroids on the screen
            x = Asteroid(random.randint(window_width, window_width+1000), random.randint(75, 500), 87, 85)
            asteroid_list.append(x)
            all_sprites_list.add(x)
            bonus_count+=1
            wall_count+=1


        for event in pygame.event.get():
             if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
             elif event.type == pygame.KEYDOWN:
                 spaceship.MoveKeyDown(event.key)
             elif event.type == pygame.KEYUP:
                 spaceship.MoveKeyUp(event.key)

        for ent in all_sprites_list:
            ent.update()

        for asteroid in asteroid_list:#checks if asteroids have left the screen
            if asteroid.rect.x<=0:
                asteroid.remove(all_sprites_list)
                asteroid_list.remove(asteroid)
                score-=100
        for laser in laser_list:#checks if lasers have left the screen
            if laser.rect.x>900:
                laser.remove(all_sprites_list)
                laser_list.remove(laser)
        for bonus in bonus_list:#checks if bonuses have left the screen
            if bonus.rect.x<=0:
                bonus.remove(all_sprites_list)
                bonus_list.remove(bonus)

        if lives==0:#if they die it displays highscores from a text file and waits for a click to restart
            big_explosion.play()
            end_screen=True
            file = open("highscores.txt", "r")
            scores = file.readlines()
            file.close()
            scores = [SCORE.replace('\n', '') for SCORE in scores]#gets scores
            if score > int(scores[9]):
                for SCORE in scores:
                    if score >= int(SCORE):
                        scores.insert(scores.index(SCORE), str(score))
                        break
                del scores[-1]#sorts scores
            while(end_screen):
                screen.fill((0, 0, 0))
                screen.blit(bgImg, (0, 0))
                font3=pygame.font.SysFont("arialblack", 27)
                highscore_text=font3.render(("HIGHSCORE    YOUR SCORE: "+str(score)), True, (WHITE))
                continue_text = font3.render("CLICK TO CONTINUE", True, (WHITE))
                SCORE1 = font3.render("1. " + scores[0], True, (WHITE))
                SCORE2 = font3.render("2. " + scores[1], True, (WHITE))
                SCORE3 = font3.render("3. " + scores[2], True, (WHITE))
                SCORE4 = font3.render("4. " + scores[3], True, (WHITE))
                SCORE5 = font3.render("5. " + scores[4], True, (WHITE))
                SCORE6 = font3.render("6. " + scores[5], True, (WHITE))
                SCORE7 = font3.render("7. " + scores[6], True, (WHITE))
                SCORE8 = font3.render("8. " + scores[7], True, (WHITE))
                SCORE9 = font3.render("9. " + scores[8], True, (WHITE))
                SCORE10 = font3.render("10. " + scores[9], True, (WHITE))
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type==pygame.MOUSEBUTTONUP:
                        if event.button==1:
                            file=open("highscores.txt", "w")
                            for SCORE in scores:
                                file.write(SCORE+"\n")
                            file.close()
                            end_screen=False
                screen.blit(highscore_text, (325, 75))
                screen.blit(SCORE1, (325, 125))
                screen.blit(SCORE2, (325, 150))
                screen.blit(SCORE3, (325, 175))
                screen.blit(SCORE4, (325, 200))
                screen.blit(SCORE5, (325, 225))
                screen.blit(SCORE6, (325, 250))
                screen.blit(SCORE7, (325, 275))
                screen.blit(SCORE8, (325, 300))
                screen.blit(SCORE9, (325, 325))
                screen.blit(SCORE10, (325, 350))
                screen.blit(continue_text, (275, 450))
                pygame.display.flip()
            start_game()

        screen.fill((0, 0, 0))
        screen.blit(bgImg, (0, 0))

        text1=update_score()
        screen.blit(text1, (600, 25))

        text2=update_lives()
        screen.blit(text2, (400, 25))

        text3=update_bonuses()
        screen.blit(text3, (100, 25))

        all_sprites_list.draw(screen)

        pygame.display.flip()

        clock.tick(60)

start_game()
