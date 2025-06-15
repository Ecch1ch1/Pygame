import pygame
import sys
import math
import os

# --- Základní nastavení ---
TILE_SIZE = 48
GRID_WIDTH, GRID_HEIGHT = 15, 12
INFO_PANEL_WIDTH = 200
SCREEN_WIDTH = GRID_WIDTH * TILE_SIZE + INFO_PANEL_WIDTH
SCREEN_HEIGHT = GRID_HEIGHT * TILE_SIZE
FPS = 60
GAME_TITLE = "Světelný Mechanik"

# --- Barvy ---
WHITE = (255, 255, 255); BLACK = (0, 0, 0); RED = (255, 50, 50)
GREY = (40, 40, 40); DARK_GREY = (25, 25, 25); CYAN = (0, 255, 255); GREEN = (50, 200, 50)
BUTTON_COLOR = (70, 70, 90); BUTTON_HOVER_COLOR = (100, 100, 120)
LOCKED_BUTTON_COLOR = (50, 50, 50)

### ZMĚNA: Rozšíření na 20 levelů s postupnou obtížností ###
LEVELS = [
    # 1-5: Základy
    {"layout": [ "WWWWWWWWWWWWWWW", "W             W", "W S         T W", "W             W", "W             W", "W             W", "W             W", "W             W", "W             W", "W             W", "W             W", "WWWWWWWWWWWWWWW" ], "mirrors": 1},
    {"layout": [ "WWWWWWWWWWWWWWW", "W             W", "W S           W", "W             W", "W           T W", "W             W", "W             W", "W             W", "W             W", "W             W", "W             W", "WWWWWWWWWWWWWWW" ], "mirrors": 1},
    {"layout": [ "WWWWWWWWWWWWWWW", "W             W", "W S   WWWW    W", "W     W  W    W", "W     W  W  T W", "W     W  W    W", "W     WWWW    W", "W             W", "W             W", "W             W", "W             W", "WWWWWWWWWWWWWWW" ], "mirrors": 2},
    {"layout": [ "WWWWWWWWWWWWWWW", "W T           W", "W             W", "W      S      W", "W             W", "W T           W", "W             W", "W             W", "W             W", "W             W", "W             W", "WWWWWWWWWWWWWWW" ], "mirrors": 2},
    {"layout": [ "WWWWWWWWWWWWWWW", "W S           W", "W             W", "W           M W", "W             W", "W             W", "W T           W", "W             W", "W             W", "W             W", "W             W", "WWWWWWWWWWWWWWW" ], "mirrors": 1},
    # 6-10: Střední obtížnost
    {"layout": [ "WWWWWWWWWWWWWWW", "W           T W", "W WWW WWWWW WWW", "W W W W   W W W", "W W W W S W W W", "W W W WWWWW W W", "W W W       W W", "W WWWWWWWWWWW W", "W             W", "W             W", "W             W", "WWWWWWWWWWWWWWW" ], "mirrors": 3},
    {"layout": [ "WWWWWWWWWWWWWWW", "WS            W", "WWWWWWWWWWWWW W", "W             W", "W WWWWWWWWWWWWW", "W W         T W", "W WWWWWWWWWWWWW", "W             W", "WWWWWWWWWWWWW W", "W             W", "W             W", "WWWWWWWWWWWWWWW" ], "mirrors": 4},
    {"layout": [ "WWWWWWWWWWWWWWW", "W S         W W", "W W         W W", "W W         W W", "W W WWWWWWWWW W", "W W           W", "W WWWWWWWWW   W", "W W       W   W", "W W       W T W", "W W       W   W", "W WWWWWWWWWWWWW", "WWWWWWWWWWWWWWW" ], "mirrors": 5},
    {"layout": [ "WWWWWWWWWWWWWWW", "W S         T W", "W WWWWWWWWWWW W", "W W           W", "W W T         W", "W W           W", "W WWWWWWWWWWW W", "W             W", "W             W", "W             W", "W             W", "WWWWWWWWWWWWWWW" ], "mirrors": 2},
    {"layout": [ "WWWWWWWWWWWWWWW", "W T W   S   W W", "W W W WWWWW W W", "W W W W     W W", "W W   W     W W", "W WWWWW     W W", "W   W       W W", "W W W       W W", "W W WWWWWWWWW W", "W W         T W", "W             W", "WWWWWWWWWWWWWWW" ], "mirrors": 4},
    # 11-15: Pokročilé hádanky
    {"layout": [ "WWWWWWWWWWWWWWW", "W S M       T W", "W W W W W W W W", "W  M M M M M  W", "W W W W W W W W", "W M M M M M M W", "W W W W W W W W", "W  M M M M M  W", "W W W W W W W W", "W M M M M M M W", "W             W", "WWWWWWWWWWWWWWW" ], "mirrors": 0},
    {"layout": [ "WWWWWWWWWWWWWWW", "W S         W T", "W W           W", "W WWWWWWWWWWWWW", "W             W", "WWWWWWWWWWWWW W", "W           W W", "W           W W", "W           W W", "W           W W", "W             W", "WWWWWWWWWWWWWWW" ], "mirrors": 3},
    {"layout": [ "WWWWWWWWWWWWWWW", "WS T          W", "W W           W", "W WWWWWWWWWWWWWW", "W            W", "WWWWWWWWWWWW W", "W            W", "W WWWWWWWWWW W", "W            W", "W WWWWWWWWWW W", "W T          W", "WWWWWWWWWWWWWWW" ], "mirrors": 6},
    {"layout": [ "WWWWWWWWWWWWWWW", "W T         T W", "W             W", "W      S      W", "W             W", "W T         T W", "W             W", "W             W", "W             W", "W             W", "W             W", "WWWWWWWWWWWWWWW" ], "mirrors": 4},
    {"layout": [ "WWWWWWWWWWWWWWW", "W     W       W", "W T W W S W T W", "W W W W W W W W", "W W W W W W W W", "W     W       W", "W     W       W", "W W W W W W W W", "W W W W W W W W", "W T W W W W T W", "W     W       W", "WWWWWWWWWWWWWWW" ], "mirrors": 8},
    # 16-20: Expertní levely
    {"layout": [ "WWWWWWWWWWWWWWW", "WS    W    M  W", "W WWW W WWWWW W", "W   W W W   W W", "WWW W W W W WWW", "W T W W W W   W", "W WWW W WWW WWW", "W W   W W W   W", "W WWWWW W WWWWW", "W      T      W", "W             W", "WWWWWWWWWWWWWWW" ], "mirrors": 3},
    {"layout": [ "WWWWWWWWWWWWWWW", "W S         T W", "W M M M M M M W", "W             W", "W M M M M M M W", "W             W", "W M M M M M M W", "W             W", "W M M M M M M W", "W             W", "W             W", "WWWWWWWWWWWWWWW" ], "mirrors": 0},
    {"layout": [ "WWWWWWWWWWWWWWW", "W S W W W W W W", "W   W   W T   W", "W WWWWWWWWWWWWW", "W             W", "WWWWWWWWWWWWW W", "W           W W", "W WWWWWWWWWWW W", "W W           W", "W W WWWWWWWWWWW", "W   T         W", "WWWWWWWWWWWWWWW" ], "mirrors": 6},
    {"layout": [ "WWWWWWWWWWWWWWW", "W T         W W", "WWWWWWWWWWW W W", "W S         W W", "W WWWWWWWWWWW W", "W W         W W", "W W WWWWWWWWWWW", "W W         T W", "W WWWWWWWWWWW W", "W W           W", "W W           W", "WWWWWWWWWWWWWWW" ], "mirrors": 5},
    {"layout": [ "WWWWWWWWWWWWWWW", "WS M M M M M MTW", "W             W", "W M M M M M M M W", "W             W", "W M M M M M M M W", "W             W", "W M M M M M M M W", "W             W", "W M M M M M M M W", "W             W", "WWWWWWWWWWWWWWW" ], "mirrors": 0},
]

