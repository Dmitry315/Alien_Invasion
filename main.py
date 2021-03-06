from GameObjects import *

particles = pygame.sprite.Group()


def lose(windows, score, font):
    print_text(windows, "You lose, total score: {}".format(score), font)
    pygame.display.update()
    sleep(1)
    while pygame.event.wait().type != pygame.KEYDOWN:
        pass


def destruction(cords):
    global particles
    numbers = range(-6, 6)

    for i in range(100):
        dx = choice(numbers)
        dy = choice(numbers)
        while not(dx and dy):
            dx = choice(numbers)
            dy = choice(numbers)
        Particle(particles, cords, dx, dy, choice([2, 3, 4, 5]) * 10)


def main():
    ################################################################
    global SPEED, particles
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
    enemy_speed = 2.5 if difficulty == 3 else 2

    # enemy spawn rate
    # if DIFFICULTY == 0 enemies won't spawn
    if difficulty != 0:
        spawn = 2000 - difficulty * 300
    else:
        spawn = 0
    ################################################################
    # init Earth
    earth_cords = (width // 2 - 45, height // 2 - 50)
    earth = Earth(earth_cords, EARTH_IMAGE)
    # pygame.time.set_timer(EARTH_ROTATE, 75)

    # init hero
    hero = Hero((width // 5, height // 2), SPEED, PLAYER_IMAGE)

    clock = pygame.time.Clock()

    # init game
    pygame.init()
    pygame.mouse.set_pos(0, 0)

    # init mixer
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.mixer.init()
    fire = pygame.mixer.Sound('sounds/fire.wav')
    destruction_sound = pygame.mixer.Sound('sounds/destuction.wav')

    # init font
    font = pygame.font.Font(None, 50)

    # game score:
    score = 0

    # is paused:
    pause = False

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
    # init sprite groups of enemies and bullets
    # to check collision
    enemies_sprites = pygame.sprite.Group()
    bullets_sprites = pygame.sprite.Group()
    run = True

    # first level cycle
    while run:
        clock.tick(fps)

        # check events
        for event in pygame.event.get():
            # if event.type == EARTH_ROTATE:
            #     earth.update()
            if event.type == METEOR_APPEAR:
                meteor = Meteor((choice(meteor_spawn), -100), METEOR_IMAGE)
            if event.type == ENEMY_APPEAR:
                cords = choice(enemy_spawn)
                enemy = SpaceEnemy(cords, enemy_speed,
                                   ENEMY_SPACESHIP_IMAGE, (width // 2, height // 2))
                enemies_sprites.add(enemy)
            # fire button
            if event.type == pygame.MOUSEBUTTONDOWN:
                fire.play(1)
                bullet = Bullet((hero.rect.x + 40, hero.rect.y + 40),
                                pygame.mouse.get_pos())
                bullets_sprites.add(bullet)
            # pause
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause = True

        # get pressed keys
        keys = pygame.key.get_pressed()
        # close game on esc
        if keys[pygame.K_ESCAPE]:
            run = False

        # move hero with WASD
        x = 0
        y = 0
        if keys[pygame.K_w] and hero.rect.y > SPEED:
            y -= SPEED
        if keys[pygame.K_a] and hero.rect.x > SPEED:
            x -= SPEED
        if keys[pygame.K_s] and hero.rect.y < height - SPEED - 80:
            y += SPEED
        if keys[pygame.K_d] and hero.rect.x < width - SPEED - 80:
            x += SPEED
        windows.fill((0, 0, 0))
        if pause:
            print_text(windows, "pause, SPACE to continue", font)
        else:
            print_text(windows, "score: {}".format(score), font)
        hero.move((x, y))

        # gravitation effect
        if difficulty >= 2 or not difficulty:
            hero.gravitation((width // 2, height // 2))

        # init hero hit box

        # meteor
        if meteor:
            meteor.move()
            meteor.draw_object(windows)

        # check collision
        if pygame.sprite.collide_mask(hero, earth):
            lose(windows, score, font)
            break
        if meteor and run:
            if pygame.sprite.collide_mask(hero, meteor):
                lose(windows, score, font)
                break
        # depict Earth
        earth.draw_object(windows)
        del_list = []
        # check collision
        for i in bullets_sprites:
            flag = i.move()
            if flag:
                del_list.append(i)
            else:
                if meteor:
                    if pygame.sprite.collide_mask(i, meteor):
                        del_list.append(i)
                        destruction_sound.play(1)
                if pygame.sprite.collide_mask(i, earth) and run:
                    run = False
                    lose(windows, score, font)
        # delete bullets out from game
        for i in del_list:
            bullets_sprites.remove(i)
        # draw bullets
        bullets_sprites.draw(windows)

        del_list = []
        for i in enemies_sprites:
            i.move()
            # can't use enemies_sprites.draw(windows)
            # because it draws without rotation
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
                    del_list.append(i)
            # collision with bullets
            bull = pygame.sprite.spritecollideany(i, bullets_sprites)
            if bull:
                bullets_sprites.remove(bull)
                del_list.append(i)
                score += 100 * difficulty
        # delete collided enemies
        for i in del_list:
            destruction_sound.play(1)
            destruction((i.rect.x + 20, i.rect.y + 20))
            enemies_sprites.remove(i)

        if run:
            # hero follow mouse
            hero.draw_object(windows, pygame.mouse.get_pos())
            particles.update()
            particles.draw(windows)
            pygame.display.update()
        if pause:
                while pygame.event.wait().type != pygame.KEYDOWN:
                    pass
                pause = False
    if difficulty:
        with open('score.txt', mode="r", encoding='utf-8') as f:
            lines = f.readlines()
            if int(lines[difficulty - 1]) < score:
                lines[difficulty - 1] = str(score) + '\n'
        with open('score.txt', mode="w", encoding='utf-8') as f:
            for i in lines:
                f.write(i)
    pygame.quit()


if __name__ == '__main__':
    main()
