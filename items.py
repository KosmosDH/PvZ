import arcade
import time
import random
from arcade.window_commands import get_window


class Sun(arcade.Sprite):
    def __init__(self, position_x, position_y):
        super().__init__("sun.png", 0.12)
        self.center_x = position_x
        self.center_y = position_y
        self.sun_pick = time.time()

    def update(self):
        self.angle += 1
        if time.time() - self.sun_pick >= 5:
            self.kill()


class Pea(arcade.Sprite):
    def __init__(self, position_x, position_y):
        super().__init__("bul.png", 0.12)
        self.center_x = position_x
        self.center_y = position_y
        self.change_x = 7
        self.damage = 1.5
        self.hit_sound = arcade.load_sound("hit.mp3")

    def update(self):
        self.center_x += self.change_x
        if self.center_x > get_window().SCREEN_WIDTH:
            self.kill()
        hits = arcade.check_for_collision_with_list(self, get_window().zombies)
        if len(hits) > 0:
            for zombie in hits:
                zombie.health -= self.damage
                arcade.play_sound(self.hit_sound)
                self.kill()

