import arcade
import time
import random
from arcade.window_commands import get_window
from items import Sun, Pea


class Plant(arcade.AnimatedTimeSprite):
    def __init__(self, health, cost):
        super().__init__(0.12)
        self.health = health
        self.cost = cost
        self.line = 0
        self.column = 0

    def update(self):
        if self.health <= 0:
            self.kill()
            get_window().window.lawns.remove((self.line, self.column))

    def planting(self, center_x, center_y, line, column):
        self.center_x = center_x
        self.center_y = center_y
        self.line = line
        self.column = column


class SunFlower(Plant):
    def __init__(self):
        super().__init__(health=80, cost=50)
        self.texture = arcade.load_texture("sun1.png")
        for i in range(3):
            self.textures.append(arcade.load_texture("sun1.png"))
        for i in range(3):
            self.textures.append(arcade.load_texture("sun2.png"))
        self.sun_spawn = time.time()
        self.sun_sound = arcade.load_sound("sunspawn.mp3")

    def update(self):
        super().update()
        if time.time() - self.sun_spawn >= 15:
            sun = Sun(self.center_x + 20, self.center_y + 30)
            get_window().spawn_suns.append(sun)
            self.sun_spawn = time.time()
            self.sun_sound.play()


class PeaShooter(Plant):
    def __init__(self):
        super().__init__(100, 100)
        self.texture = arcade.load_texture("pea1.png")
        for i in range(2):
            self.textures.append(arcade.load_texture("pea1.png"))
        for i in range(2):
            self.textures.append(arcade.load_texture("pea2.png"))
        for i in range(2):
            self.textures.append(arcade.load_texture("pea3.png"))
        self.pea_spawn = time.time()
        self.pea_sound = arcade.load_sound("peaspawn.mp3")

    def update(self):
        super().update()
        zombie_on_line = False
        for zombie in get_window().window.zombies:
            if self.line == zombie.line:
                zombie_on_line = True
        if time.time() - self.pea_spawn >= 2 and zombie_on_line:
            pea = Pea(self.center_x + 10, self.center_y + 10)
            self.pea_spawn = time.time()
            get_window().peas.append(pea)
            self.pea_sound.play()


class WallNut(Plant):
    def __init__(self):
        super().__init__(200, 50)
        self.texture = arcade.load_texture("nut1.png")
        for i in range(10):
            self.textures.append(arcade.load_texture("nut1.png"))
        self.textures.append(arcade.load_texture("nut2.png"))
        for i in range(2):
            self.textures.append(arcade.load_texture("nut3.png"))
        self.textures.append(arcade.load_texture("nut2.png"))


class TorchWood(Plant):
    def __init__(self):
        super().__init__(100, 175)
        self.texture = arcade.load_texture("tree1.png")
        for i in range(2):
            self.textures.append(arcade.load_texture("tree1.png"))
        for i in range(2):
            self.textures.append(arcade.load_texture("tree2.png"))
        for i in range(2):
            self.textures.append(arcade.load_texture("tree3.png"))

    def update(self):
        super().update()
        fire_peas = arcade.check_for_collision_with_list(self, get_window().peas)
        for pea in fire_peas:
            pea.texture = arcade.load_texture("firebul.png")
            pea.damage = 3

