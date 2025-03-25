import pygame
import sys
import random
import time
# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Mario')

# Clock for FPS control
clock = pygame.time.Clock()

# Load background
bg = pygame.image.load("mario.png")  # Replace with your background image
bgw, bgh = bg.get_width(), bg.get_height()
scroll = 0
speed = 0
life = 5
# Gravity variables
gravity = 0.5
jump_strength = -15
ground_level = 400
upadate_wall = True
# Mario character properties
cx, cy = 100, ground_level  # Position
velocity_y = 0  # Jump speed
is_jumping = False  # Jump state
walking = 0

music = pygame.mixer.music.load("bg_music.mp3")  # Replace with your music file
music_playing = True  # Music initially off
sound_playing = True

coin_sound = pygame.mixer.Sound("coin.wav")
box_sound = pygame.mixer.Sound("box.wav")
jump_sound = pygame.mixer.Sound("jump.wav")
# Button settings
def write_me(screen, text, font_size, Color, position):
    font = pygame.Font(None, font_size)
    text = font.render(text, True, Color)
    screen.blit(text, position)


def toggle_music():
    global music_playing, button_color
    if music_playing:
        pygame.mixer.music.stop()
        music_playing = False
        button_color = (255, 0, 0)  # Red for OFF
    else:
        pygame.mixer.music.play(-1)  # Loop indefinitely
        music_playing = True
        button_color = (0, 255, 0)  # Green for ON

