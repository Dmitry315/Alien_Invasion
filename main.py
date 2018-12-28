from GameObjects import *

from random import choice

# add player speed
SPEED = 8
# FPS
FPS = 60
# load images
PLAYER_IMAGE = pygame.image.load('spaceship.png')
EARTH_IMAGE = pygame.image.load('Earth.png')
ENEMY_SPACESHIP = pygame.image.load('enemy_spaceship.png')

clock = pygame.time.Clock()


# init Earth
earth_cords = (width // 2 - 50, height // 2 - 50)
Earth = Earth(earth_cords, EARTH_IMAGE)
earth_hit_box = Earth.hit_box(100, 95)

# init hero
hero = Hero((500, 500), SPEED, PLAYER_IMAGE)

# events
ENEMY_APPEAR = 30


def main():
    # init game
    pygame.init()
    pygame.mouse.set_pos(0, 0)
    # FULL SCREEN
    windows = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    windows.fill((0, 0, 0))

    pygame.time.set_timer(ENEMY_APPEAR, 1500)
    enemy_spawn = [
        (0, 0), (width // 2, 0),
        (width, 0), (width, height//2),
        (width, height), (width // 2, height),
        (0, height), (0, height // 2)
        # Spawn map:
        #  * - * - *
        #  |       |
        #  *       *
        #  |       |
        #  * - * - *
    ]
    # init list of enemies and bullets
    # to check collision
    enemies = []
    bullets = []
    run = True
    # first level cycle
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == ENEMY_APPEAR:
                cords = choice(enemy_spawn)
                enemies.append(SpaceEnemy(cords, 2, ENEMY_SPACESHIP, earth_cords))
            if event.type == pygame.MOUSEBUTTONDOWN:
                bullets.append(Bullet((hero.x + 40, hero.y + 40), pygame.mouse.get_pos()))
        # get pressed keys
        keys = pygame.key.get_pressed()
        # close game on esc
        if keys[pygame.K_ESCAPE]:
            run = False
        # move hero with WASD
        x = 0
        y = 0
        if keys[pygame.K_w]:
            y -= SPEED
        if keys[pygame.K_a]:
            x -= SPEED
        if keys[pygame.K_s]:
            y += SPEED
        if keys[pygame.K_d]:
            x += SPEED
        windows.fill((0, 0, 0))
        hero.move((x, y))
        # init hero hit box
        hero_hit_box = pygame.Rect(hero.x, hero.y, 80, 80)
        # check collision
        if hero.hit_box().colliderect(earth_hit_box):
            run = False
            print('collided')
        # depict objects
        Earth.draw_object(windows)
        del_list = []
        for num, i in enumerate(bullets):
            flag = i.move()
            if flag:
                del_list.append(num)
            else:
                i.draw_object(windows)
                if i.hit_box().colliderect(earth_hit_box):
                    run = False
                    print('collided')
        for i in range(len(del_list)):
            del bullets[del_list[i] - i]
        del_list = []
        del_list2 = []
        for num, i in enumerate(enemies):
            i.move()
            i.draw_object(windows)
            if i.hit_box().colliderect(hero.hit_box()):
                run = False
                print('collided')
            if i.hit_box().colliderect(earth_hit_box):
                run = False
                print('collided')
            for j in range(len(bullets)):
                if i.hit_box().colliderect(bullets[j].hit_box()):
                    del_list.append(num)
                    del_list2.append(j)
        for i in range(len(del_list)):
            del enemies[del_list[i] - i]
        for i in range(len(del_list2)):
            del bullets[del_list2[i] - i]

        # hero follow mouse
        hero.draw_object(windows, pygame.mouse.get_pos())
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
