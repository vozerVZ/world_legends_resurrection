import pygame
import entity

screen_height = 1080
screen_width = 1920

tile_w = 40
tile_h = 40


class Location:
    def __init__(self, txt_file):
        self.is_draw = False
        self.tile_matrix = []
        self.relief_matrix = []
        self.entities_matrix = []

        f = open("res/maps/" + txt_file, "r")
        itr = 0
        for line in f:
            if itr == 0:
                self.id_text = line.split()[0]
            elif 2 <= itr <= 22:
                self.tile_matrix.append(line.split())
            elif 24 <= itr <= 44:
                self.relief_matrix.append(line.split())
            elif itr == 46:
                self.id = int(line.split()[0])
                self.l_n = int(line.split()[1])
                self.r_n = int(line.split()[2])
                self.u_n = int(line.split()[3])
                self.d_n = int(line.split()[4])
            elif itr >= 48:
                self.entities_matrix.append(entity.Entity(line.split(), self.relief_matrix))

            itr += 1
        f.close()

    def get_tile_matrix(self):
        return self.tile_matrix

    def get_relief_matrix(self):
        return self.relief_matrix

    def get_entities_matrix(self):
        return self.entities_matrix

    def get_left_neighbour(self):
        return self.l_n

    def get_right_neighbour(self):
        return self.r_n

    def get_up_neighbour(self):
        return self.u_n

    def get_down_neighbour(self):
        return self.d_n

    def get_id(self):
        return self.id

    def unagr_all_enemies(self):
        for i in self.entities_matrix:
            i.start_walking()
            i.set_count(False)

    def draw(self, sc, tiles_arr):
        for i in range(len(self.tile_matrix[0])):
            for j in range(len(self.tile_matrix)):
                if int(self.tile_matrix[j][i]) < len(tiles_arr):
                    sc.blit(tiles_arr[int(self.tile_matrix[j][i])], (i * tile_w, j * tile_h))
                    #pygame.draw.rect(sc, [255, 0, 0], (i * tile_w, j * tile_h, tile_w, tile_h), 2)
                else:
                    pygame.draw.rect(sc, [0, 0, 0], (i * tile_w, j * tile_h, tile_w, tile_h))