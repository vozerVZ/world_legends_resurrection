import pygame
import equipment

delete_icon = pygame.image.load("res/img/delete.png")


class InvCell:
    def __init__(self, mode, x, y):
        if mode == 0:  # inventory cell
            self.w = 90
            self.h = 90
            self.mode = 0
        else:  # player equip cell
            self.w = 150
            self.h = 150
            self.mode = mode

        self.x = x
        self.y = y
        self.equip = 0

    def get_rect(self):
        if self.mode == 0:
            return pygame.Rect(1000 + self.x * self.w, 20 + self.y * self.h, self.w, self.h)
        else:
            return pygame.Rect(self.x, self.y, self.w, self.h)


class Inv:
    def __init__(self):
        self.inventory = []
        for i in range(10):
            inv_line = []
            for j in range(10):
                inv_line.append(InvCell(0, j, i))
            self.inventory.append(inv_line)

        inv_line = [InvCell(1, 50, 50), InvCell(2, 50, 250), InvCell(3, 50, 450)]
        self.inventory.append(inv_line)

    def get_cell(self, x, y):
        for i in self.inventory:
            for j in i:
                if j.get_rect().collidepoint(x, y):
                    return j
                    break
        return -1

    def set_equip(self, x, y, eq_id):
        for i in self.inventory:
            for j in i:
                if j.get_rect().collidepoint(x, y):
                    j.equip = equipment.Equip(eq_id)
                    break

    def get_inv_arr(self):
        arr = []
        for i in self.inventory:
            for j in i:
                if j.equip == 0:
                    arr.append(-1)
                else:
                    arr.append(j.equip.id)

        return arr

    def fill_inventory(self, arr):
        for k in range(len(arr)):
            if int(arr[k]) != -1:
                self.inventory[k // 10][k % 10].equip = equipment.Equip(int(arr[k]))
            else:
                self.inventory[k // 10][k % 10].equip = 0

    def add_equip(self, arr):
        for i in arr:
            for j in self.inventory:
                flag = False
                for z in j:
                    if z.equip == 0:
                        z.equip = equipment.Equip(int(i))
                        flag = True
                        break
                if flag:
                    break

    def draw(self, sc):
        sc.fill([162, 95, 42])

        for i in self.inventory:
            for j in i:
                if j.mode == 0:
                    pygame.draw.rect(sc, [0, 0, 0], (1000 + j.x * j.w, 20 + j.y * j.h, j.w, j.h), 2)
                else:
                    pygame.draw.rect(sc, [0, 0, 0], (j.x, j.y, j.w, j.h), 2)
                if j.equip != 0:
                    if j.mode == 0:
                        j.equip.draw(sc, 1000 + j.x * j.w, 20 + j.y * j.h, 0)
                    else:
                        j.equip.draw(sc, j.x, j.y, 1)
        sc.blit(delete_icon, (50, 900))
