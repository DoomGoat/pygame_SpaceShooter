import game_objects

GO = game_objects

# GAME MANAGER


class GameManager:
    def __init__(self):
        self.score = 0
        self.enemys = []
        self.enemy_projs = []
        self.player_projs = []
        # Instantiate game objects
        self.background = GO.Background()
        self.player = GO.Player(self)
        self.enemy_spawn_0 = GO.Spawner(self)

    def on_screen(self, obj):
        return obj.rect.x > -obj.sprite.get_width() and obj.rect.x <= self.background.width

    def collide(self, go1, go2):
        # Check if the 2 game object sprite overlap
        offset_x = go2.rect.x - go1.rect.x
        offset_y = go2.rect.y - go1.rect.y
        return go1.mask.overlap(go2.mask, (offset_x, offset_y))


    # Update game objects
    def update(self):
        self.enemy_spawn_0.update()
        # Manage enemys
        for enemy in reversed(self.enemys):
            enemy.move()
            # On collision with player
            if self.collide(enemy, self.player):
                self.player.take_dmg(enemy.hp)
                enemy.hp = 0
            # Update score on enemy death
            if enemy.dead():
                self.score += enemy.max_hp
            # Destroy enemy if out of screen or if dead
            if not self.on_screen(enemy) or enemy.dead():
                self.enemys.remove(enemy)
            else:
                enemy.update()

        # Manage enemy projectiles
        for proj in reversed(self.enemy_projs):
            proj.move()
            # Destroy projectile if out of screen
            if not self.on_screen(proj):
                self.enemy_projs.remove(proj)
                return
            # On collision with player
            if self.collide(proj, self.player):
                self.player.take_dmg(proj.dmg)
                self.enemy_projs.remove(proj)
        
        # Manage player projectiles
        for proj in reversed(self.player_projs):
            proj.move()
            # Destroy projectile if out of screen
            if not self.on_screen(proj):
                self.player_projs.remove(proj)
                return
            # On collision with an enemy
            for enemy in reversed(self.enemys):
                if self.collide(proj, enemy):
                    enemy.take_dmg(proj.dmg)
                    self.player_projs.remove(proj)
                    return
