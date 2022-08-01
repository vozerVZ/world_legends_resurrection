import pygame
import random
import node


#name, behavior, hp, damage, exp_reward, money_reward
entitites_arr = [["butterfly", "P", 5, 2, 0, 0, [0, 1, 2]]]

helmet = pygame.image.load("res/eq/helmet.png")
chestplate = pygame.image.load("res/eq/chestplate.png")
sword = pygame.image.load("res/eq/sword.png")
# type, img, +dmg, +armor, +max_hp, +max_mana, chance
#types: 1 - helmet 2 - chestplate 3 - weapon
things = [[1, helmet, 0, 0, 0, 100, 50],
          [2, chestplate, 0, 0, 100, 0, 40],
          [3, sword, 10, 0, 0, 0, 20]]


screen_height = 1080
screen_width = 1920

tile_w = 40
tile_h = 40


class Entity:
    def __init__(self, info, rel_mtx):
        self.player = -1

        self.name = entitites_arr[int(info[0])][0]
        self.behavior = entitites_arr[int(info[0])][1]  # F - Friendly P - passive A - aggressive
        self.max_hp = entitites_arr[int(info[0])][2]
        self.hp = self.max_hp
        self.damage = entitites_arr[int(info[0])][3]
        self.exp_reward = entitites_arr[int(info[0])][4]
        self.money_reward = entitites_arr[int(info[0])][5]
        self.drop_arr = entitites_arr[int(info[0])][6]

        self.x_left_corner = int(info[1])
        self.y_left_corner = int(info[2])
        self.x_right_corner = int(info[3])
        self.y_right_corner = int(info[4])

        self.x = int(info[1]) * tile_w
        self.y = int(info[2]) * tile_h

        self.x_dest = self.x // tile_w
        self.y_dest = (self.y + screen_height // 12) // tile_h

        self.wandering_timer = 0
        self.chase_seek_timer = 0
        self.attack_timer = 0
        self.revive_timer = 0

        self.mode = "walk"
        self.attack_radius = tile_w * 2
        self.agr_radius = tile_w * 3

        self.is_count = False

        self.relief_matrix = rel_mtx
        self.nodes = []

        for j in range(0, len(self.relief_matrix)):
            for i in range(0, len(self.relief_matrix[0])):
                if self.relief_matrix[j][i] != '0':
                    self.nodes.append(node.Node(i, j, j * len(self.relief_matrix[0]) + i, -1, -1, -1, -1))
                else:
                    if i == 0 or self.relief_matrix[j][i - 1] != '0':
                        l_n = -1
                    else:
                        l_n = j * len(self.relief_matrix[0]) + i - 1

                    if i == len(self.relief_matrix[0]) - 1 or self.relief_matrix[j][i + 1] != '0':
                        r_n = -1
                    else:
                        r_n = j * len(self.relief_matrix[0]) + i + 1

                    if j == 0 or self.relief_matrix[j - 1][i] != '0':
                        u_n = -1
                    else:
                        u_n = (j - 1) * len(self.relief_matrix[0]) + i

                    if j == len(self.relief_matrix) - 1 or self.relief_matrix[j + 1][i] != '0':
                        d_n = -1
                    else:
                        d_n = (j + 1) * len(self.relief_matrix[0]) + i

                    self.nodes.append(node.Node(i, j, j * len(self.relief_matrix[0]) + i, r_n, l_n, u_n, d_n))

        self.path = self.dijkstra_alg(self.x // tile_w, (self.y + screen_height//12) // tile_h, self.x_dest, self.y_dest)

    def dijkstra_alg(self, x_from, y_from, x_to, y_to):
        for i in self.nodes:
            i.path.clear()
            i.path.append([i.x, i.y])
            i.path_len = -1
            i.done = False

        queue = [self.nodes[x_from + y_from * len(self.relief_matrix[0])]]

        for i in queue:
            if not i.done:
                neighbours = i.get_neighbours()
                for j in neighbours:
                    queue.append(self.nodes[j])
                    if self.nodes[j].path_len == -1 or self.nodes[j].path_len > (i.path_len + 1):
                        path_arr = i.path.copy()
                        path_arr.append([self.nodes[j].x, self.nodes[j].y])
                        self.nodes[j].set_path(i.path_len + 1, path_arr)

                i.done = True

        return self.nodes[x_to + y_to * len(self.relief_matrix[0])].path

    def set_count(self, mode):
        self.is_count = mode

    def is_counted(self):
        return self.is_count

    def set_player_class(self, player):
        self.player = player

    def start_chasing(self):
        if self.behavior == "P" or self.behavior == "A":
            self.mode = "chase"

    def start_walking(self):
        self.hp = self.max_hp
        self.mode = "walk"
        self.x_dest = random.randint(self.x_left_corner, self.x_right_corner)
        self.y_dest = random.randint(self.y_left_corner, self.y_right_corner)
        self.path.clear()
        self.path = self.dijkstra_alg(self.x // tile_w, (self.y + screen_height // 12) // tile_h, self.x_dest,
                                      self.y_dest)

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_rect(self):
        return pygame.Rect(self.x, self.y, screen_width // 40, screen_height // 12)

    def get_reward(self):
        return [self.exp_reward, self.money_reward]

    def get_damage(self, dmg):
        self.hp -= dmg

        return self.hp > 0

    def drop(self):
        drop_lottery = []
        for i in self.drop_arr:
            lottery = random.randint(0, 100)
            #print(lottery, things[int(i)][6])
            if lottery <= things[int(i)][6]:
                drop_lottery.append(int(i))

        return drop_lottery

    def draw(self, sc):
        #for i in self.path:
            #pygame.draw.rect(sc, [0, 255, 255], (i[0] * tile_w, i[1] * tile_h, tile_w, tile_h))
        pygame.draw.rect(sc, [0, 42, 0], (self.x, self.y, screen_width // 40, screen_height // 12), 4)

        pygame.draw.rect(sc, [255, 0, 0], (self.x, self.y - tile_h//3, screen_width // 40 * self.hp // self.max_hp, tile_h//4))
        pygame.draw.rect(sc, [0, 0, 0], (self.x, self.y - tile_h // 3, screen_width // 40, tile_h // 4), 2)

    def move(self):
        if self.wandering_timer == 0:
            '''
            if self.x_dest < self.x // tile_w:
                self.x -= 1
            elif self.x_dest > self.x // tile_w:
                self.x += 1

            if self.y_dest < self.y // tile_h:
                self.y -= 1
            elif self.y_dest > self.y // tile_h:
                self.y += 1
            '''
            if len(self.path) > 0:
                if self.x // tile_w == self.path[0][0] and (self.y + screen_height // 12) // tile_h == self.path[0][1]:
                    self.path.pop(0)
                elif self.x // tile_w < self.path[0][0]:
                    self.x += 1
                elif self.x // tile_w > self.path[0][0]:
                    self.x -= 1
                elif (self.y + screen_height // 12) // tile_h > self.path[0][1]:
                    self.y -= 1
                elif (self.y + screen_height // 12) // tile_h < self.path[0][1]:
                    self.y += 1

    def update(self, sc, draw_flag):
        if self.wandering_timer > 0:
            self.wandering_timer -= 1
        if self.chase_seek_timer > 0:
            self.chase_seek_timer -= 1
        if self.attack_timer > 0:
            self.attack_timer -= 1
        if self.revive_timer > 0:
            self.revive_timer -= 1
        if self.revive_timer == 1:
            self.hp = self.max_hp
            self.x = self.x_dest * tile_w
            self.y = self.y_dest * tile_h
            self.start_walking()

        if self.hp <= 0 and self.revive_timer == 0:
            self.revive_timer = 1000

        if self.revive_timer == 0:
            if self.behavior == "A" and abs(self.x - self.player.get_x()) < self.agr_radius and abs(self.y - self.player.get_y()) < self.agr_radius:
                self.start_chasing()

            if self.mode == "chase" and self.chase_seek_timer == 0:
                self.path.clear()
                self.path = self.dijkstra_alg(self.x // tile_w, (self.y + screen_height // 12) // tile_h,
                                              self.player.get_x() // tile_w,
                                              (self.player.get_y() + screen_height // 12) // tile_h)
                self.chase_seek_timer = 50

            if self.mode == "chase" and abs(self.x - self.player.get_x()) < self.attack_radius and abs(self.y - self.player.get_y()) < self.attack_radius and self.attack_timer == 0:
                self.attack_timer = 100
                self.player.get_damage(self.damage)

            if self.mode == "walk" and self.x_dest == self.x // tile_w and self.y_dest == (self.y + screen_height//12) // tile_h:
                self.path.clear()
                self.wandering_timer = random.randint(100, 400)
                while True:
                    self.x_dest = random.randint(self.x_left_corner, self.x_right_corner)
                    self.y_dest = random.randint(self.y_left_corner, self.y_right_corner)
                    if self.relief_matrix[self.y_dest][self.x_dest] == '0':
                        break

                self.path = self.dijkstra_alg(self.x // tile_w, (self.y + screen_height//12) // tile_h, self.x_dest, self.y_dest)

            self.move()
            if draw_flag:
                self.draw(sc)
