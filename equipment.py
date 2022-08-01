import pygame

screen_height = 1080
screen_width = 1920

helmet = pygame.image.load("res/eq/helmet.png")
chestplate = pygame.image.load("res/eq/chestplate.png")
sword = pygame.image.load("res/eq/sword.png")
# type, img, name, +dmg, +armor, +max_hp, +max_mana, chance
#types: 1 - helmet 2 - chestplate 3 - weapon
things = [[1, helmet, "helmet", 0, 0, 0, 100, 50],
          [2, chestplate, "chestplate", 0, 0, 100, 0, 20],
          [3, sword, "sword", 10, 0, 0, 0, 20]]


class Equip:
    def __init__(self, eq_id):
        self.id = eq_id
        self.type = things[eq_id][0]
        self.img = things[eq_id][1]
        self.name = things[eq_id][2]
        self.dmg = things[eq_id][3]
        self.armor = things[eq_id][4]
        self.hp = things[eq_id][5]
        self.mana = things[eq_id][6]
        self.chance = things[eq_id][7]

    def get_info(self):
        info = []
        info.append(self.type)
        info.append(self.img)
        info.append(self.dmg)
        info.append(self.armor)
        info.append(self.hp)
        info.append(self.mana)
        return info

    def get_id(self):
        return self.id

    def draw(self, sc, x, y, mode):
        if mode == 0:
            sc.blit(self.img, (x, y))
        else:
            sc.blit(pygame.transform.scale(self.img, (150, 150)), (x, y))

    def draw_stat(self, sc, font, x, y):
        if screen_height - y > 410:
            mod = 0
        else:
            mod = -1

        pygame.draw.rect(sc, [255, 255, 255], (x, y, 200, 400))

        text = font.render(self.name, 1, [0, 0, 0])
        sc.blit(text, (x + 10, y + 20))

        h_mod = 1

        if self.dmg > 0:
            text = font.render("+" + str(self.dmg) + " dmg", 1, [0, 0, 0])
            sc.blit(text, (x + 10, y + 20 + 40 * h_mod))
            h_mod += 1

        if self.armor > 0:
            text = font.render("+" + str(self.armor) + " armor", 1, [0, 0, 0])
            sc.blit(text, (x + 10, y + 20 + 40 * h_mod))
            h_mod += 1

        if self.hp > 0:
            text = font.render("+" + str(self.hp) + " max hp", 1, [0, 0, 0])
            sc.blit(text, (x + 10, y + 20 + 40 * h_mod))
            h_mod += 1

        if self.mana > 0:
            text = font.render("+" + str(self.mana) + " max mana", 1, [0, 0, 0])
            sc.blit(text, (x + 10, y + 20 + 40 * h_mod))
            h_mod += 1