class Spritesheet:
    def __init__(self, filename):
        try: self.sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error: print(f"Varování: Spritesheet '{filename}' nenalezen."); self.sheet = None
    def get_image(self, x, y, width, height):
        if self.sheet is None:
            image = pygame.Surface((width, height)); image.fill(RED); return image
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), (x, y, width, height))
        return image

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y): super().__init__(); self.image = pygame.image.load('wall.png').convert_alpha(); self.rect = self.image.get_rect(topleft=(x, y))
class LaserSource(pygame.sprite.Sprite):
    def __init__(self, x, y, direction): super().__init__(); self.image = pygame.image.load('laser_source.png').convert_alpha(); self.rect = self.image.get_rect(topleft=(x, y)); self.direction = pygame.math.Vector2(direction)
class Target(pygame.sprite.Sprite):
    def __init__(self, x, y, spritesheet):
        super().__init__(); self.spritesheet = spritesheet; self.img_off = self.spritesheet.get_image(0, 0, TILE_SIZE, TILE_SIZE); self.img_on = self.spritesheet.get_image(TILE_SIZE, 0, TILE_SIZE, TILE_SIZE); self.image = self.img_off; self.rect = self.image.get_rect(topleft=(x, y)); self.is_lit = False
    def light_up(self, lit, game):
        was_lit = self.is_lit; self.is_lit = lit; self.image = self.img_on if self.is_lit else self.img_off
        if self.is_lit and not was_lit and game.target_lit_sound: game.target_lit_sound.play()
