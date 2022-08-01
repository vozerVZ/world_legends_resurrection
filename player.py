import pygame
import node
import inventory

screen_height = 1080
screen_width = 1920

tile_w = 40
tile_h = 40


class Player:
    def __init__(self, x_pos, y_pos, loc_arr, invt):
        self.x = x_pos
        self.y = y_pos
        self.max_hp = 100
        self.hp = self.max_hp
        self.max_mana = 100
        self.mana = self.max_mana
        self.damage = 1
        self.armor = 0
        self.exp = 0
        self.money = 0
        self.heal = 5
        self.mana_regen = 2
        self.inv = invt

        self.loc_id = 0
        self.loc_arr = loc_arr

        self.mode = "walk"
        self.enemy_goal = -1
        self.attack_radius = tile_w * 2
        self.attackers_count = 0

        self.dest_x = self.x
        self.dest_y = self.y + screen_height//12

        self.loc_map = self.loc_arr[self.loc_id].get_relief_matrix()
        self.ent_map = self.loc_arr[self.loc_id].get_entities_matrix()
        self.path = []
        self.nodes = []

        self.chase_seek_timer = 0
        self.attack_timer = 0
        self.heal_timer = 0
        self.mana_regen_timer = 0
        self.revive_timer = 0
        self.q_timer = 0
        self.w_timer = 0
        self.e_timer = 0
        self.r_timer = 0
        self.shield_timer = 0

        self.q_skill_manacost = 10
        self.w_skill_manacost = 10
        self.e_skill_manacost = 10
        self.r_skill_manacost = 10

        for j in range(0, len(self.loc_map)):
            for i in range(0, len(self.loc_map[0])):
                if self.loc_map[j][i] != '0':
                    self.nodes.append(node.Node(i, j, j * len(self.loc_map[0]) + i, -1, -1, -1, -1))
                else:
                    if i == 0 or self.loc_map[j][i - 1] != '0':
                        l_n = -1
                    else:
                        l_n = j * len(self.loc_map[0]) + i - 1

                    if i == len(self.loc_map[0]) - 1 or self.loc_map[j][i + 1] != '0':
                        r_n = -1
                    else:
                        r_n = j * len(self.loc_map[0]) + i + 1

                    if j == 0 or self.loc_map[j - 1][i] != '0':
                        u_n = -1
                    else:
                        u_n = (j - 1) * len(self.loc_map[0]) + i

                    if j == len(self.loc_map) - 1 or self.loc_map[j + 1][i] != '0':
                        d_n = -1
                    else:
                        d_n = (j + 1) * len(self.loc_map[0]) + i

                    self.nodes.append(node.Node(i, j, j * len(self.loc_map[0]) + i, r_n, l_n, u_n, d_n))

    def update_nodes(self):
        self.nodes.clear()
        for j in range(0, len(self.loc_map)):
            for i in range(0, len(self.loc_map[0])):
                if self.loc_map[j][i] != '0':
                    self.nodes.append(node.Node(i, j, j * len(self.loc_map[0]) + i, -1, -1, -1, -1))
                else:
                    if i == 0 or self.loc_map[j][i - 1] != '0':
                        l_n = -1
                    else:
                        l_n = j * len(self.loc_map[0]) + i - 1

                    if i == len(self.loc_map[0]) - 1 or self.loc_map[j][i + 1] != '0':
                        r_n = -1
                    else:
                        r_n = j * len(self.loc_map[0]) + i + 1

                    if j == 0 or self.loc_map[j - 1][i] != '0':
                        u_n = -1
                    else:
                        u_n = (j - 1) * len(self.loc_map[0]) + i

                    if j == len(self.loc_map) - 1 or self.loc_map[j + 1][i] != '0':
                        d_n = -1
                    else:
                        d_n = (j + 1) * len(self.loc_map[0]) + i

                    self.nodes.append(node.Node(i, j, j * len(self.loc_map[0]) + i, r_n, l_n, u_n, d_n))

    def dijkstra_alg(self, x_from, y_from, x_to, y_to):
        for i in self.nodes:
            i.path.clear()
            i.path.append([i.x, i.y])
            i.path_len = -1
            i.done = False

        queue = [self.nodes[x_from + y_from * len(self.loc_map[0])]]

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

        return self.nodes[x_to + y_to * len(self.loc_map[0])].path

    def clear_timers(self):
        self.chase_seek_timer = 0
        self.attack_timer = 0
        self.heal_timer = 0
        self.mana_regen_timer = 0
        self.revive_timer = 0
        self.q_timer = 0
        self.w_timer = 0
        self.e_timer = 0
        self.r_timer = 0
        self.shield_timer = 0

    def decrease_timers(self):
        if self.chase_seek_timer > 0:
            self.chase_seek_timer -= 1
        if self.attack_timer > 0:
            self.attack_timer -= 1
        if self.heal_timer > 0:
            self.heal_timer -= 1
        if self.mana_regen_timer > 0:
            self.mana_regen_timer -= 1
        if self.revive_timer > 0:
            self.revive_timer -= 1
        if self.q_timer > 0:
            self.q_timer -= 1
        if self.w_timer > 0:
            self.w_timer -= 1
        if self.e_timer > 0:
            self.e_timer -= 1
        if self.r_timer > 0:
            self.r_timer -= 1
        if self.shield_timer > 0:
            self.shield_timer -= 1

    def re_init(self, info):
        self.x = int(info[0])
        self.dest_x = self.x
        self.y = int(info[1])
        self.dest_y = self.y + screen_height // 12
        self.loc_id = int(info[2])
        self.path.clear()
        self.mode = "walk"
        self.enemy_goal = -1
        self.attackers_count = 0
        self.loc_map = self.loc_arr[self.loc_id].get_relief_matrix()
        self.ent_map = self.loc_arr[self.loc_id].get_entities_matrix()
        self.update_nodes()
        self.max_hp = int(info[3])
        self.hp = self.max_hp
        self.max_mana = int(info[4])
        self.mana = self.max_mana
        self.damage = int(info[5])
        self.armor = int(info[6])
        self.exp = int(info[7])
        self.money = int(info[8])
        self.clear_timers()

    def get_info(self):
        player_info = []
        player_info.append(self.x)
        player_info.append(self.y)
        player_info.append(self.loc_id)
        player_info.append(self.max_hp)
        player_info.append(self.max_mana)
        player_info.append(self.damage)
        player_info.append(self.armor)
        player_info.append(self.exp)
        player_info.append(self.money)

        return player_info

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_loc_id(self):
        return self.loc_id

    def get_damage(self, dmg):
        if self.shield_timer == 0:
            self.hp -= dmg

        return self.hp > 0

    def set_stats(self, dmg, armor, max_hp, max_mana):
        self.damage += dmg
        self.armor += armor
        self.max_hp += max_hp
        self.max_mana += max_mana

        if self.hp > self.max_hp:
            self.hp = self.max_hp
        if self.mana > self.max_mana:
            self.mana = self.max_mana

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.max_hp

    def get_mana(self):
        return self.mana

    def get_max_mana(self):
        return self.max_mana

    def damage_enemy(self, dmg):
        if not self.enemy_goal.get_damage(dmg):
            reward = self.enemy_goal.get_reward()
            self.exp += reward[0]
            self.money += reward[1]
            drop = self.enemy_goal.drop()
            if len(drop) > 0:
                self.inv.add_equip(drop)
            self.mode = "walk"
            self.enemy_goal.set_count(False)
            self.attackers_count -= 1
            self.enemy_goal = -1

    def set_dest_coords(self, d_x, d_y):
        chase_flag = False

        for i in self.ent_map:
            if i.get_rect().collidepoint(d_x, d_y):
                self.enemy_goal = i
                self.mode = "chase"
                chase_flag = True
                break

        if self.loc_map[d_y // tile_h][d_x // tile_w] == '0' and not chase_flag:
            self.mode = "walk"
            self.path.clear()
            self.enemy_goal = -1
            self.path = self.dijkstra_alg(self.x // tile_w, (self.y + screen_height//12) // tile_h, d_x // tile_w, d_y // tile_h)
            self.dest_x = d_x
            self.dest_y = d_y

    def q_skill(self):
        if self.mana >= self.q_skill_manacost and self.q_timer == 0 and self.enemy_goal != -1:
            self.mana -= self.q_skill_manacost
            self.q_timer = 300
            self.damage_enemy(self.damage * 3)

    def is_q_skill_ready(self):
        return self.mana >= self.q_skill_manacost and self.q_timer == 0

    def w_skill(self):
        if self.mana >= self.w_skill_manacost and self.w_timer == 0:
            self.hp += self.max_hp // 10
            self.w_timer = 300
            self.mana -= self.w_skill_manacost
            if self.hp > self.max_hp:
                self.hp = self.max_hp

    def is_w_skill_ready(self):
        return self.mana >= self.w_skill_manacost and self.w_timer == 0

    def e_skill(self):
        e_g = self.enemy_goal
        if self.mana >= self.e_skill_manacost and self.e_timer == 0:
            for i in self.ent_map:
                if abs(self.x - i.get_x()) <= tile_w * 3 and abs(self.y - i.get_y()) <= tile_h * 3:
                    i.start_chasing()
                    self.enemy_goal = i
                    self.damage_enemy(self.damage * 2)
            self.mana -= self.e_skill_manacost
            self.e_timer = 300
        self.enemy_goal = e_g

    def is_e_skill_ready(self):
        return self.mana >= self.e_skill_manacost and self.e_timer == 0

    def r_skill(self):
        if self.mana >= self.r_skill_manacost and self.r_timer == 0:
            self.shield_timer = 500
            self.r_timer = 300
            self.mana -= self.r_skill_manacost

    def is_r_skill_ready(self):
        return self.mana >= self.r_skill_manacost and self.r_timer == 0
    
    def move(self):
        '''
        if self.x < self.dest_x:
            if self.loc_arr[self.loc_id].get_relief_matrix()[self.y // tile_h][(self.x + screen_width // 40 + 2) // tile_w] == '0':
                self.x += 1
        elif self.x > self.dest_x:
            if self.loc_arr[self.loc_id].get_relief_matrix()[self.y // tile_h][(self.x - 2) // tile_w] == '0':
                self.x -= 1
        
        if (self.y + screen_height//12) < self.dest_y:
            if self.loc_arr[self.loc_id].get_relief_matrix()[(self.y + screen_height // 12 + 2) // tile_h][self.x // tile_w] == '0':
                self.y += 1
        elif (self.y + screen_height//12) > self.dest_y:
            if self.loc_arr[self.loc_id].get_relief_matrix()[(self.y + screen_height//12 - 2) // tile_h][self.x // tile_w] == '0':
                self.y -= 1
        '''
        if len(self.path) > 0:
            if self.x // tile_w == self.path[0][0] and (self.y + screen_height//12) // tile_h == self.path[0][1]:
                self.path.pop(0)
            elif self.x // tile_w < self.path[0][0]:
                self.x += 1
            elif self.x // tile_w > self.path[0][0]:
                self.x -= 1
            elif (self.y + screen_height//12) // tile_h > self.path[0][1]:
                self.y -= 1
            elif (self.y + screen_height//12) // tile_h < self.path[0][1]:
                self.y += 1
                
    def draw(self, sc):
        pygame.draw.rect(sc, [0, 0, 42], (self.x, self.y, screen_width//40, screen_height//12), 4)
        #for i in self.path:
            #pygame.draw.rect(sc, [42, 0, 42], (i[0] * tile_w, i[1] * tile_h, tile_w, tile_h))

    def update(self, sc):
        self.decrease_timers()

        if self.hp <= 0 and self.revive_timer == 0:
            self.revive_timer = 1000
            self.money *= 0.8
            self.loc_arr[self.loc_id].unagr_all_enemies()
            self.mode = "walk"
            self.enemy_goal = -1

        if self.revive_timer == 1:
            self.loc_id = 0
            self.hp = self.max_hp
            self.x = 200
            self.y = 200
            self.dest_x = self.x
            self.dest_y = self.y + screen_height // 12
            self.loc_map = self.loc_arr[self.loc_id].get_relief_matrix()
            self.ent_map = self.loc_arr[self.loc_id].get_entities_matrix()
            self.path.clear()
            self.update_nodes()

        if self.attackers_count == 0 and self.hp < self.max_hp and self.heal_timer == 0 and self.revive_timer == 0:
            self.hp += self.heal
            self.heal_timer = 200
            if self.hp > self.max_hp:
                self.hp = self.max_hp

        if self.mana < self.max_mana and self.mana_regen_timer == 0 and self.revive_timer == 0:
            self.mana += self.mana_regen
            self.mana_regen_timer = 200
            if self.mana > self.max_mana:
                self.mana = self.max_mana

        if self.x // tile_w == 0 and self.loc_arr[self.loc_id].get_left_neighbour() != -1:
            self.path.clear()
            self.mode = "walk"
            self.loc_arr[self.loc_id].unagr_all_enemies()
            self.loc_id = self.loc_arr[self.loc_id].get_left_neighbour()
            self.loc_map = self.loc_arr[self.loc_id].get_relief_matrix()
            self.ent_map = self.loc_arr[self.loc_id].get_entities_matrix()
            self.update_nodes()
            self.x = screen_width - tile_w * 2
            self.attackers_count = 0
            #self.dest_x = self.x
            #self.dest_y = self.y + screen_height//12
        elif self.x // tile_w == 47 and self.loc_arr[self.loc_id].get_right_neighbour() != -1:
            self.path.clear()
            self.mode = "walk"
            self.loc_arr[self.loc_id].unagr_all_enemies()
            self.loc_id = self.loc_arr[self.loc_id].get_right_neighbour()
            self.loc_map = self.loc_arr[self.loc_id].get_relief_matrix()
            self.ent_map = self.loc_arr[self.loc_id].get_entities_matrix()
            self.update_nodes()
            self.x = tile_w * 1 + 2
            self.attackers_count = 0
            #self.dest_x = self.x
            #self.dest_y = self.y + screen_height//12
        elif (self.y + screen_height // 12) // tile_h == 0 and self.loc_arr[self.loc_id].get_up_neighbour() != -1:
            self.path.clear()
            self.mode = "walk"
            self.loc_arr[self.loc_id].unagr_all_enemies()
            self.loc_id = self.loc_arr[self.loc_id].get_up_neighbour()
            self.loc_map = self.loc_arr[self.loc_id].get_relief_matrix()
            self.ent_map = self.loc_arr[self.loc_id].get_entities_matrix()
            self.update_nodes()
            self.y = tile_h * 18 - 20
            self.attackers_count = 0
            #self.dest_x = self.x
            #self.dest_y = self.y + screen_height//12
        elif (self.y + screen_height // 12) // tile_h == 20 and self.loc_arr[self.loc_id].get_down_neighbour() != -1:
            self.path.clear()
            self.mode = "walk"
            self.loc_arr[self.loc_id].unagr_all_enemies()
            self.loc_id = self.loc_arr[self.loc_id].get_down_neighbour()
            self.loc_map = self.loc_arr[self.loc_id].get_relief_matrix()
            self.ent_map = self.loc_arr[self.loc_id].get_entities_matrix()
            self.update_nodes()
            self.y = tile_h - screen_height // 12 + 5
            self.attackers_count = 0
            #self.dest_x = self.x
            #self.dest_y = self.y + screen_height//12

        if self.mode == "chase" and self.chase_seek_timer == 0:
            self.path.clear()
            self.path = self.dijkstra_alg(self.x // tile_w, (self.y + screen_height // 12) // tile_h, self.enemy_goal.get_x() // tile_w,
                                          (self.enemy_goal.get_y() + screen_height // 12) // tile_h)
            self.chase_seek_timer = 50

        if self.mode == "chase" and abs(self.x - self.enemy_goal.get_x()) < self.attack_radius and abs(self.y - self.enemy_goal.get_y()) < self.attack_radius and self.attack_timer == 0:
            self.enemy_goal.start_chasing()
            self.attack_timer = 100
            if not self.enemy_goal.is_counted():
                self.attackers_count += 1
                self.enemy_goal.set_count(True)
            self.damage_enemy(self.damage)

        if self.revive_timer == 0:
            self.move()
            self.draw(sc)
        
        
