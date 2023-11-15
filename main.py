#-----------------------------------#
#  SPACESHOOTER by Nicolas Finesso  #
#-----------------------------------#

import game_manager

# Libraries ref
GM = game_manager.GameManager()
GO = game_manager.game_objects
pygame = GO.pygame

# Font parameters
pygame.display.set_caption("*** Space Shooter ***")
pygame.font.init()
MAIN_FONT = pygame.font.SysFont("MS Gothic", 50)
GAMEOVER_FONT = pygame.font.SysFont("MS Gothic", 100)

# Game window parameters
BG = GM.background
WIDTH = BG.width
HEIGHT = BG.height
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

FPS = 60

# Game actors
PLAYER = GM.player

# GAME FUNCTIONS
def draw_window(scroll):
    # Draw background
    WIN.blit(BG.sprite, (scroll, 0))
    WIN.blit(BG.sprite, (scroll + BG.sprite.get_width(), 0))
    WIN.blit(PLAYER.sprite, (PLAYER.rect.x, PLAYER.rect.y))
    # Draw actors
    for enemy in GM.enemys:
        enemy.draw(WIN)
    for proj in GM.enemy_projs:
        proj.draw(WIN)
    for proj in GM.player_projs:
        proj.draw(WIN)
    PLAYER.draw(WIN)
    # Draw text
    score_label = MAIN_FONT.render(f"Score: {GM.score}", 1, (255, 255, 255))
    WIN.blit(score_label, (10, 10))

    pygame.display.update()

def draw_gameover():
    lbl = GAMEOVER_FONT.render("GAME OVER", 1, (255, 255, 255))
    WIN.blit(lbl, (WIDTH/2 - lbl.get_width() /
             2, HEIGHT/2 - lbl.get_height()/2))

    pygame.display.update()


# PLAYER FUNCTIONS
def player_actions(key):
    if key[pygame.K_q] and PLAYER.rect.x > 0:
        PLAYER.rect.x -= PLAYER.speed
    if key[pygame.K_d] and PLAYER.rect.x + PLAYER.rect.width < WIDTH:
        PLAYER.rect.x += PLAYER.speed
    if key[pygame.K_z] and PLAYER.rect.y > 0:
        PLAYER.rect.y -= PLAYER.speed
    if key[pygame.K_s] and PLAYER.rect.y + PLAYER.rect.height < HEIGHT:
        PLAYER.rect.y += PLAYER.speed
    if key[pygame.K_SPACE]:
        GM.enemy_spawn_0.spawn_object()


# GAME LOOP
def main():
    clock = pygame.time.Clock()
    run = True
    scroll = 0

    while run:
        clock.tick(FPS)
        # Check when user quit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Scroll background and draw text on screen
        draw_window(scroll)
        scroll -= BG.scroll_speed
        if abs(scroll) > BG.sprite.get_width():
            scroll = 0

        # Check if player alive
        if not PLAYER.dead():
            # Read Player controls
            keys_pressed = pygame.key.get_pressed()
            player_actions(keys_pressed)
            # Update all game actors
            PLAYER.update()
            GM.update()
        else:
            draw_gameover()
        # Quit game
    pygame.quit()


# Run if lunch as main file
if __name__ == "__main__":
    main()
