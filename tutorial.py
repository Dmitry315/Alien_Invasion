from GameObjects import *

particles = pygame.sprite.Group()


def destruction(cords):
    global particles
    numbers = range(-6, 6)
    for _ in range(100):
        dx = choice(numbers)
        dy = choice(numbers)
        while not(dx and dy):
            dx = choice(numbers)
            dy = choice(numbers)
        Particle(particles, cords, dx, dy, choice([2, 3, 4, 5]) * 10)


def tutorial():
    with open('game_settings.txt', encoding='utf-8', mode='r') as f:
        lines = f.readlines()
        fps = int(lines[0].split()[1])
    # init hero
    hero = Hero((width // 6, height // 2), SPEED, PLAYER_IMAGE)

    # init Earth
    earth_cords = (width // 2 - 50, height // 2 - 50)
    earth = Earth(earth_cords, EARTH_IMAGE)
    # pygame.time.set_timer(EARTH_ROTATE, 75)

    # init meteor
    meteor = Meteor((width * 3 // 4, -100), METEOR_IMAGE)

    # load dialogs:
    with open('dialogs/tutorial.txt', encoding='utf-8', mode='r') as file:
        dialogs = file.readlines()
    dialog_count = 0
    clock = pygame.time.Clock()
    # flags
    w, a, s, d = 0, 0, 0, 0
    q = 1
    # init game
    pygame.init()

    # init mixer
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.mixer.init()
    fire = pygame.mixer.Sound('sounds/fire.wav')
    destruction_sound = pygame.mixer.Sound('sounds/destuction.wav')

    # init font
    font = pygame.font.Font(None, 50)

    pygame.mouse.set_pos(0, 0)

    # FULL SCREEN
    windows = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    windows.fill((0, 0, 0))
    # init list of enemies and bullets
    # to check collision
    enemies_sprites = pygame.sprite.Group()
    bullets_sprites = pygame.sprite.Group()
    run = True
    while run:
        clock.tick(fps)
        # check events
        for event in pygame.event.get():
            # if event.type == EARTH_ROTATE:
            #     earth.update()
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if dialog_count in [0, 4, 5] and event.key == pygame.K_SPACE:
                    dialog_count += 1
            # fire button
            elif event.type == pygame.MOUSEBUTTONDOWN:
                fire.play(1)
                bullets_sprites.add(Bullet((hero.rect.x + 40, hero.rect.y + 40),
                                           pygame.mouse.get_pos()))
                if dialog_count == 2:
                    dialog_count = 3

        # get pressed keys
        keys = pygame.key.get_pressed()
        # close game on esc
        if keys[pygame.K_ESCAPE]:
            run = False

        # move hero with WASD
        # check hero moved in tutorial
        x = 0
        y = 0
        if keys[pygame.K_w]:
            y -= SPEED
            w = 1 if dialog_count == 1 else 0
        if keys[pygame.K_a]:
            x -= SPEED
            a = 1 if dialog_count == 1 else 0
        if keys[pygame.K_s]:
            y += SPEED
            s = 1 if dialog_count == 1 else 0
        if keys[pygame.K_d]:
            x += SPEED
            d = 1 if dialog_count == 1 else 0
        if w and a and s and d and dialog_count == 1:
            dialog_count = 2
            bullets_sprites = pygame.sprite.Group()
        windows.fill((0, 0, 0))

        # print dialogs
        if dialog_count < len(dialogs):
            print_text(windows, dialogs[dialog_count][:-1], font)
        hero.move((x, y))

        # add targets
        if dialog_count == 3 and q:
            q = 0
            enemies_sprites.add(SpaceEnemy((width * 3 // 4, height // 4), 0,
                                           ENEMY_SPACESHIP_IMAGE, (hero.rect.x, hero.rect.y)))
            enemies_sprites.add(SpaceEnemy((width * 3 // 4, height * 2 // 4), 0,
                                           ENEMY_SPACESHIP_IMAGE, (hero.rect.x, hero.rect.y)))
            enemies_sprites.add(SpaceEnemy((width * 3 // 4, height * 3 // 4), 0,
                                           ENEMY_SPACESHIP_IMAGE, (hero.rect.x, hero.rect.y)))

        del_list = []
        # del_list2 = []
        for i in bullets_sprites:
            flag = i.move()
            if flag:
                del_list.append(i)
            else:
                # check collision for bullets
                if meteor:
                    if pygame.sprite.collide_mask(i, meteor):
                        destruction_sound.play(1)
                        del_list.append(i)
                if pygame.sprite.collide_mask(i, earth) and dialog_count >= 4:
                    del_list.append(i)
                # collision with bullets
                enemy = pygame.sprite.spritecollideany(i, enemies_sprites)
                if enemy:
                    destruction_sound.play(1)
                    destruction((enemy.rect.x + 20, enemy.rect.y + 20))
                    enemies_sprites.remove(enemy)
                    del_list.append(i)
        # delete collided enemies and bullets
        for i in del_list:
            bullets_sprites.remove(i)
        bullets_sprites.draw(windows)

        # check collision for enemies with hero
        for i in enemies_sprites:
            if pygame.sprite.collide_mask(i, hero):
                hero.rect.x = width // 4
                hero.rect.y = height // 2
            i.draw_object(windows)

        # targets killed
        if not bool(enemies_sprites) and dialog_count == 3:
            dialog_count = 4
            hero.rect.x = width // 4
            hero.rect.y = height // 2
            bullets_sprites = pygame.sprite.Group()
        # draw Earth
        if dialog_count >= 4:
            earth.draw_object(windows)
        # check collision hero and earth
        if pygame.sprite.collide_mask(hero, earth) and dialog_count >= 4:
            hero.rect.x = width // 4
            hero.rect.y = height // 2
        # add gravitation
        if dialog_count == 5:
            if not q:
                hero.rect.x = width // 4
                hero.rect.y = height // 2
                q = 1
            hero.gravitation(earth_cords)
        # show meteor
        if dialog_count == 6:
            if q:
                q = 0
                enemies_sprites.add(SpaceEnemy((width * 3 // 4, height * 2 // 4), 0,
                                               ENEMY_SPACESHIP_IMAGE,
                                               (hero.rect.x, hero.rect.y)))
            meteor.move()
            meteor.draw_object(windows)
            enemy = pygame.sprite.spritecollideany(meteor, enemies_sprites)
            if enemy:
                destruction_sound.play(1)
                destruction((enemy.rect.x + 20, enemy.rect.y + 20))
                enemies_sprites = pygame.sprite.Group()
            if pygame.sprite.collide_mask(meteor, hero):
                hero.rect.x = width // 4
                hero.rect.y = height // 2
        if meteor.rect.y > height and dialog_count == 6:
            dialog_count += 1

        # hero follow mouse
        hero.draw_object(windows, pygame.mouse.get_pos())
        particles.update()
        particles.draw(windows)
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    tutorial()