class Mirror(pygame.sprite.Sprite):
    def __init__(self, x, y, placeable=False):
        super().__init__(); self.original_image = pygame.image.load('mirror.png').convert_alpha(); self.image = self.original_image; self.rect = self.image.get_rect(topleft=(x, y)); self.placeable = placeable; self.orientation = 0; self.angle = 0
    def rotate(self):
        self.orientation = (self.orientation + 1) % 4; self.angle -= 90; center = self.rect.center; self.image = pygame.transform.rotate(self.original_image, self.angle); self.rect = self.image.get_rect(center=center)

class Game:
    def __init__(self):
        pygame.init(); pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 28)
        self.level_select_font = pygame.font.Font(None, 48)
        self.state = 'main_menu'
        self.load_assets()
        self.load_progress() # Načtení postupu při startu

    def load_assets(self):
        try: self.mirror_icon = pygame.transform.scale(pygame.image.load('mirror.png').convert_alpha(), (32, 32))
        except pygame.error: self.mirror_icon = pygame.Surface((32,32)); self.mirror_icon.fill(CYAN)
        self.target_spritesheet = Spritesheet('target_spritesheet.png')
        try: pygame.mixer.music.load('menu_music.mp3'); self.menu_music_loaded = True
        except pygame.error: self.menu_music_loaded = False; print("Varování: 'menu_music.mp3' nenalezen.")
        try: pygame.mixer.music.load('game_music.mp3'); self.game_music_loaded = True
        except pygame.error: self.game_music_loaded = False; print("Varování: 'game_music.mp3' nenalezen.")
        self.laser_start_sound = self.load_sound('laser_start.wav'); self.mirror_hit_sound = self.load_sound('mirror_hit.wav')
        self.target_lit_sound = self.load_sound('target_lit.wav'); self.victory_sound = self.load_sound('victory.wav')

    def load_sound(self, filename):
        try: return pygame.mixer.Sound(filename)
        except pygame.error: print(f"Varování: Zvuk '{filename}' nenalezen."); return None

    ### ZMĚNA: Nové metody pro ukládání a načítání postupu ###
    def load_progress(self):
        try:
            with open('progress.txt', 'r') as f:
                self.highest_unlocked_level = int(f.read())
        except (FileNotFoundError, ValueError):
            self.highest_unlocked_level = 1 # Pokud soubor neexistuje, je odemčen jen level 1

    def save_progress(self):
        with open('progress.txt', 'w') as f:
            f.write(str(self.highest_unlocked_level))

    def play_music(self, track):
        # ... (beze změny)
        pass # Kód pro hudbu zůstává stejný

    def load_level(self, level_index):
        # ... (beze změny)
        pass # Kód pro načtení levelu zůstává stejný

    def check_level_completion(self):
        if not self.level_complete and self.targets and all(target.is_lit for target in self.targets):
            self.level_complete = True
            if self.victory_sound: self.victory_sound.play()
            # Odemčení dalšího levelu
            next_level = self.current_level_index + 2
            if next_level > self.highest_unlocked_level:
                self.highest_unlocked_level = next_level
                self.save_progress()

    def run(self):
        self.running = True
        while self.running:
            if self.state == 'main_menu': self.main_menu_loop()
            elif self.state == 'level_select': self.level_select_loop()
            elif self.state == 'in_game': self.game_loop()
        pygame.quit(); sys.exit()
    
    # ... zbytek kódu ...
    def main_menu_loop(self):
        self.play_music('menu')
        
        # Vytvoření tlačítek
        continue_button = pygame.Rect(SCREEN_WIDTH/2 - 150, SCREEN_HEIGHT/2 - 60, 300, 50)
        select_button = pygame.Rect(SCREEN_WIDTH/2 - 150, SCREEN_HEIGHT/2, 300, 50)
        quit_button = pygame.Rect(SCREEN_WIDTH/2 - 150, SCREEN_HEIGHT/2 + 60, 300, 50)
        
        while self.state == 'main_menu':
            self.screen.fill(DARK_GREY)
            title_surf = pygame.font.Font(None, 72).render(GAME_TITLE, True, WHITE)
            self.screen.blit(title_surf, title_surf.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/4)))
            
            mouse_pos = pygame.mouse.get_pos()
            
            # Tlačítko Pokračovat
            pygame.draw.rect(self.screen, BUTTON_HOVER_COLOR if continue_button.collidepoint(mouse_pos) else BUTTON_COLOR, continue_button)
            continue_text = self.font.render("Pokračovat", True, WHITE)
            self.screen.blit(continue_text, continue_text.get_rect(center=continue_button.center))

            # Tlačítko Výběr úrovně
            pygame.draw.rect(self.screen, BUTTON_HOVER_COLOR if select_button.collidepoint(mouse_pos) else BUTTON_COLOR, select_button)
            select_text = self.font.render("Výběr úrovně", True, WHITE)
            self.screen.blit(select_text, select_text.get_rect(center=select_button.center))

            # Tlačítko Konec
            pygame.draw.rect(self.screen, BUTTON_HOVER_COLOR if quit_button.collidepoint(mouse_pos) else BUTTON_COLOR, quit_button)
            quit_text = self.font.render("Konec", True, WHITE)
            self.screen.blit(quit_text, quit_text.get_rect(center=quit_button.center))

            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.running = False; self.state = 'quit'
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if continue_button.collidepoint(mouse_pos):
                        self.current_level_index = min(self.highest_unlocked_level - 1, len(LEVELS) - 1)
                        self.state = 'in_game'
                        self.load_level(self.current_level_index)
                    if select_button.collidepoint(mouse_pos):
                        self.state = 'level_select'
                    if quit_button.collidepoint(mouse_pos):
                        self.running = False; self.state = 'quit'
            
            pygame.display.flip(); self.clock.tick(FPS)
    
    ### ZMĚNA: Nová metoda pro obrazovku výběru levelů ###
    def level_select_loop(self):
        cols, rows = 5, 4
        btn_width, btn_height = 100, 100
        spacing = 20
        start_x = (SCREEN_WIDTH - (cols * btn_width + (cols - 1) * spacing)) / 2
        start_y = (SCREEN_HEIGHT - (rows * btn_height + (rows - 1) * spacing)) / 2
        
        level_buttons = []
        for i in range(len(LEVELS)):
            row = i // cols
            col = i % cols
            x = start_x + col * (btn_width + spacing)
            y = start_y + row * (btn_height + spacing)
            level_buttons.append(pygame.Rect(x, y, btn_width, btn_height))

        back_button = pygame.Rect(20, SCREEN_HEIGHT - 70, 150, 50)

        while self.state == 'level_select':
            self.screen.fill(DARK_GREY)
            title_surf = self.font.render("Výběr úrovně", True, WHITE)
            self.screen.blit(title_surf, title_surf.get_rect(center=(SCREEN_WIDTH/2, 50)))

            mouse_pos = pygame.mouse.get_pos()

            for i, rect in enumerate(level_buttons):
                is_unlocked = (i + 1) <= self.highest_unlocked_level
                color = LOCKED_BUTTON_COLOR
                if is_unlocked:
                    color = BUTTON_HOVER_COLOR if rect.collidepoint(mouse_pos) else BUTTON_COLOR
                
                pygame.draw.rect(self.screen, color, rect)
                level_num_surf = self.level_select_font.render(str(i + 1), True, WHITE if is_unlocked else GREY)
                self.screen.blit(level_num_surf, level_num_surf.get_rect(center=rect.center))

            # Tlačítko Zpět
            pygame.draw.rect(self.screen, BUTTON_HOVER_COLOR if back_button.collidepoint(mouse_pos) else BUTTON_COLOR, back_button)
            back_text = self.font.render("Zpět", True, WHITE)
            self.screen.blit(back_text, back_text.get_rect(center=back_button.center))

            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.running = False; self.state = 'quit'
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if back_button.collidepoint(mouse_pos):
                        self.state = 'main_menu'
                    for i, rect in enumerate(level_buttons):
                        if rect.collidepoint(mouse_pos) and (i + 1) <= self.highest_unlocked_level:
                            self.current_level_index = i
                            self.state = 'in_game'
                            self.load_level(i)

            pygame.display.flip()
            self.clock.tick(FPS)
            
    # Ostatní metody (game_loop, events, update, draw, atd.) jsou zde pro kompletnost,
    # ale jejich vnitřní logika zůstává téměř stejná jako v minulé verzi.
    # Následující kód je upraven pro práci s novou strukturou stavů.

    def game_loop(self):
        # Tato smyčka nyní běží, dokud se nezmění stav (např. na 'main_menu')
        while self.state == 'in_game':
            self.events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False; self.state = 'quit'
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                # Klik na tlačítko "Další level"
                if self.level_complete:
                    if hasattr(self, 'next_level_button_rect') and self.next_level_button_rect.collidepoint(pos):
                        self.current_level_index += 1
                        if self.current_level_index < len(LEVELS):
                            self.load_level(self.current_level_index)
                        else: # Konec hry
                            self.state = 'main_menu'
                    return

                # Klik na herní tlačítka v info panelu
                panel_x_start = GRID_WIDTH * TILE_SIZE
                if pos[0] > panel_x_start:
                    if self.start_button_rect.collidepoint(pos) and self.tries_left > 0:
                        self.tries_left -= 1
                        self.laser_is_on = True
                        self.laser_on_time = pygame.time.get_ticks()
                        if self.laser_start_sound: self.laser_start_sound.play()
                        self.calculate_laser_path()
                    if self.reset_button_rect.collidepoint(pos):
                        self.load_level(self.current_level_index)
                    return
                
                # Interakce v herní ploše
                grid_x, grid_y = pos[0] // TILE_SIZE, pos[1] // TILE_SIZE
                clicked_sprite = next((s for s in self.all_sprites if s.rect.collidepoint(pos)), None)
                if event.button == 1:
                    if clicked_sprite is None and self.placeable_mirrors_count > 0:
                        self.all_sprites.add(Mirror(grid_x * TILE_SIZE, grid_y * TILE_SIZE, True)); self.placeable_mirrors_count -= 1
                elif event.button == 3:
                    if isinstance(clicked_sprite, Mirror): clicked_sprite.rotate()
    
    # ... zbytek metod (update, draw, atd.) ...
    def update(self):
        if self.laser_is_on:
            now = pygame.time.get_ticks()
            if now - self.laser_on_time > self.laser_duration:
                if not self.level_complete: # Pokud není vyhráno, laser zhasne
                    self.laser_is_on = False
                    self.laser_path = []
                    for target in self.targets: target.light_up(False, self)
        
        if self.laser_is_on:
            self.check_level_completion()

    def draw(self):
        self.screen.fill(BLACK)
        for x in range(GRID_WIDTH + 1): pygame.draw.line(self.screen, GREY, (x * TILE_SIZE, 0), (x * TILE_SIZE, SCREEN_HEIGHT))
        for y in range(GRID_HEIGHT + 1): pygame.draw.line(self.screen, GREY, (0, y * TILE_SIZE), (GRID_WIDTH * TILE_SIZE, y * TILE_SIZE))
        self.all_sprites.draw(self.screen)
        if self.laser_is_on: self.draw_laser()
        self.draw_info_panel()
        pygame.display.flip()
        
    def draw_laser(self):
        if len(self.laser_path) > 1:
            pulse = (math.sin(pygame.time.get_ticks() * 0.01) + 1) / 2
            color = (255, int(100 + 155 * pulse), int(100 + 155 * pulse))
            pygame.draw.lines(self.screen, color, False, self.laser_path, 5)

    def draw_info_panel(self):
        panel_rect = pygame.Rect(GRID_WIDTH * TILE_SIZE, 0, INFO_PANEL_WIDTH, SCREEN_HEIGHT)
        pygame.draw.rect(self.screen, DARK_GREY, panel_rect)
        level_text = self.font.render(f"Level {self.current_level_index + 1}", True, WHITE)
        self.screen.blit(level_text, (panel_rect.x + 20, 20))
        inventory_text = self.small_font.render("Inventář:", True, WHITE)
        self.screen.blit(inventory_text, (panel_rect.x + 20, 80))
        self.screen.blit(self.mirror_icon, (panel_rect.x + 20, 110))
        count_text = self.font.render(f"x {self.placeable_mirrors_count}", True, WHITE)
        self.screen.blit(count_text, (panel_rect.x + 70, 115))
        tries_text = self.font.render(f"Pokusy: {self.tries_left}", True, WHITE)
        self.screen.blit(tries_text, (panel_rect.x + 20, 180))
        mouse_pos = pygame.mouse.get_pos()
        self.start_button_rect = pygame.Rect(panel_rect.x + 20, 250, 160, 50)
        self.reset_button_rect = pygame.Rect(panel_rect.x + 20, 320, 160, 50)
        start_color = BUTTON_HOVER_COLOR if self.start_button_rect.collidepoint(mouse_pos) and self.tries_left > 0 else BUTTON_COLOR if self.tries_left > 0 else LOCKED_BUTTON_COLOR
        pygame.draw.rect(self.screen, start_color, self.start_button_rect)
        start_text_surf = self.small_font.render("SPUSTIT LASER", True, WHITE)
        self.screen.blit(start_text_surf, start_text_surf.get_rect(center=self.start_button_rect.center))
        reset_color = BUTTON_HOVER_COLOR if self.reset_button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(self.screen, reset_color, self.reset_button_rect)
        reset_text_surf = self.small_font.render("RESTART", True, WHITE)
        self.screen.blit(reset_text_surf, reset_text_surf.get_rect(center=self.reset_button_rect.center))
        if self.tries_left == 0 and not self.level_complete:
            lose_text = self.font.render("Došly pokusy!", True, RED); self.screen.blit(lose_text, (panel_rect.x + 20, 400))
        if self.level_complete:
            msg_text = "Level splněn!" if self.current_level_index + 1 < len(LEVELS) else "Gratulace!"; button_text = "Další level" if self.current_level_index + 1 < len(LEVELS) else "Do menu"
            msg_surf = self.font.render(msg_text, True, GREEN); self.screen.blit(msg_surf, (panel_rect.x + 20, 450))
            self.next_level_button_rect = pygame.Rect(panel_rect.x + 20, 500, 160, 50)
            pygame.draw.rect(self.screen, GREEN, self.next_level_button_rect)
            btn_surf = self.small_font.render(button_text, True, BLACK); btn_rect = btn_surf.get_rect(center=self.next_level_button_rect.center)
            self.screen.blit(btn_surf, btn_rect)

if __name__ == '__main__':
    # Tato část je nyní jednodušší, protože vše řídí hlavní smyčka ve třídě Game
    game = Game()
    game.run()