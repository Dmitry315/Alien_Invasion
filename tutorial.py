from GameObjects import *


def tutorial():

    # init hero
    hero = Hero((500, 500), speed, PLAYER_IMAGE)

    # init Earth
    earth_cords = (width // 2 - 50, height // 2 - 50)
    earth = Earth(earth_cords, EARTH_IMAGE)

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

    # init font
    font = pygame.font.Font(None, 50)

    pygame.mouse.set_pos(0, 0)

    # FULL SCREEN
    windows = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    windows.fill((0, 0, 0))
    # init list of enemies and bullets
    # to check collision
    enemies = []
    bullets = []
    run = True
    while run:
        clock.tick(fps)
        # check events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if dialog_count in [0, 4, 5] and event.key == pygame.K_SPACE:
                    dialog_count += 1
            # fire button
            elif event.type == pygame.MOUSEBUTTONDOWN:
                bullets.append(Bullet((hero.rect.x + 40, hero.rect.y + 40), pygame.mouse.get_pos()))
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
            y -= speed
            w = 1 if dialog_count == 1 else 0
        if keys[pygame.K_a]:
            x -= speed
            a = 1 if dialog_count == 1 else 0
        if keys[pygame.K_s]:
            y += speed
            s = 1 if dialog_count == 1 else 0
        if keys[pygame.K_d]:
            x += speed
            d = 1 if dialog_count == 1 else 0
        if w and a and s and d and dialog_count == 1:
            dialog_count = 2
            bullets = []
        windows.fill((0, 0, 0))

        # print dialogs
        if dialog_count < len(dialogs):
            print_text(windows, dialogs[dialog_count][:-1], font)
        hero.move((x, y))

        # add targets
        if dialog_count == 3 and q:
            q = 0
            enemies.extend([
                SpaceEnemy((width * 3 // 4, height // 4), 0,
                           ENEMY_SPACESHIP_IMAGE, (hero.rect.x, hero.rect.y)),
                SpaceEnemy((width * 3 // 4, height * 2 // 4), 0,
                           ENEMY_SPACESHIP_IMAGE, (hero.rect.x, hero.rect.y)),
                SpaceEnemy((width * 3 // 4, height * 3 // 4), 0,
                           ENEMY_SPACESHIP_IMAGE, (hero.rect.x, hero.rect.y))
            ])

        del_list = []
        del_list2 = []
        for num, i in enumerate(bullets):
            flag = i.move()
            if flag:
                del_list.append(num)
            else:
                # check collision for bullets
                if meteor:
                    if pygame.sprite.collide_mask(i, meteor):
                        del_list.append(num)
                if pygame.sprite.collide_mask(i, earth) and dialog_count >= 4:
                    del_list.append(num)
                for num1, j in enumerate(enemies):
                    if pygame.sprite.collide_mask(i, j):
                        del_list.append(num)
                        del_list2.append(num1)
                i.draw_object(windows)

        # delete collided enemies and bullets
        for i in range(len(del_list)):
            del bullets[del_list[i] - i]
        for i in range(len(del_list2)):
            del enemies[del_list2[i] - i]

        # check collision for enemies with hero
        for i in enemies:
            if pygame.sprite.collide_mask(i, hero):
                hero.rect.x = 500
                hero.rect.y = 500
            i.draw_object(windows)

        # targets killed
        if not bool(enemies) and dialog_count == 3:
            dialog_count = 4
            hero.rect.x = width // 4
            hero.rect.y = height // 2
            bullets = []
        # draw Earth
        if dialog_count >= 4:
            earth.draw_object(windows)
        # check collision hero and earth
        if pygame.sprite.collide_mask(hero, earth) and dialog_count >= 4:
            hero.rect.x = width // 4
            hero.rect.y = height // 2
        # add gravitation
        if dialog_count == 5:
            hero.gravitation(earth_cords)
        # show meteor
        if dialog_count == 6:
            if not q:
                q = 1
                enemies.append(SpaceEnemy((width * 3 // 4, height * 2 // 4), 0,
                               ENEMY_SPACESHIP_IMAGE, (hero.rect.x, hero.rect.y)))
            meteor.move()
            meteor.draw_object(windows)
            for i in enemies:
                if pygame.sprite.collide_mask(meteor, i):
                    enemies = []
        if meteor.rect.y > height and dialog_count == 6:
            dialog_count += 1

        # hero follow mouse
        hero.draw_object(windows, pygame.mouse.get_pos())

        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    tutorial()
