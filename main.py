# TYPE:DEV
# CODE:resurr
import pygame
import sys
import map
import player
import interface
import location
import inventory
import ctypes
ctypes.windll.user32.SetProcessDPIAware()


def arr_to_str(arr):
    s = ""
    for q in arr:
        s += (str(q) + ' ')

    return s[:-1]


pygame.init()
screen_width = 1920
screen_height = 1080

size = [screen_width, screen_height]
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

tile_w = 40
tile_h = 40

clock = pygame.time.Clock()

font1 = pygame.font.Font(None, 35)
font2 = pygame.font.Font(None, 60)

reset_flag = False
reset_timer = 0

menu_back = pygame.image.load("res/img/menu_background.png")
play_button = pygame.image.load("res/img/play_button.png")
fish_1 = pygame.image.load("res/img/fish_1.png")
fish_2 = pygame.image.load("res/img/fish_2.png")
exit_button = pygame.image.load("res/img/exit_button.png")
reset_button = pygame.image.load("res/img/reset_button.png")
sure_button = pygame.image.load("res/img/sure_button.png")

q_skill_icon = pygame.image.load("res/skills/q_skill.png")
w_skill_icon = pygame.image.load("res/skills/w_skill.png")
e_skill_icon = pygame.image.load("res/skills/e_skill.png")
r_skill_icon = pygame.image.load("res/skills/r_skill.png")

skills_icons = [q_skill_icon, w_skill_icon, e_skill_icon, r_skill_icon]

undefined_tile = pygame.image.load("res/tiles/undefined.png")
dirt_tile = pygame.image.load("res/tiles/dirt.png")
grass_tile = pygame.image.load("res/tiles/grass.png")
rock_tile = pygame.image.load("res/tiles/rock.png")
wood_tile = pygame.image.load("res/tiles/wood.png")
water_tile = pygame.image.load("res/tiles/water.png")

tiles = [dirt_tile, grass_tile, rock_tile, wood_tile, water_tile]
tiles_transformed_for_loc = []
tiles_transformed_for_minimap = []
for i in tiles:
    tiles_transformed_for_loc.append(pygame.transform.scale(i, (tile_w, tile_h)))
    tiles_transformed_for_minimap.append(pygame.transform.scale(i, (9, 9)))

locations = []

test_location_central = location.Location("test_location_central.txt")
locations.append(test_location_central)

test_location_left = location.Location("test_location_left.txt")
locations.append(test_location_left)

test_location_right = location.Location("test_location_right.txt")
locations.append(test_location_right)

test_location_up = location.Location("test_location_up.txt")
locations.append(test_location_up)

test_location_down = location.Location("test_location_down.txt")
locations.append(test_location_down)

inv = inventory.Inv()
hero = player.Player(850, 350, locations, inv)


f = open("res/saves/save_default.txt", "r")
save_default = [f.readline().split(), f.readline().split()]
f.close()

f = open("res/saves/save_1.txt", "r")
save_1 = [f.readline().split(), f.readline().split()]
f.close()

f = open("res/saves/save_2.txt", "r")
save_2 = [f.readline().split(), f.readline().split()]
f.close()

f = open("res/saves/save_3.txt", "r")
save_3 = [f.readline().split(), f.readline().split()]
f.close()

for i in locations:
    for j in i.get_entities_matrix():
        j.set_player_class(hero)

stage = 0  # 0 - menu 1 - saves 2 - game

is_inv_open = False
is_map_open = False

x_map_bias = 0
y_map_bias = 0

is_dnd_on = False
dnd_cell = -1

done = False

