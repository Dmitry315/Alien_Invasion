from GameObjects import *


def lose(windows, score, font):
    print_text(windows, "You lose, total score: {}".format(score), font)
    pygame.display.update()
    sleep(2)
    while pygame.event.wait().type != pygame.KEYDOWN:
        pass


def main():
    ################################################################
    global enemy_speed, bullet_radius, spawn, speed, difficulty, fps
    with open('game_settings.txt', encoding='utf-8', mode='r') as f:
        lines = f.readlines()
        fps = int(lines[0].split()[1])
        diff = int(lines[1].split()[1])
        if diff > 3:
            difficulty = 3
        elif diff < 0:
            difficulty = 0
        else:
            difficulty = diff

    # enemy speed
    enemy_speed = 3 if difficulty == 3 else 2

    # enemy spawn rate
    # if DIFFICULTY == 0 enemies won't spawn
    if difficulty != 0:
        spawn = 2000 - difficulty * 300
    else:
        spawn = 0
    ################################################################
    # init Earth
    earth_cords = (width // 2 - 50, height // 2 - 50)
    earth = Earth(earth_cords, EARTH_IMAGE)

    # init hero
    hero = Hero((width // 2, height // 4), speed, PLAYER_IMAGE)

    clock = pygame.time.Clock()

    # init game
    pygame.init()
    pygame.mouse.set_pos(0, 0)

    # init font
    font = pygame.font.Font(None, 50)

    # game score:
    score = 0

    # FULL SCREEN
    windows = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    windows.fill((0, 0, 0))

    # Enemies appear every 1.5 sec
    if difficulty != 0:
        pygame.time.set_timer(ENEMY_APPEAR, spawn)

    # Meteor appears every 10 sec
    if difficulty == 3:
        pygame.time.set_timer(METEOR_APPEAR, 10000)
    meteor = None
    # Enemy's spawn
    enemy_spawn = [
        (0, 0), (width // 2, 0),
        (width, 0), (width, height // 2),
        (width, height), (width // 2, height),
        (0, height), (0, height // 2)
        # Spawn map:
        #  * - - * - - *
        #  |           |
        #  *     E     *
        #  |           |
        #  * - - * - - *
    ]

    # Meteor spawn
    meteor_spawn = list(range(100, width // 3)) + list(range(width * 2 // 3, width - 100))
    # Spawn map:
    #  / * * - * * \
    #  |           |
    #  |     E     |
    #  |           |
    #  \ - - - - - /
    # init list of enemies and bullets
    # to check collision
    enemies = []
    bullets = []
    run = True

    # first level cycle
    while run:
        clock.tick(fps)

        # check events
        for event in pygame.event.get():
            if event.type == METEOR_APPEAR:
                meteor = Meteor((choice(meteor_spawn), -100), METEOR_IMAGE)
            elif event.type == ENEMY_APPEAR:
                cords = choice(enemy_spawn)
                enemies.append(SpaceEnemy(cords, enemy_speed,
                                          ENEMY_SPACESHIP_IMAGE, earth_cords))
            # fire button
            elif event.type == pygame.MOUSEBUTTONDOWN:
                bullets.append(Bullet((hero.rect.x + 40, hero.rect.y + 40),
                                      pygame.mouse.get_pos()))

        # get pressed keys
        keys = pygame.key.get_pressed()
        # close game on esc
        if keys[pygame.K_ESCAPE]:
            run = False

        # move hero with WASD
        x = 0
        y = 0
        if keys[pygame.K_w]:
            y -= speed
        if keys[pygame.K_a]:
            x -= speed
        if keys[pygame.K_s]:
            y += speed
        if keys[pygame.K_d]:
            x += speed
        windows.fill((0, 0, 0))
        print_text(windows, "score: {}".format(score), font)
        hero.move((x, y))

        # gravitation effect
        if difficulty >= 2:
            hero.gravitation(earth_cords)

        # init hero hit box

        # meteor
        if meteor:
            meteor.move()
            meteor.draw_object(windows)

        # check collision
        if pygame.sprite.collide_mask(hero, earth):
            run = False
            lose(windows, score, font)
        if meteor and run:
            if pygame.sprite.collide_mask(hero, meteor):
                run = False
                lose(windows, score, font)
        # depict Earth
        earth.draw_object(windows)
        del_list = []
        # check collision
        for num, i in enumerate(bullets):
            flag = i.move()
            if flag:
                del_list.append(num)
            else:
                i.draw_object(windows)
                if meteor:
                    if pygame.sprite.collide_mask(i, meteor):
                        # if bull_hit_box.colliderect(meteor_hit_box):
                        del_list.append(num)
                if pygame.sprite.collide_mask(i, earth) and run:
                    # elif bull_hit_box.colliderect(earth_hit_box) and run:
                    run = False
                    lose(windows, score, font)
                    pygame.quit()
        # delete bullets out from game
        for i in range(len(del_list)):
            del bullets[del_list[i] - i]

        del_list = []
        del_list2 = []
        for num, i in enumerate(enemies):
            i.move()
            i.draw_object(windows)
            # check collision with hero
            if pygame.sprite.collide_mask(i, hero) and run:
                run = False
                lose(windows, score, font)
            # check collision with earth
            if pygame.sprite.collide_mask(i, earth) and run:
                run = False
                lose(windows, score, font)
            # collision with meteor
            elif meteor:
                if pygame.sprite.collide_mask(i, meteor):
                    del_list.append(num)
            # collision with bullets
            for j in range(len(bullets)):
                # if enemy_hit_box.colliderect(bullets[j].hit_box()):
                if pygame.sprite.collide_mask(i, bullets[j]):
                    del_list.append(num)
                    del_list2.append(j)
                    score += 100 * difficulty
        # delete collided enemies and bullets
        for i in range(len(del_list)):
            del enemies[del_list[i] - i]
        for i in range(len(del_list2)):
            del bullets[del_list2[i] - i]

        # hero follow mouse
        if run:
            hero.draw_object(windows, pygame.mouse.get_pos())
            pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
