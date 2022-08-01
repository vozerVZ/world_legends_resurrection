import pygame


def draw_loc(sc, tiles_arr, locs, idd, x, y, x_bias, y_bias, flag):
    loc = locs[idd]
    loc.is_draw = True
    loc_arr = loc.get_tile_matrix()
    for i in range(len(loc_arr[0])):
        for j in range(len(loc_arr)):
            if int(loc_arr[j][i]) < len(tiles_arr):
                sc.blit(tiles_arr[int(loc_arr[j][i])], (x + i * 9 + 432 * x_bias, y + j * 9 + 189 * y_bias))
            else:
                pygame.draw.rect(sc, [0, 0, 0], (x + i * 9 + 432 * x_bias, y + j * 9 + 189 * y_bias, 9, 9))
    pygame.draw.rect(sc, [0, 0, 0], (x + 432 * x_bias, y + 189 * y_bias, 432, 189), 3)
    if flag == 0:
        pygame.draw.circle(sc, [255, 0, 0], (x + 216 + 432 * x_bias, y + 94 + 189 * y_bias), 25)

    if loc.get_left_neighbour() != -1 and not locs[loc.get_left_neighbour()].is_draw:
        draw_loc(sc, tiles_arr, locs, loc.get_left_neighbour(), x - 432, y, x_bias, y_bias, 1)
    if loc.get_right_neighbour() != -1 and not locs[loc.get_right_neighbour()].is_draw:
        draw_loc(sc, tiles_arr, locs, loc.get_right_neighbour(), x + 432, y, x_bias, y_bias, 1)
    if loc.get_up_neighbour() != -1 and not locs[loc.get_up_neighbour()].is_draw:
        draw_loc(sc, tiles_arr, locs, loc.get_up_neighbour(), x, y - 189, x_bias, y_bias, 1)
    if loc.get_down_neighbour() != -1 and not locs[loc.get_down_neighbour()].is_draw:
        draw_loc(sc, tiles_arr, locs, loc.get_down_neighbour(), x, y + 189, x_bias, y_bias, 1)