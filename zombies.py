import arcade
import time
import random
from arcade.window_commands import get_window, get_display_size


class Zombie(arcade.AnimatedTimeSprite):
    def __init__(self, health, line):
        self.SCREEN_WIDTH = 1000
        super().__init__(0.09)
        self.health = health
        self.line = line
        self.center_x = self.SCREEN_WIDTH
        self.change_x = 0.2

    def update(self):
        self.center_x -= self.change_x
        if self.health <= 0:
            self.kill()
            get_window().score += 1
            get_window().attack_time -= 0.3
        eating = False
        food = arcade.check_for_collision_with_list(self, get_window().plants)
        for plant in food:
            if self.line == plant.line:
                plant.health -= 0.5
                eating = True
        if eating:
            self.change_x = 0
            self.angle = 15
        else:
            self.change_x = 0.2
            self.angle = 0
        if self.center_x <= 250:
            get_window().game = False


class OrdinaryZombie(Zombie):
    def __init__(self, line):
        super().__init__(12, line)
        self.texture = arcade.load_texture("zom1.png")
        for i in range(5):
            self.textures.append(arcade.load_texture("zom1.png"))
        self.textures.append(arcade.load_texture("zom2.png"))


class ConeheadZombie(Zombie):
    def __init__(self, line):
        super().__init__(20, line)
        self.texture = arcade.load_texture("cone1.png")
        for i in range(5):
            self.textures.append(arcade.load_texture("cone1.png"))
        self.textures.append(arcade.load_texture("cone2.png"))


class BuckheadZombie(Zombie):
    def __init__(self, line):
        super().__init__(32, line)
        self.texture = arcade.load_texture('buck1.png')
        for i in range(5):
            self.textures.append(arcade.load_texture("buck1.png"))
        self.textures.append(arcade.load_texture("buck2.png"))


