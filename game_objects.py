from pathlib import Path
import math
import random
import pygame

# Load assets
class Loader:
    def __init__(self):
        self.imgs = {
            'BG_IMG': self.load_img('SpaceBG.png'),
            'SHIP_0_IMG': self.load_img('SpaceShip0.png'),
            'SHIP_1_IMG': self.load_img('SpaceShip1.png'),
            'PROJECTILE_0_IMG': self.load_img('Projectile0.png')
        }

    def load_img(self, file_name):
        print(f'{file_name} loaded.')
        return pygame.image.load(Path(__file__).parent/'sprites'/file_name)

# Initialise all asstets       
LOADER = Loader()

# Game Classes
class Background:
    def __init__(self):
        BG_IMG = LOADER.imgs['BG_IMG']
        self.width, self.height = 1280, 720 # Screen size
        self.sprite = pygame.transform.scale(BG_IMG, (BG_IMG.get_size()))
        self.scroll_speed = 1


class SpaceShip:
    def __init__(self, gm, img, scale_xy=(1, 1), rot=0, pos=(0, 0)):
        self.sprite = pygame.transform.rotate(
            pygame.transform.scale(img, scale_xy), rot)
        self.mask = pygame.mask.from_surface(self.sprite)
        self.rect = pygame.Rect(pos, scale_xy)
        self.rot = rot
        self.speed = 5
        self.max_hp = 100
        self.hp = self.max_hp
        self.fire_rate = 10
        self.dmg_mult = 1
        self.weapons = []
        self.projectiles = []
        self.last_shoot_time = pygame.time.get_ticks()

    def shoot(self):
        if self.weapons != 0:
            gun_side = self.rect.right if self.rot < 0 else self.rect.x
            gun_pos = (gun_side, self.rect.centery)
            for weapon in self.weapons:
                bullet = weapon(rot=self.rot, pos=gun_pos, dmg_mult=self.dmg_mult)
                self.projectiles.append(bullet)
    
    def take_dmg (self, dmg):
        self.hp -= dmg

    def dead(self):
        return self.hp <= 0

    def draw(self, window):
        window.blit(self.sprite, (self.rect.x, self.rect.y))

    def move(self):
        self.rect.x += self.speed if self.rot < 0 else self.speed * - 1

    def update(self):
        # Shoot
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shoot_time >= 1000 / self.fire_rate:
            self.shoot()
            self.last_shoot_time = current_time


class Player(SpaceShip):
    def __init__(self, gm, img=LOADER.imgs['SHIP_1_IMG'], scale_xy=(80, 80), rot=-90, pos=(0, 0)):
        super().__init__(gm, img, scale_xy, rot, pos)
        self.weapons = [Weapon_0]
        self.projectiles = gm.player_projs


class Enemy(SpaceShip):
    def __init__(self, gm, img=LOADER.imgs['SHIP_1_IMG'], scale_xy=(80, 80), rot=-90, pos=(0, 0)):
        super().__init__(gm, img, scale_xy, rot, pos)
        self.projectiles = gm.enemy_projs

class Enemy_0(Enemy):
    def __init__(self, gm, img=LOADER.imgs['SHIP_0_IMG'], scale_xy=(50, 50), rot=90, pos=(0, 0)):
        super().__init__(gm, img, scale_xy, rot, pos)
        self.speed = 2
        self.max_hp = 10
        self.hp = self.max_hp
        self.fire_rate = random.uniform(0.3, 0.5)    
        self.weapons = [Weapon_1]


class Projectile:
    def __init__(self, img, rot=0, pos=(0, 0), dmg_mult=1):
        self.sprite = pygame.transform.rotate(img, rot)
        self.rect = pygame.Rect(pos, (self.sprite.get_size()))
        self.mask = pygame.mask.from_surface(self.sprite)
        self.rect.y -= self.sprite.get_height() / 2  # Correct y position after spawned
        self.rot = rot
        self.speed = 10
        self.dmg = 2 * dmg_mult

    def move(self):
        self.rect.x += self.speed if self.rot < 0 else self.speed * - 1

    def draw(self, window):
        window.blit(self.sprite, (self.rect.x, self.rect.y))


class Weapon_0(Projectile):
    def __init__(self, img=LOADER.imgs['PROJECTILE_0_IMG'], rot=0, pos=(0, 0), dmg_mult=1):
        super().__init__(img, rot, pos, dmg_mult)


class Weapon_1(Projectile):
    def __init__(self, img=LOADER.imgs['PROJECTILE_0_IMG'], rot=0, pos=(0, 0), dmg_mult=1):
        super().__init__(img, rot, pos, dmg_mult)
        self.speed = 5
        self.dmg = 10


class Spawner:
    def __init__(self, gm):
        self.gm = gm
        self.obj_to_spawn = [Enemy_0]
        self.spawn_interval = 1
        self.spawn_timer = 0
        self.obj_spawned = gm.enemys
        self.score = 0

    def spawn_object(self):
        for obj in self.obj_to_spawn:
            game_obj = obj(self.gm)
            game_obj.rect.y = random.randint(10, self.gm.background.height - 60)
            game_obj.rect.x = self.gm.background.width
            self.obj_spawned.append(game_obj)

    def update(self):
        # Spawn game object
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_timer >= self.spawn_interval * 1000:
            self.spawn_object()
            self.spawn_timer = current_time


class Bonus():
    def __init__(self, img, rot, pos, targets):
        self.sprite = pygame.transform.rotate(img, rot)
        self.rect = pygame.Rect(pos, (self.sprite.get_size()))
        self.mask = pygame.mask.from_surface(self.sprite)