while not done:
    for i in pygame.event.get():
        if stage == 0:
            if i.type == pygame.MOUSEBUTTONUP:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 1520 <= mouse_x <= 1520 + play_button.get_width() and 100 <= mouse_y <= 100 + play_button.get_height():
                    stage = 1
                elif 1520 <= mouse_x <= 1520 + fish_1.get_width() and 300 <= mouse_y <= 300 + fish_1.get_height():
                    pass
                elif 1520 <= mouse_x <= 1520 + fish_2.get_width() and 500 <= mouse_y <= 500 + fish_2.get_height():
                    pass
                elif 1520 <= mouse_x <= 1520 + exit_button.get_width() and 700 <= mouse_y <= 700 + exit_button.get_height():
                    pygame.quit()
                    sys.exit()
        elif stage == 1:
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_ESCAPE:
                    stage = 0

            if i.type == pygame.MOUSEBUTTONUP:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 240 <= mouse_x <= 240 + reset_button.get_width() and 1000 <= mouse_y <= 1000 + reset_button.get_height():
                    if not reset_flag:
                        reset_flag = True
                        reset_timer = 200
                    else:
                        save_1.clear()
                        save_1 = save_default.copy()
                        with open("res/saves/save_1.txt", 'w') as f:
                            f.writelines(arr_to_str(save_1[0]) + '\n' + arr_to_str(save_1[1]))
                        f.close()
                        reset_flag = False
                        reset_timer = 0
                elif 0 <= mouse_x <= 640:
                    hero.re_init(save_1[0])
                    inv.fill_inventory(save_1[1])

                    mouse_x = hero.get_x()
                    mouse_y = hero.get_y()
                    mouse_cell_x = mouse_x // tile_w
                    mouse_cell_y = mouse_y // tile_h

                    stage = 2

        elif stage == 2:
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_ESCAPE:
                    if is_inv_open:
                        is_inv_open = False
                    elif is_map_open:
                        is_map_open = False
                    else:
                        player_info = arr_to_str(hero.get_info())
                        player_inv = arr_to_str(inv.get_inv_arr())
                        locations[hero.get_loc_id()].unagr_all_enemies()
                        with open("res/saves/save_1.txt", 'w') as f:
                            f.writelines(player_info + '\n' + player_inv)
                        f.close()
                        f = open("res/saves/save_1.txt", "r")
                        save_1 = [f.readline().split(), f.readline().split()]
                        f.close()
                        stage = 0
                elif i.key == pygame.K_UP and is_map_open:
                    y_map_bias -= 1
                elif i.key == pygame.K_DOWN and is_map_open:
                    y_map_bias += 1
                elif i.key == pygame.K_LEFT and is_map_open:
                    x_map_bias -= 1
                elif i.key == pygame.K_RIGHT and is_map_open:
                    x_map_bias += 1
                elif i.key == pygame.K_q and not is_inv_open and not is_map_open:
                    hero.q_skill()
                elif i.key == pygame.K_w and not is_inv_open and not is_map_open:
                    hero.w_skill()
                elif i.key == pygame.K_e and not is_inv_open and not is_map_open:
                    hero.e_skill()
                elif i.key == pygame.K_r and not is_inv_open and not is_map_open:
                    hero.r_skill()
                elif i.key == pygame.K_i and not is_map_open:
                    is_inv_open = not is_inv_open
                    is_dnd_on = False
                    dnd_cell = -1
                elif i.key == pygame.K_m and not is_inv_open:
                    if is_map_open:
                        x_map_bias = 0
                        y_map_bias = 0
                        for j in locations:
                            j.is_draw = False
                    is_map_open = not is_map_open

            if i.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if is_inv_open:
                    chose_cell = inv.get_cell(mouse_x, mouse_y)
                    if chose_cell != -1 and chose_cell.equip != 0:
                        is_dnd_on = True
                        dnd_cell = chose_cell
            elif i.type == pygame.MOUSEBUTTONUP:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_y < tile_h * 21 and not is_inv_open and not is_map_open:
                    hero.set_dest_coords(mouse_x, mouse_y)

                if is_inv_open and is_dnd_on:
                    if 50 <= mouse_x <= 200 and 900 <= mouse_y <= 1050:  # delete
                        if dnd_cell.mode != 0:
                            hero.set_stats(-1 * dnd_cell.equip.dmg, -1 * dnd_cell.equip.armor, -1 * dnd_cell.equip.hp, -1 * dnd_cell.equip.mana)
                        dnd_cell.equip = 0
                    chose_cell = inv.get_cell(mouse_x, mouse_y)
                    if chose_cell != -1:
                        if dnd_cell.mode == 0 and chose_cell.mode == 0:  # inv to inv
                            dnd_cell.equip, chose_cell.equip = chose_cell.equip, dnd_cell.equip
                        elif dnd_cell.mode != 0 and chose_cell.mode == 0 and (chose_cell.equip == 0 or dnd_cell.equip.type == chose_cell.equip.type):  # equip to inv
                            hero.set_stats(-1 * dnd_cell.equip.dmg, -1 * dnd_cell.equip.armor, -1 * dnd_cell.equip.hp, -1 * dnd_cell.equip.mana)
                            if chose_cell.equip != 0:
                                hero.set_stats(chose_cell.equip.dmg, chose_cell.equip.armor, chose_cell.equip.hp, chose_cell.equip.mana)
                            dnd_cell.equip, chose_cell.equip = chose_cell.equip, dnd_cell.equip
                        elif dnd_cell.mode == 0 and chose_cell.mode != 0 and dnd_cell.equip.type == chose_cell.mode:  # inv to equip
                            hero.set_stats(dnd_cell.equip.dmg, dnd_cell.equip.armor, dnd_cell.equip.hp, dnd_cell.equip.mana)
                            if chose_cell.equip != 0:
                                hero.set_stats(-1 * chose_cell.equip.dmg, -1 * chose_cell.equip.armor, -1 * chose_cell.equip.hp, -1 * chose_cell.equip.mana)
                            dnd_cell.equip, chose_cell.equip = chose_cell.equip, dnd_cell.equip

                    is_dnd_on = False
                    dnd_cell = -1

                mouse_cell_x = mouse_x // tile_w
                mouse_cell_y = mouse_y // tile_h

    screen.fill((255, 255, 255))

    if stage == 0:
        screen.blit(menu_back, (0, 0))
        screen.blit(play_button, (1520, 100))
        screen.blit(fish_1, (1520, 300))
        screen.blit(fish_2, (1520, 500))
        screen.blit(exit_button, (1520, 700))
    elif stage == 1:
        if reset_timer > 0:
            reset_timer -= 1
        if reset_timer == 0 and reset_flag:
            reset_flag = False
        pygame.draw.rect(screen, [153, 153, 153], (0, 0, 640, 1080), 2)
        pygame.draw.rect(screen, [153, 153, 153], (640, 0, 640, 1080), 2)
        pygame.draw.rect(screen, [153, 153, 153], (1280, 0, 640, 1080), 2)

        ch_text = font2.render("HP: " + str(round(int(save_1[0][3]))), 1, [0, 0, 0])
        screen.blit(ch_text, (50, 200))

        ch_text = font2.render("MANA: " + str(round(int(save_1[0][4]))), 1, [0, 0, 0])
        screen.blit(ch_text, (50, 300))

        ch_text = font2.render("DAMAGE: " + str(round(int(save_1[0][5]))), 1, [0, 0, 0])
        screen.blit(ch_text, (50, 400))

        ch_text = font2.render("ARMOR: " + str(round(int(save_1[0][6]))), 1, [0, 0, 0])
        screen.blit(ch_text, (50, 500))

        ch_text = font2.render("EXP: " + str(round(int(save_1[0][7]))), 1, [0, 0, 0])
        screen.blit(ch_text, (50, 600))

        ch_text = font2.render("MONEY: " + str(round(int(save_1[0][8]))), 1, [0, 0, 0])
        screen.blit(ch_text, (50, 700))

        if reset_flag:
            screen.blit(sure_button, (240, 1000))
        else:
            screen.blit(reset_button, (240, 1000))

        ch_text = font2.render("UNAVAILABLE", 1, [153, 153, 153])
        screen.blit(ch_text, (800, 500))

        ch_text = font2.render("UNAVAILABLE", 1, [153, 153, 153])
        screen.blit(ch_text, (1450, 500))

    elif stage == 2:
        locations[hero.get_loc_id()].draw(screen, tiles_transformed_for_loc)

        hero.update(screen)

        for i in locations:
            for j in i.get_entities_matrix():
                j.update(screen, i.get_id() == hero.get_loc_id())

        interface.interface_draw(screen, font1, hero.get_hp(), hero.get_max_hp(), hero.get_mana(), hero.get_max_mana(), locations[hero.get_loc_id()].get_tile_matrix(), tiles_transformed_for_minimap, skills_icons, hero.is_q_skill_ready(), hero.is_w_skill_ready(), hero.is_e_skill_ready(), hero.is_r_skill_ready())

    if is_inv_open:
        inv.draw(screen)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        cell = inv.get_cell(mouse_x, mouse_y)
        if cell != -1 and cell.equip != 0:
            cell.equip.draw_stat(screen, font1, mouse_x, mouse_y)

    if is_dnd_on:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dnd_cell.equip.draw(screen, mouse_x, mouse_y, 0)

    if is_map_open:
        screen.fill([255, 255, 255])
        for j in locations:
            j.is_draw = False
        map.draw_loc(screen, tiles_transformed_for_minimap, locations, hero.get_loc_id(), 800, 500, x_map_bias, y_map_bias, 0)

    pygame.display.flip()
    clock.tick(60)
