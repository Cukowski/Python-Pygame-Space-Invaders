import pygame
import random
import pygame.mixer

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("images/game.wav")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)  # The -1 argument makes it loop indefinitely

hit_sound = pygame.mixer.Sound("images/got_hit.wav")
hit_sound.set_volume(0.2)

shoot_sound = pygame.mixer.Sound("images/shoot.wav")
shoot_sound.set_volume(0.2)

game_state = "playing"  # "playing" or "game_over"

window_height = 600
window_width = 800
rows = 3
cols = 10

clock = pygame.time.Clock()
timer = pygame.time.get_ticks()

screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Space Invaders")

background = pygame.image.load("images/background.jpg")

invaders_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
playerBulelt_group = pygame.sprite.Group()
invaderBullet_group = pygame.sprite.Group()


class player_bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/user_bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= 5
        if pygame.sprite.spritecollide(self, invaders_group, True):
            self.kill()


class invader_bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/invader_bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y += 2

        if pygame.sprite.spritecollide(self, player_group, False):
            self.kill()
            player.health_remaning -= 50

            hit_sound.play()


class Invader(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/spaceInvaders.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        # for the movement
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1

        if self.move_counter > 75:
            self.move_direction *= -1
            self.move_counter *= -1


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/user.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.last_shot = pygame.time.get_ticks()
        self.health_start = 50
        self.health_remaning = 50

    def update(self, keys=None):
        speed = 3
        cooldown = 100

        pygame.draw.rect(screen, (0, 0, 0), (self.rect.x,
                         self.rect.bottom, self.rect.width, 10))

        if self.health_remaning > 0:
            pygame.draw.rect(screen, (0, 255, 0), (self.rect.x, self.rect.bottom,
                                                   int(self.rect.width * (self.health_remaning / self.health_start)), 10))
        elif self.health_remaning <= 0:
            self.kill()
            return False  # Player is not alive

        if keys is not None:
            if keys[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= speed

            if keys[pygame.K_RIGHT] and self.rect.right < window_width:
                self.rect.x += speed

            # shoot
            if keys[pygame.K_SPACE] and pygame.time.get_ticks() - self.last_shot > cooldown:
                bullet = player_bullet(self.rect.centerx, self.rect.top)
                playerBulelt_group.add(bullet)
                self.last_shot = pygame.time.get_ticks()

                shoot_sound.play()

        return True  # Player is alive


def create_invader_bullet():
    attacking_invader = random.choice(invaders_group.sprites())
    invaderBullet = invader_bullet(
        attacking_invader.rect.centerx, attacking_invader.rect.centery)
    invaderBullet_group.add(invaderBullet)


def create_invaders():
    for row in range(rows):
        for col in range(cols):
            invader = Invader(100 + col * 65, 80 + row * 50)
            invaders_group.add(invader)


def reset_game():
    global game_state, timer
    game_state = "playing"
    timer = pygame.time.get_ticks()
    player.rect.center = (int(window_width / 2), int(window_height - 100))
    player_group.empty()
    player_group.add(player)
    create_invaders()


# ... (your existing code)

# Initialize player and sprite groups outside the game loop
player = Player(int(window_width / 2,), int(window_height - 100))
player_group.add(player)
create_invaders()

# Load the initial background image
initial_background = pygame.image.load("images/background.jpg")


def reset_game():
    global game_state, reset_timer
    create_invaders()
    player.rect.center = (int(window_width / 2), int(window_height - 100))
    player_group.empty()
    player_group.add(player)
    game_state = "playing"
    reset_timer = 0


game = True
reset_timer = 0  # Variable to track the time after game over
reset_delay = 2000  # Delay in milliseconds before resetting the game

while game:
    clock.tick(60)
    screen.blit(background, (0, 0))

    keys = pygame.key.get_pressed()

    if game_state == "playing":
        if len(invaders_group) == 0:
            game_state = "game_over"
            reset_timer = pygame.time.get_ticks()

        seconds = (pygame.time.get_ticks() - timer) / 1000
        if seconds > 5:
            create_invader_bullet()
            timer = pygame.time.get_ticks()

        invaders_group.update()
        player_group.update(keys)
        invaderBullet_group.update()
        playerBulelt_group.update()

        invaders_group.draw(screen)
        player_group.draw(screen)
        invaderBullet_group.draw(screen)
        playerBulelt_group.draw(screen)

        if not player.update(keys):
            game_state = "game_over"

    elif game_state == "game_over":
        screen.blit(initial_background, (0, 0))

        if pygame.time.get_ticks() - reset_timer > reset_delay:
            background = pygame.image.load("images/gameover_background.jpg")
            screen.blit(background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        reset_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    pygame.display.update()

pygame.quit()
