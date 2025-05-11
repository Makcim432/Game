import pygame

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption('Run And Jump')
icon = pygame.image.load('icon.png').convert_alpha()
pygame.display.set_icon(icon)

bg = pygame.image.load('bg.png').convert_alpha()
walk_left = [
    pygame.image.load('player_left1.png').convert_alpha(),
    pygame.image.load('player_left2.png').convert_alpha(),
    pygame.image.load('player_left3.png').convert_alpha(),
    pygame.image.load('player_left4.png').convert_alpha(),

]
walk_right = [
    pygame.image.load('player_right1.png').convert_alpha(),
    pygame.image.load('player_right2.png').convert_alpha(),
    pygame.image.load('player_right3.png').convert_alpha(),
    pygame.image.load('player_right4.png').convert_alpha(),
]



ghost = pygame.image.load('ghost.png').convert_alpha()
ghost_list_in_game = []
player_anim_count = 0
bg_x = 0

player_speed = 7
player_x = 100
player_y = 550

is_jump = False
jump_count = 10

ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 3000)

label = pygame.font.SysFont('Times New Roman', 40)
lose_label = label.render('Вы проиграли!', False, ('Red'))
restart_label = label.render('Играть заново', False, ('Green'))
restart_label_rect = restart_label.get_rect(topleft=(350, 350))

gameplay = True


bg_sound = pygame.mixer.Sound('music.mp3')
bg_sound.play(100)
jump_sound = pygame.mixer.Sound('jump.mp3')

running = True
while running:
    
    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 920, 0))
    
    if gameplay:
        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

        if ghost_list_in_game:
            for (i, el) in enumerate(ghost_list_in_game):
                screen.blit(ghost, el)
                el.x -= 10


                if el.x < -10:
                    ghost_list_in_game.pop(i)


                if player_rect.colliderect(el):
                    gameplay = False




        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

        if keys[pygame.K_a] and player_x > 50:
            player_x -= player_speed
        elif keys[pygame.K_d] and player_x < 500:
            player_x += player_speed

        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
                jump_sound.play()
        else:
            if jump_count >= -10:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 10

        if player_anim_count == 3:
            player_anim_count = 0
        else:

            player_anim_count += 1

        bg_x -= 2
        if bg_x == -900:
            bg_x = 0
    else:
        screen.fill((87, 88, 89))
        screen.blit(lose_label, (350, 250))
        screen.blit(restart_label, restart_label_rect)

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 100
            ghost_list_in_game.clear()

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit

        if event.type == ghost_timer:
            ghost_list_in_game.append(ghost.get_rect(topleft=(1002, 550)))

    clock.tick(15)