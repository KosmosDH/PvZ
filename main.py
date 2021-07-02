from plant import *
from zombies import OrdinaryZombie, ConeheadZombie, BuckheadZombie

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Plants VS Zombies"


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.game = True
        self.back = arcade.load_texture("background.jpg")
        self.menu = arcade.load_texture("menu_vertical.png")
        self.end = arcade.load_texture("end.png")
        self.plants = arcade.SpriteList()
        self.seed = None
        self.seed_sound = arcade.load_sound("seed.mp3")
        self.game_sound = arcade.Sound("grasswalk.mp3")
        self.game_sound.play(0.3, pan= 1)
        self.game_sound.play(0.3, pan=-1)
        self.lawns = []
        self.sun = 300
        self.score = 0
        self.spawn_suns = arcade.SpriteList()
        self.peas = arcade.SpriteList()
        self.zombies = arcade.SpriteList()
        self.zombie_spawn = time.time()
        self.attack_time = 20

    # отрисовка
    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.back)
        arcade.draw_texture_rectangle(60, 300, 130, 600, self.menu)
        arcade.draw_text(f"Счёт: {window.score}", 870, 550, arcade.color.BLACK, 30)
        self.plants.draw()
        if self.seed is not None:
            self.seed.draw()
        arcade.draw_text(f"{self.sun}", 30, 490, arcade.color.BROWN, 30)
        self.spawn_suns.draw()
        self.peas.draw()
        self.zombies.draw()
        if not self.game:
            arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.end)

    # игровая логика
    def update(self, delta_time):
        if self.game:
            self.plants.update_animation()
            self.plants.update()
            self.spawn_suns.update()
            self.peas.update()
            self.zombies.update()
            self.zombies.update_animation()
            if time.time() - self.zombie_spawn > self.attack_time and self.score < 50:
                center_y, line = lawn_y(random.randint(30, 520))
                zombie_type = random.randint(1, 3)
                if zombie_type == 1:
                    zombie = OrdinaryZombie(line)
                if zombie_type == 2:
                    zombie = ConeheadZombie(line)
                if zombie_type == 3:
                    zombie = BuckheadZombie(line)
                zombie.center_y = center_y
                self.zombies.append(zombie)
                self.zombie_spawn = time.time()
            if self.score > 53 and len(self.zombies) == 0:
                self.end = arcade.load_texture("logo.png")
                self.game = False

    # нажатить кнопку мыши
    def on_mouse_press(self, x, y, button, modifiers):
        if self.game:
            if 10 < x < 110 and 370 < y < 480:
                self.seed = SunFlower()
            if 10 < x < 110 and 255 < y < 365:
                self.seed = PeaShooter()
            if 10 < x < 110 and 140 < y < 250:
                self.seed = WallNut()
            if 10 < x < 110 and 25 < y < 135:
                self.seed = TorchWood()
            if self.seed is not None:
                self.seed.center_x = x
                self.seed.center_y = y
                self.seed.alpha = 150
            for sun in self.spawn_suns:
                if sun.left < x < sun.right and sun.bottom < y < sun.top:
                    sun.kill()
                    self.sun += 25

    # движение мыши
    def on_mouse_motion(self, x, y, dx, dy):
        if self.seed is not None:
            self.seed.center_x = x
            self.seed.center_y = y

    # отпустить кнопку мыши
    def on_mouse_release(self, x, y, button, modifiers):
        if self.seed is not None and 250 < x < 960 and 30 < y < 526:
            center_x, column = lawn_x(x)
            center_y, line = lawn_y(y)
            cost = self.seed.cost
            if (line, column) not in self.lawns and self.sun >= cost:
                self.lawns.append((line, column))
                self.seed.planting(center_x, center_y, line, column)
                self.seed.alpha = 255
                self.plants.append(self.seed)
                self.seed = None
                self.seed_sound.play()
                self.sun -= cost
            elif self.seed is not None:
                self.seed = None


def lawn_x(x):
    if 250 < x < 326:
        column = 1
        center_x = 283
    elif 326 < x < 400:
        column = 2
        center_x = 360
    elif 400 < x < 485:
        column = 3
        center_x = 440
    elif 485 < x < 560:
        column = 4
        center_x = 520
    elif 560 < x < 640:
        column = 5
        center_x = 600
    elif 640 < x < 715:
        column = 6
        center_x = 675
    elif 715 < x < 785:
        column = 7
        center_x = 750
    elif 785 < x < 870:
        column = 8
        center_x = 830
    elif 870 < x < 960:
        column = 9
        center_x = 915
    return center_x, column


def lawn_y(y):
    if 29 < y < 130:
        line = 1
        center_y = 80
    elif 130 < y < 220:
        line = 2
        center_y = 170
    elif 220 < y < 323:
        line = 3
        center_y = 270
    elif 323 < y < 424:
        line = 4
        center_y = 370
    elif 424 < y < 527:
        line = 5
        center_y = 470
    return center_y, line


window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
arcade.run()