def try_again(screen):
    running = True
    while running:
        mx, my = pygame.mouse.get_pos()
        

        screen.fill((255, 255, 255, 128))

        pygame.draw.rect(screen, (30, 30, 30), (WIDTH//2-60, HEIGHT//2-15, 120, 30), width=0,border_radius=2)
        text = "GAME OVER"
        font = pygame.Font(None, 40)
        text = font.render(text, True, (30, 30, 100))
        screen.blit(text, (WIDTH//2-text.get_width()//2, HEIGHT//2- text.get_height()//2- 30))
        font = pygame.Font(None, 24)
        text = font.render("Try Again", True, (255, 255, 255))
        screen.blit(text, (WIDTH//2-text.get_width()//2, HEIGHT//2- text.get_height()//2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                    if mx in range(340, 460 ) and my in range(285, 315):
                        running = False
                    
     
                

        pygame.display.flip()
        clock.tick(60)

def wait_there(screen):
    start_time = time.time()
    while (time.time()- start_time)< 3:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
        

        screen.fill((255, 255, 255, 128))
        text = "HIT"
        font = pygame.Font(None, 40)
        text = font.render(text, True, (30, 30, 100))
        screen.blit(text, (WIDTH//2-text.get_width()//2, HEIGHT//2- text.get_height()//2- 30))
        font = pygame.Font(None, 24)
        text = font.render("Resuming in 3s", True, (30, 30, 30))
        screen.blit(text, (WIDTH//2-text.get_width()//2, HEIGHT//2- text.get_height()//2))

        pygame.display.flip()
        clock.tick(60)

        



# 🎮 Load Mario sprite sheet
class SpriteSheet:
    def __init__(self, image_path, columns, rows):
        self.sprite_sheet = pygame.image.load(image_path).convert_alpha()
        self.columns = columns
        self.rows = rows
        self.frame_width = self.sprite_sheet.get_width() // columns
        self.frame_height = self.sprite_sheet.get_height() // rows

    def get_frames_from_row(self, row):
        frames = []
        for col in range(self.columns):
            frame_rect = pygame.Rect(col * self.frame_width, row * self.frame_height,
                                     self.frame_width, self.frame_height)
            frame = self.sprite_sheet.subsurface(frame_rect)
            frames.append(frame)
        return frames

class AnimatedSprite:
    def __init__(self, sprite_sheet, row, fps):
        self.frames = sprite_sheet.get_frames_from_row(row)
        self.frame_index = 0
        self.fps = fps
        self.frame_delay = 1000 // fps
        self.last_update_time = pygame.time.get_ticks()

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time > self.frame_delay:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.last_update_time = current_time

    def draw(self, surface, position, reverse=False, box = True):
        img = self.frames[self.frame_index]
        if reverse:
            img = pygame.transform.flip(img, True, False)
        
        mario_rect = pygame.Rect(position[0], position[1], img.get_rect()[2], img.get_rect()[3])
        if box:
            pygame.draw.rect(screen, (255, 0, 0), mario_rect, 3)
        surface.blit(img, position)
        return mario_rect

# Obstacle class
class Obstacle:
    def __init__(self, image, y_position, obs_type):
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = y_position
        self.type = obs_type

    def update(self, speed):
        self.rect.x -= speed
        if self.rect.x < -self.rect.width*10:
            obstacles.remove(self)  # Correct way to remove obstacles
    def remove(self):
        obstacles.remove(self)


    def draw(self, screen):
        screen.blit(self.image, self.rect)
    def get_type_rect(self):
        return self.type, self.rect


def draw_life(screen, life):
    write_me(screen, "LIFE", 20,  (255, 0 , 0),  (WIDTH- 150, 8))
    for i in range(5):
        pygame.draw.circle(screen, (255, 0, 0), (WIDTH-100 + i*20, 15), 5, width = 2 if i>=life else 0)
        

# Load Mario sprite animations
sprite_sheet = SpriteSheet("all_pose-01.png", columns=4, rows=4)
walk = AnimatedSprite(sprite_sheet, row=1, fps=6)  
jump = AnimatedSprite(sprite_sheet, row=2, fps=6)  
mario_standing = pygame.image.load("standing1.png")  

# Obstacle images
small_pillar_img = "pillar_s.png"  
big_pillar_img = "pillar_b.png" 
box = "box.png"
wall = "mid.png"
coin = "coin.png" 
coin_count = 0
all_time_best = 0
b_box = True
# Obstacle list

obstacles = []
obstacle_timer = 0  # Timer to control obstacle spawning
wall_right = 110
min_dis = 90
dis = 0
rs_time = 100

def spwan_obstacle():
    global obstacle_timer, rs_time
    global dis, min_dis, small_pillar_img, big_pillar_img, wall, box, coin
    if obstacle_timer > rs_time and dis > min_dis:  # Add obstacles every 100 frames
        obstacle_type = random.choice(["small", "big", "wall", "box", "coin"])
        if obstacle_type == "small":
            obstacles.append(Obstacle(small_pillar_img, 395, "small"))
            min_dis = 120
            dis = -min_dis+30
        elif obstacle_type == "big":
            obstacles.append(Obstacle(big_pillar_img, 380, "big"))
            dis = -min_dis+30
            min_dis = 120
        elif obstacle_type == "wall":
            obstacles.append(Obstacle(wall, 330, "wall"))
            obstacles.append(Obstacle(coin, 330-random.randint(100, 150), "coin"))
            min_dis = 160
            dis = -min_dis+30
        elif obstacle_type == "box":
            obstacles.append(Obstacle(box, random.randint(250, 340), "box"))
            dis = -min_dis+30
            min_dis = 120
        elif obstacle_type == "coin":
            obstacles.append(Obstacle(coin, random.randint(250, 340),"coin"))
            
            dis = -min_dis+30
            min_dis = 120
        obstacle_timer = 0  
# Game loop
flag_wall = False
update_status = True
running = True
total_dis= 0
while running:
    screen.fill(WHITE)
    mx, my = pygame.mouse.get_pos()

    pygame.draw.rect(screen, (30, 30, 30), (WIDTH-80, 40, 60, 20), border_radius=2)
    text = "MUSIC: ON" if music_playing else "MUSIC: OFF"
    write_me(screen, text, 14, (255, 255, 255),(WIDTH-78, 45) )

    pygame.draw.rect(screen, (200, 200, 200), (WIDTH-80, 65, 60, 20), border_radius=2)
    text = "BOX:ON" if b_box else "BOX:OFF"
    write_me(screen, text, 14, (255, 0, 0), (WIDTH-70, 70))

    pygame.draw.rect(screen, (30, 30, 30), (10, 40, 60, 20), border_radius=2)
    text = "SOUND:ON" if sound_playing else "SOUND:OFF"
    write_me(screen, text, 14, (255, 255, 255),(12, 45) )

    



    if music_playing:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()

    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_SPACE or event.key == pygame.K_UP or  event.key == pygame.K_w) and not is_jumping:
                velocity_y = jump_strength
                is_jumping = True
                if sound_playing:
                    jump_sound.play()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if mx in range(720, 720+ 60) and my in range(40,60):
                music_playing = not music_playing

            if mx in range(720, 720+ 60) and my in range(65, 85):
                b_box = not b_box

            if mx in range(10, 70) and my in range(40, 60):
                sound_playing = not sound_playing
            

    

    # Apply gravity
    velocity_y += gravity
    cy += velocity_y

    if cy >= ground_level:
        cy = ground_level
        velocity_y = 0
        is_jumping = False

    # Mario movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:  
        walking = -1
        scroll += 7
        speed = -7
        dis-=7
        total_dis -=7
    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:  
        walking = 1
        scroll -= 7
        speed = 7
        dis+=7
        total_dis += 7
    else:
        walking = 0
        speed = 0



    # Draw background
    for i in range(-1, WIDTH // bgw + 2):
        screen.blit(bg, (i * bgw + scroll, HEIGHT - bgh))
    font = pygame.Font(None, 24)
    screen.blit(font.render(f"COINS: {coin_count}", True, (100, 100, 100) ), (10, 10))
    screen.blit(font.render(f"BEST SO FAR: {all_time_best}", True, (100, 100, 100) ), (100, 10))

    if scroll <= -bgw:
        scroll += bgw
    elif scroll >= bgw:
        scroll -= bgw

    



    # Draw Mario with animations
    
    if is_jumping:
        jump.update()
        mario_rect = jump.draw(screen, (cx, cy), reverse=(walking < 0), box = b_box)
    elif walking != 0:
        walk.update()
        mario_rect = walk.draw(screen, (cx, cy), reverse=(walking < 0), box= b_box)
    else:
        screen.blit(mario_standing, (cx, cy))
        mario_rect = pygame.Rect(cx, cy, mario_standing.get_width(), mario_standing.get_height())
        

    # 🌟 **Improved Obstacle Spawning Logic**
    obstacle_timer += 1
    
    
    spwan_obstacle()
    # Draw & update obstacles
    for obstacle in obstacles[:]:  
        obstacle.draw(screen)
        obstacle.update(speed)
        obs_type, obs_rect = obstacle.get_type_rect()
        
        
        if mario_rect.colliderect(obs_rect):
            if obs_type == "coin":
                if sound_playing:
                    coin_sound.play()
                coin_count+= 1
                obstacle.remove()
            elif obs_type == "box":
                extra = random.randint(5, 10)
                coin_count += extra
                obstacle.remove()
                if sound_playing:
                    box_sound.play()

            elif obs_type == "small" or obs_type == "big":
                obstacle.remove()
                life-=1
                wait_there(screen)

            elif obs_type == "wall":
                if mario_rect.top >= obs_rect.y- obs_rect.height:
                    obstacle.remove()
                    ground_level = 400
                    life -=1
                    wait_there(screen)
                elif mario_rect.bottom >= obs_rect.top:
                    flag_wall = True
                    ground_level = obs_rect.top - mario_rect.height+5
                    if update_status:
                        dis_now = total_dis
                        req_dis_r = obs_rect.width- 100+ obs_rect.x
                        req_dis_l = mario_rect.x - obs_rect.x + mario_rect.width/1.5
                        update_status = False

                

                
    if flag_wall:
        if total_dis>dis_now+req_dis_r or total_dis < dis_now- req_dis_l:
            flag_wall = False
            ground_level = 400
            update_status = True

    if b_box:
        pygame.draw.rect(screen, (255, 0, 0),mario_rect, 3)

    if total_dis>10000:
        total_dis = 0
        if rs_time<10:
            rs_time = 10
        else:
            rs_time = rs_time//1.5
        
    
    if life<1:
        try_again(screen)
        life = 5
        all_time_best = coin_count if all_time_best< coin_count else all_time_best
        coin_count = 0
    draw_life(screen, life)

    

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
