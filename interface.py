import pygame

screen_height = 1080
screen_width = 1920

tile_w = 40
tile_h = 40


def interface_draw(sc, font, hp, max_hp, mana, max_mana, loc_matrix, tiles_arr, skills_arr, q_skill, w_skill, e_skill, r_skill):
    # hp/mana/skills bar
    pygame.draw.rect(sc, [162, 95, 42], (0, 840, 1920, 240))
    # hero image
    pygame.draw.rect(sc, [162, 95, 42], (0, 840, 300, 240))
    pygame.draw.rect(sc, [0, 0, 0], (0, 840, 300, 240), 4)
    # minimap
    pygame.draw.rect(sc, [162, 95, 42], (1548, 933, 336, 147))
    pygame.draw.rect(sc, [0, 0, 0], (1480, 883, 440, 197), 4)
    for i in range(len(loc_matrix[0])):
        for j in range(len(loc_matrix)):
            if int(loc_matrix[j][i]) < len(tiles_arr):
                sc.blit(tiles_arr[int(loc_matrix[j][i])], (4 + 1480 + i * 9, 4 + 883 + j * 9))
            else:
                pygame.draw.rect(sc, [0, 0, 0], (i * tile_w, j * tile_h, tile_w, tile_h))
    #hero hp
    pygame.draw.rect(sc, [155, 45, 48], (330, 900, 650, 40))
    pygame.draw.rect(sc, [193, 0, 32], (330, 900, 650 * hp // max_hp, 40))
    pygame.draw.rect(sc, [0, 0, 0], (330, 900, 650, 40), 2)

    hp_text = font.render(str(round(hp)) + "/" + str(max_hp), 1, [0, 0, 0])
    sc.blit(hp_text, (990, 908))

    # hero mana
    pygame.draw.rect(sc, [0, 33, 55], (330, 1000, 650, 40))
    pygame.draw.rect(sc, [51, 51, 255], (330, 1000, 650 * mana // max_mana, 40))
    pygame.draw.rect(sc, [0, 0, 0], (330, 1000, 650, 40), 2)

    hp_text = font.render(str(round(mana)) + "/" + str(max_mana), 1, [0, 0, 0])
    sc.blit(hp_text, (990, 1008))

    # Q skill
    if q_skill:
        sc.blit(skills_arr[0], (1150, 880))
    pygame.draw.rect(sc, [0, 0, 0], (1150, 880, 70, 70), 2)

    # W skill
    if w_skill:
        sc.blit(skills_arr[1], (1290, 880))
    pygame.draw.rect(sc, [0, 0, 0], (1290, 880, 70, 70), 2)

    # E skill
    if e_skill:
        sc.blit(skills_arr[2], (1150, 1000))
    pygame.draw.rect(sc, [0, 0, 0], (1150, 1000, 70, 70), 2)

    # R skill
    if r_skill:
        sc.blit(skills_arr[3], (1290, 1000))
    pygame.draw.rect(sc, [0, 0, 0], (1290, 1000, 70, 70), 2)