
import pygame
import random
import pygame_menu
pygame.init()

WIDTH, HEIGHT = 400, 600
PIPE_GAP = 200
score = 0
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FLAPPi BIRDZ")

font = pygame.font.Font(None,36)
def draw_score():
    text=font.render(f"Score:{int(score)}  ",True,'red')
    SCREEN.blit(text,(10,10))

def show_start_screen():
    menu=pygame_menu.Menu('меню',300,400,theme=pygame_menu.themes.THEME_DARK)
    menu.add.button("играть", main)
    menu.add.button(" выход",pygame_menu.events.EXIT)
    menu.mainloop(SCREEN)
def show_end_screen():
    menu=pygame_menu.Menu(' меню',300,400,theme=pygame_menu.themes.THEME_DARK)
    menu.add.label(f"Score:{int(score)}", font_size = 30)
    menu.add.button("заново", main)
    menu.add.button(" выход",pygame_menu.events.EXIT)
    menu.mainloop(SCREEN)
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('bird.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center = (WIDTH // 4, HEIGHT // 2))
        self.speed = 0
        self.acceleration =1
    def draw(self):
        SCREEN.blit(self.image, self.rect)
    def update(self):
        self.rect.y += self.speed
        self.speed += self.acceleration
        if self.rect.top < 0:
            self.rect.top =0
            self.speed =0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.speed =0
    def jump(self):
        self.speed= -10
class Pipe(pygame.sprite.Sprite):
    def __init__(self, type,start):
        super().__init__()
        self.image=pygame.image.load("pipe.png")
        self.image = pygame.transform.scale(self.image, (80, self.image.get_height()//2))
        self.passed=False
        if type == "TOP":
            self.image=pygame.transform.flip(self.image,False,True)
            self.rect=self.image.get_rect(bottomleft=(WIDTH,start))
        elif type =="BOTTOM":
            self.rect = self.image.get_rect(topleft=(WIDTH, start+PIPE_GAP))
    def update(self):
        self.rect.x-=5
        if self.rect.right<0:
            self.kill()

pipes = pygame.sprite.Group()
def make_pipes():
    start = random.randint(50, HEIGHT - PIPE_GAP - 50 )
    pipes.add(Pipe('TOP', start), Pipe("BOTTOM", start))
clock = pygame.time.Clock()

def main():
    global score
    bird = Bird()
    bird.rect.center = (WIDTH// 4, HEIGHT // 2)
    bird.speed= 0
    score = 0
    pipes.empty()
    make_pipes()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        bird.update()
        pipes.update()
        if pipes.sprites()[-1].rect.x <= WIDTH / 2:
            make_pipes()
        collisions = pygame.sprite.spritecollide(bird, pipes, False)
        if collisions:
            show_end_screen()
        for pipe in pipes:
            if pipe.rect.right < bird.rect.left and not pipe.passed:
                pipe.passed = True
                score += 0.5

        SCREEN.fill('light blue')
        bird.draw()
        pipes.draw(SCREEN)
        draw_score()
        pygame.display.update()
        clock.tick(30)

show_start_screen()










