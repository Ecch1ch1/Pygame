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
LOCKED_BUTTON_COLOR = (50, 50, 50); SELECTED_ITEM_COLOR = (150, 150, 100)

# ===================================================================================
# === ZMĚNA: Přehledná definice levelů pro snadnou editaci ===
# ===================================================================================

LEVEL_1 = {"mirrors": 1, "splitters": 0, "layout": """
WWWWWWWWWWWWWWW
W             W
W S         T W
W             W
W             W
W             W
W             W
W             W
W             W
W             W
W             W
WWWWWWWWWWWWWWW"""}

LEVEL_2 = {"mirrors": 1, "splitters": 0, "layout": """
WWWWWWWWWWWWWWW
W             W
W S           W
W             W
W           T W
W             W
W             W
W             W
W             W
W             W
W             W
WWWWWWWWWWWWWWW"""}

LEVEL_3 = {"mirrors": 3, "splitters": 0, "layout": """
WWWWWWWWWWWWWWW
W             W
W S   WWWW    W
W     W  W    W
W     W  W  T W
W     W  W    W
W     WWWW    W
W             W
W             W
W             W
W             W
WWWWWWWWWWWWWWW"""}

LEVEL_4 = {"mirrors": 2, "splitters": 0, "layout": """
WWWWWWWWWWWWWWW
W T           W
W             W
W      S      W
W             W
W             W
W             W
W             W
W             W
W             W
W             W
WWWWWWWWWWWWWWW"""}

LEVEL_5 = {"mirrors": 2, "splitters": 0, "layout": """
WWWWWWWWWWWWWWW
W S           W
W             W
W           M W
W             W
W             W
W T           W
W             W
W             W
W             W
W             W
WWWWWWWWWWWWWWW"""}

LEVEL_6 = {"mirrors": 4, "splitters": 0, "layout": """
WWWWWWWWWWWWWWW
W           T W
W WWW WWWWW WWW
W W W W   W W W
W W W W S W W W
W W W WWW W W W
W W W       W W
W WWWWWWWWWWW W
W             W
W             W
W             W
WWWWWWWWWWWWWWW"""}

LEVEL_7 = {"mirrors": 4, "splitters": 0, "layout": """
WWWWWWWWWWWWWWW
WS            W
WWWWWWWWWWWWW W
W             W
W WWWWWWWWWWWWW
W           T W
W WWWWWWWWWWWWW
W             W
WWWWWWWWWWWWW W
W             W
W             W
WWWWWWWWWWWWWWW"""}

LEVEL_8 = {"mirrors": 5, "splitters": 0, "layout": """
WWWWWWWWWWWWWWW
W S         W W
W W         W W
W W         W W
W W WWWWWWWWW W
W W           W
W WWWWWWWWW   W
W W       W   W
W W       W T W
W W       W   W
W WWWWWWWWWWWWW
WWWWWWWWWWWWWWW"""}

LEVEL_9 = {"mirrors": 2, "splitters": 0, "layout": """
WWWWWWWWWWWWWWW
W S           W
W WWWWWWWWWWW W
W W           W
W W T         W
W W           W
W WWWWWWWWWWW W
W             W
W             W
W             W
W             W
WWWWWWWWWWWWWWW"""}

LEVEL_10 = {"mirrors": 2, "splitters": 1, "layout": """
WWWWWWWWWWWWWWW
W WTW   S   W W
W W W WWWWW W W
W W W W     W W
W W   W     W W
W W WWW     W W
W   W       W W
W W W       W W
W W WWWWWWW W W
W W         T W
W             W
WWWWWWWWWWWWWWW"""}

LEVEL_11 = {"mirrors": 0, "splitters": 0, "layout": """
WWWWWWWWWWWWWWW
W S  M      TMW
W W W W W W W W
W  M M M M M  W
W W W W W W W W
W M M M M M M W
W W W W W W W W
W  M M M M M MW
W W W W W W W W
W M M M M M M W
W             W
WWWWWWWWWWWWWWW"""}

LEVEL_12 = {"mirrors": 4, "splitters": 0, "layout": """
WWWWWWWWWWWWWWW
W S         W T
W W           W
W WWWWWWWWWWWWW
W             W
WWWWWWWWWWWWW W
W           W W
W           W W
W           W W
W           W W
W             W
WWWWWWWWWWWWWWW"""}

LEVEL_13 = {"mirrors": 4, "splitters": 1, "layout": """
WWWWWWWWWWWWWWW
WS           TW
W W           W
W WWWWWWWWWW WWW
W            W
WWWWWWWWWWWW W
W            W
W WWWWWWWWWW W
W            W
W WWWWWWWWWW W
W T          W
WWWWWWWWWWWWWWW"""}

LEVEL_14 = {"mirrors": 0, "splitters": 3, "layout": """
WWWWWWWWWWWWWWW
W T         T W
W             W
W      S      W
W             W
W T         T W
W             W
W             W
W             W
W             W
W             W
WWWWWWWWWWWWWWW"""}

LEVEL_15 = {"mirrors": 0, "splitters": 2, "layout": """
WWWWWWWWWWWWWWW
W T         T W
W W           W
W S     B     W
W W           W
W T         T W
W WWWWWWWWWWW W
W W           W
W W   WWWWW   W
W WWWWW   W   W
W         W   W
WWWWWWWWWWWWWWW"""}

LEVEL_16 = {"mirrors": 4, "splitters": 1, "layout": """
WWWWWWWWWWWWWWW
WS    W    M  W
W WWW W WWWWW W
W   W W W   W W
WWW W W W W WWW
W T W W W W   W
W WWW W WWW WWW
W     W W W   W
W WWWWW W WWWWW
W      T      W
W             W
WWWWWWWWWWWWWWW"""}

LEVEL_17 = {"mirrors": 0, "splitters": 0, "layout": """
WWWWWWWWWWWWWWW
W S         T W
W M M M M M M W
W             W
W M M M M M M W
W             W
W M M M M M M W
W             W
W M M M M M M W
W             W
W             W
WWWWWWWWWWWWWWW"""}

LEVEL_18 = {"mirrors": 4, "splitters": 1, "layout": """
WWWWWWWWWWWWWWW
W           T W
W S   B       W
W             W
W             W
W             W
W             W
W             W
W             W
W             W
W T           W
WWWWWWWWWWWWWWW"""}

LEVEL_19 = {"mirrors": 5, "splitters": 0, "layout": """
WWWWWWWWWWWWWWW
W T         W W
WWWWWWWWWWW W W
W S         W W
W WWWWWWWWWWW W
W W         W W
W W WWWWWWWWWWW
W W           W
W WWWWWWWWWWW W
W W           W
W W           W
WWWWWWWWWWWWWWW"""}

LEVEL_20 = {"mirrors": 3, "splitters": 0, "layout": """
WWWWWWWWWWWWWWW
WS M M M M M MTW
W             W
W M M M M M M M W
W             W
W M M M M M M M W
W             W
W M M M M M M M W
W             W
W M M M M M M M W
W             W
WWWWWWWWWWWWWWW"""}

LEVELS = [ LEVEL_1, LEVEL_2, LEVEL_3, LEVEL_4, LEVEL_5, LEVEL_6, LEVEL_7, LEVEL_8, LEVEL_9, LEVEL_10, LEVEL_11, LEVEL_12, LEVEL_13, LEVEL_14, LEVEL_15, LEVEL_16, LEVEL_17, LEVEL_18, LEVEL_19, LEVEL_20 ]

class Spritesheet:
    def __init__(self, filename):
        try: self.sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error: print(f"Varování: Spritesheet '{filename}' nenalezen."); self.sheet = None
    def get_image(self, x, y, width, height):
        if self.sheet is None: image = pygame.Surface((width, height)); image.fill(RED); return image
        image = pygame.Surface((width, height), pygame.SRCALPHA); image.blit(self.sheet, (0, 0), (x, y, width, height)); return image

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
class BeamSplitter(pygame.sprite.Sprite):
    def __init__(self, x, y, placeable=False):
        super().__init__(); self.original_image = pygame.image.load('beam_splitter.png').convert_alpha(); self.image = self.original_image; self.rect = self.image.get_rect(topleft=(x, y)); self.placeable = placeable; self.orientation = 0; self.angle = 0
    def rotate(self):
        self.orientation = (self.orientation + 1) % 2; self.angle -= 90; center = self.rect.center; self.image = pygame.transform.rotate(self.original_image, self.angle); self.rect = self.image.get_rect(center=center)

class Game:
    def __init__(self):
        pygame.init(); pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)); pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock(); self.font = pygame.font.Font(None, 36); self.small_font = pygame.font.Font(None, 28); self.level_select_font = pygame.font.Font(None, 48); self.credits_font = pygame.font.Font(None, 18)
        self.running = True; self.state = 'main_menu'
        self.laser_is_on = False; self.all_sprites = pygame.sprite.Group(); self.mirrors = pygame.sprite.Group(); self.targets = pygame.sprite.Group()
        self.load_assets(); self.load_progress()
        self.selected_item = 'mirror'

    def load_assets(self):
        try: self.mirror_icon = pygame.transform.scale(pygame.image.load('mirror.png').convert_alpha(), (32, 32))
        except pygame.error: self.mirror_icon = pygame.Surface((32,32)); self.mirror_icon.fill(CYAN)
        try: self.splitter_icon = pygame.transform.scale(pygame.image.load('beam_splitter.png').convert_alpha(), (32, 32))
        except pygame.error: self.splitter_icon = pygame.Surface((32,32)); self.splitter_icon.fill(RED)
        self.target_spritesheet = Spritesheet('target_spritesheet.png')
        self.menu_music_loaded = self.load_music_track('menu_music.mp3'); self.game_music_loaded = self.load_music_track('game_music.mp3')
        self.laser_start_sound = self.load_sound('laser_start.mp3'); self.mirror_hit_sound = self.load_sound('mirror_hit.mp3')
        self.target_lit_sound = self.load_sound('target_lit.mp3'); self.victory_sound = self.load_sound('victory.mp3')
    def load_music_track(self, filename):
        try: pygame.mixer.music.load(filename); return True
        except pygame.error: print(f"Varování: Hudba '{filename}' nenalezena."); return False
    def load_sound(self, filename):
        try: return pygame.mixer.Sound(filename)
        except pygame.error: print(f"Varování: Zvuk '{filename}' nenalezen."); return None
    def load_progress(self):
        try:
            with open('progress.txt', 'r') as f: self.highest_unlocked_level = int(f.read())
        except (FileNotFoundError, ValueError): self.highest_unlocked_level = 1
    def save_progress(self):
        with open('progress.txt', 'w') as f: f.write(str(self.highest_unlocked_level))
    def play_music(self, track_name):
        if hasattr(self, 'current_music') and self.current_music == track_name: return
        pygame.mixer.music.stop()
        file_to_load = 'menu_music.mp3' if track_name == 'menu' else 'game_music.mp3'
        music_loaded_flag = self.menu_music_loaded if track_name == 'menu' else self.game_music_loaded
        if music_loaded_flag: pygame.mixer.music.load(file_to_load); pygame.mixer.music.play(-1); self.current_music = track_name
        else: self.current_music = None
        
    def load_level(self, level_index):
        self.current_level_index = level_index; self.play_music('game')
        self.all_sprites.empty(); self.mirrors.empty(); self.targets.empty()
        level_info = LEVELS[level_index]
        self.placeable_mirrors_count = level_info["mirrors"]; self.placeable_splitters_count = level_info.get("splitters", 0)
        
        # ZMĚNA: Správné zpracování multiline stringu
        layout_data = level_info["layout"].strip().splitlines()

        self.tries_left = 3; self.laser_is_on = False; self.laser_on_time = 0; self.laser_duration = 2000
        self.laser_paths = []; self.level_complete = False; self.selected_item = 'mirror'
        for y, row in enumerate(layout_data):
            for x, tile in enumerate(row.strip()):
                px, py = x * TILE_SIZE, y * TILE_SIZE
                if tile == 'W': self.all_sprites.add(Wall(px, py))
                elif tile == 'S': self.laser_source = LaserSource(px, py, (1, 0)); self.all_sprites.add(self.laser_source)
                elif tile == 'T': target = Target(px, py, self.target_spritesheet); self.all_sprites.add(target); self.targets.add(target)
                elif tile == 'M': mirror = Mirror(px, py); self.all_sprites.add(mirror); self.mirrors.add(mirror)
                elif tile == 'B': self.all_sprites.add(BeamSplitter(px, py))

    def calculate_laser_paths(self):
        self.laser_paths = []; mirror_was_hit_this_shot = False
        active_beams = [{'pos': pygame.math.Vector2(self.laser_source.rect.center), 'dir': pygame.math.Vector2(self.laser_source.direction)}]
        processed_beams = 0
        while active_beams and processed_beams < 20:
            beam = active_beams.pop(0); processed_beams += 1
            pos = beam['pos']; direction = beam['dir']; current_path = [pos]
            for _ in range(GRID_WIDTH * GRID_HEIGHT):
                start_point = pos; end_point = pos + direction * (SCREEN_WIDTH * 2)
                closest_intersection = None; collided_sprite = None
                for sprite in self.all_sprites:
                    if sprite == self.laser_source or (isinstance(sprite, (Mirror, BeamSplitter)) and sprite.rect.center == tuple(start_point)): continue
                    clipped_line = sprite.rect.clipline(start_point, end_point)
                    if clipped_line:
                        intersection_point = pygame.math.Vector2(clipped_line[0])
                        if closest_intersection is None or start_point.distance_squared_to(intersection_point) < start_point.distance_squared_to(closest_intersection):
                            closest_intersection = intersection_point; collided_sprite = sprite
                if collided_sprite:
                    current_path.append(closest_intersection)
                    new_start_pos = pygame.math.Vector2(collided_sprite.rect.center)
                    if isinstance(collided_sprite, (Wall, Target)): break 
                    elif isinstance(collided_sprite, Mirror):
                        mirror_was_hit_this_shot = True
                        inc_dir_x, inc_dir_y = int(round(direction.x)), int(round(direction.y))
                        new_dir = pygame.math.Vector2(inc_dir_y, inc_dir_x) if collided_sprite.orientation % 2 == 0 else pygame.math.Vector2(-inc_dir_y, -inc_dir_x)
                        active_beams.append({'pos': new_start_pos, 'dir': new_dir}); break
                    elif isinstance(collided_sprite, BeamSplitter):
                        mirror_was_hit_this_shot = True
                        inc_dir_x = abs(round(direction.x))
                        if collided_sprite.orientation == 0 and inc_dir_x == 1:
                            active_beams.append({'pos': new_start_pos, 'dir': pygame.math.Vector2(0, 1)}); active_beams.append({'pos': new_start_pos, 'dir': pygame.math.Vector2(0, -1)})
                        elif collided_sprite.orientation == 1 and inc_dir_x == 0:
                            active_beams.append({'pos': new_start_pos, 'dir': pygame.math.Vector2(1, 0)}); active_beams.append({'pos': new_start_pos, 'dir': pygame.math.Vector2(-1, 0)})
                        break
                else: current_path.append(end_point); break
            self.laser_paths.append(current_path)
        if mirror_was_hit_this_shot and self.mirror_hit_sound: self.mirror_hit_sound.play()
        for target in self.targets:
            target_hit = False
            for path in self.laser_paths:
                for i in range(len(path) - 1):
                    if target.rect.clipline(path[i], path[i+1]): target_hit = True; break
                if target_hit: break
            target.light_up(target_hit, self)
    def check_level_completion(self):
        if not self.level_complete and self.targets and all(target.is_lit for target in self.targets):
            self.level_complete = True
            if self.victory_sound: self.victory_sound.play()
            next_level_unlocked = self.current_level_index + 2
            if next_level_unlocked > self.highest_unlocked_level:
                self.highest_unlocked_level = next_level_unlocked; self.save_progress()

    def run(self):
        while self.running:
            if self.state == 'main_menu': self.main_menu_loop()
            elif self.state == 'level_select': self.level_select_loop()
            elif self.state == 'in_game': self.game_loop()
            else: self.running = False
    
    def main_menu_loop(self):
        self.play_music('menu')
        continue_button = pygame.Rect(SCREEN_WIDTH/2-150, SCREEN_HEIGHT/2-60, 300, 50); select_button = pygame.Rect(SCREEN_WIDTH/2-150, SCREEN_HEIGHT/2, 300, 50); quit_button = pygame.Rect(SCREEN_WIDTH/2-150, SCREEN_HEIGHT/2+60, 300, 50)
        while self.state == 'main_menu' and self.running: # Added self.running
            self.screen.fill(DARK_GREY); title_surf = pygame.font.Font(None, 72).render(GAME_TITLE, True, WHITE)
            self.screen.blit(title_surf, title_surf.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/4)))
            credits_text = "Tvurci: Tomas S., Benjamin D., Adam V., Nikola D."
            credits_surf = self.font.render(credits_text, True, RED) 
            credits_rect = credits_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 150))
            self.screen.blit(credits_surf, credits_rect)
            mouse_pos = pygame.mouse.get_pos()
            pygame.draw.rect(self.screen, BUTTON_HOVER_COLOR if continue_button.collidepoint(mouse_pos) else BUTTON_COLOR, continue_button); continue_text = self.font.render("Pokračovat", True, WHITE); self.screen.blit(continue_text, continue_text.get_rect(center=continue_button.center))
            pygame.draw.rect(self.screen, BUTTON_HOVER_COLOR if select_button.collidepoint(mouse_pos) else BUTTON_COLOR, select_button); select_text = self.font.render("Výběr úrovně", True, WHITE); self.screen.blit(select_text, select_text.get_rect(center=select_button.center))
            pygame.draw.rect(self.screen, BUTTON_HOVER_COLOR if quit_button.collidepoint(mouse_pos) else BUTTON_COLOR, quit_button); quit_text = self.font.render("Konec", True, WHITE); self.screen.blit(quit_text, quit_text.get_rect(center=quit_button.center))
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.running = False; self.state = 'quit' # Ensure state is also set to 'quit'
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if continue_button.collidepoint(mouse_pos):
                        self.current_level_index = min(self.highest_unlocked_level - 1, len(LEVELS) - 1); self.load_level(self.current_level_index); self.state = 'in_game'
                    if select_button.collidepoint(mouse_pos): self.state = 'level_select'
                    if quit_button.collidepoint(mouse_pos): self.running = False; self.state = 'quit'
            pygame.display.flip(); self.clock.tick(FPS)
    
    def level_select_loop(self):
        self.play_music('menu'); cols, rows = 5, 4; btn_width, btn_height = 100, 100; spacing = 20
        start_x = (SCREEN_WIDTH - (cols*btn_width + (cols-1)*spacing))/2; start_y = (SCREEN_HEIGHT - (rows*btn_height + (rows-1)*spacing))/2
        level_buttons = [pygame.Rect(start_x + (i % cols)*(btn_width+spacing), start_y + (i // cols)*(btn_height+spacing), btn_width, btn_height) for i in range(len(LEVELS))]
        back_button = pygame.Rect(20, SCREEN_HEIGHT - 70, 150, 50)
        while self.state == 'level_select' and self.running: # Added self.running
            self.screen.fill(DARK_GREY); title_surf = self.font.render("Výběr úrovně", True, WHITE); self.screen.blit(title_surf, title_surf.get_rect(center=(SCREEN_WIDTH/2, 50)))
            mouse_pos = pygame.mouse.get_pos()
            for i, rect in enumerate(level_buttons):
                is_unlocked = (i + 1) <= self.highest_unlocked_level; color = LOCKED_BUTTON_COLOR
                if is_unlocked: color = BUTTON_HOVER_COLOR if rect.collidepoint(mouse_pos) else BUTTON_COLOR
                pygame.draw.rect(self.screen, color, rect); level_num_surf = self.level_select_font.render(str(i+1), True, WHITE if is_unlocked else GREY)
                self.screen.blit(level_num_surf, level_num_surf.get_rect(center=rect.center))
            pygame.draw.rect(self.screen, BUTTON_HOVER_COLOR if back_button.collidepoint(mouse_pos) else BUTTON_COLOR, back_button)
            back_text = self.font.render("Zpět", True, WHITE); self.screen.blit(back_text, back_text.get_rect(center=back_button.center))
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.running = False; self.state = 'quit' # Ensure state is also set to 'quit'
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if back_button.collidepoint(mouse_pos): self.state = 'main_menu'
                    for i, rect in enumerate(level_buttons):
                        if rect.collidepoint(mouse_pos) and (i + 1) <= self.highest_unlocked_level: self.current_level_index = i; self.load_level(i); self.state = 'in_game'
            pygame.display.flip(); self.clock.tick(FPS)
            
    def game_loop(self):
        while self.state == 'in_game' and self.running: # Added self.running
            self.events(); self.update(); self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.state = 'quit' # Ensure state is also set to 'quit'
            
            # Rotation with 'R' key
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                mouse_pos = pygame.mouse.get_pos()
                for sprite in self.all_sprites:
                    if isinstance(sprite, (Mirror, BeamSplitter)) and sprite.rect.collidepoint(mouse_pos):
                        sprite.rotate()
                        break # Stop after rotating one sprite

            # Rotation with right mouse click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3: # 3 is for right-click
                pos = event.pos
                for sprite in self.all_sprites:
                    if isinstance(sprite, (Mirror, BeamSplitter)) and sprite.rect.collidepoint(pos):
                        sprite.rotate()
                        break # Stop after rotating one sprite

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                panel_x_start = GRID_WIDTH * TILE_SIZE

                # Handle clicks within the info panel
                if pos[0] > panel_x_start:
                    # Check for "Back to Menu" button first, as it should always be clickable from info panel
                    if hasattr(self, 'back_to_menu_button_rect') and self.back_to_menu_button_rect.collidepoint(pos):
                        self.state = 'main_menu'
                        return # Exit event loop as action is handled

                    # Handle level completion buttons
                    if self.level_complete:
                        if hasattr(self, 'next_level_button_rect') and self.next_level_button_rect.collidepoint(pos):
                            self.current_level_index += 1
                            if self.current_level_index < len(LEVELS):
                                self.load_level(self.current_level_index)
                            else:
                                self.state = 'main_menu' # Go to main menu if no more levels
                        return # Exit event loop after handling level complete buttons

                    # Handle other info panel buttons (Start, Reset, Item Selection)
                    if hasattr(self, 'start_button_rect') and self.start_button_rect.collidepoint(pos) and self.tries_left > 0 and not self.laser_is_on:
                        self.tries_left -= 1
                        self.laser_is_on = True
                        self.laser_on_time = pygame.time.get_ticks()
                        if self.laser_start_sound: self.laser_start_sound.play()
                        self.calculate_laser_paths()
                    elif hasattr(self, 'reset_button_rect') and self.reset_button_rect.collidepoint(pos):
                        self.load_level(self.current_level_index)
                    elif hasattr(self, 'mirror_icon_rect') and self.mirror_icon_rect.collidepoint(pos):
                        self.selected_item = 'mirror'
                    elif hasattr(self, 'splitter_icon_rect') and self.splitter_icon_rect.collidepoint(pos):
                        self.selected_item = 'splitter'
                    return # Exit event loop after handling info panel buttons

                # Handle placing items with left click (button == 1) on the game grid
                if event.button == 1:
                    grid_x, grid_y = pos[0] // TILE_SIZE, pos[1] // TILE_SIZE
                    # Ensure the click is within the game grid boundaries, not the info panel area
                    if grid_x < GRID_WIDTH and grid_y < GRID_HEIGHT:
                        clicked_sprite = next((s for s in self.all_sprites if s.rect.collidepoint(pos)), None)
                        if clicked_sprite is None: # Only place if no sprite is already there
                            if self.selected_item == 'mirror' and self.placeable_mirrors_count > 0:
                                self.all_sprites.add(Mirror(grid_x * TILE_SIZE, grid_y * TILE_SIZE, True)) # Fixed Tile_SIZE typo
                                self.placeable_mirrors_count -= 1
                            elif self.selected_item == 'splitter' and self.placeable_splitters_count > 0:
                                self.all_sprites.add(BeamSplitter(grid_x * TILE_SIZE, grid_y * TILE_SIZE, True))
                                self.placeable_splitters_count -= 1
    
    def update(self):
        if self.laser_is_on:
            now = pygame.time.get_ticks()
            if now - self.laser_on_time > self.laser_duration:
                if not self.level_complete:
                    self.laser_is_on = False; self.laser_paths = []
                    for target in self.targets: target.light_up(False, self)
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
        for path in self.laser_paths:
            if len(path) > 1:
                pulse = (math.sin(pygame.time.get_ticks() * 0.01) + 1) / 2
                color = (255, int(100 + 155 * pulse), int(100 + 155 * pulse))
                pygame.draw.lines(self.screen, color, False, path, 5)

    def draw_info_panel(self):
        panel_rect = pygame.Rect(GRID_WIDTH * TILE_SIZE, 0, INFO_PANEL_WIDTH, SCREEN_HEIGHT)
        pygame.draw.rect(self.screen, DARK_GREY, panel_rect)
        
        # Level info
        level_text = self.font.render(f"Level {self.current_level_index + 1}", True, WHITE)
        self.screen.blit(level_text, (panel_rect.x + 20, 20))
        
        # Inventory
        inventory_text = self.small_font.render("Inventář:", True, WHITE)
        self.screen.blit(inventory_text, (panel_rect.x + 20, 80))
        
        self.mirror_icon_rect = pygame.Rect(panel_rect.x + 20, 110, TILE_SIZE, TILE_SIZE)
        if self.selected_item == 'mirror': pygame.draw.rect(self.screen, SELECTED_ITEM_COLOR, self.mirror_icon_rect, 3)
        self.screen.blit(self.mirror_icon, (self.mirror_icon_rect.x + 8, self.mirror_icon_rect.y + 8))
        count_text_m = self.font.render(f"x {self.placeable_mirrors_count}", True, WHITE)
        self.screen.blit(count_text_m, (panel_rect.x + 80, 115))
        
        self.splitter_icon_rect = pygame.Rect(panel_rect.x + 20, 170, TILE_SIZE, TILE_SIZE)
        if self.selected_item == 'splitter': pygame.draw.rect(self.screen, SELECTED_ITEM_COLOR, self.splitter_icon_rect, 3)
        self.screen.blit(self.splitter_icon, (self.splitter_icon_rect.x + 8, self.splitter_icon_rect.y + 8))
        count_text_s = self.font.render(f"x {self.placeable_splitters_count}", True, WHITE)
        self.screen.blit(count_text_s, (panel_rect.x + 80, 175))

        # Back to Menu Button (positioned above other action buttons)
        mouse_pos = pygame.mouse.get_pos()
        self.back_to_menu_button_rect = pygame.Rect(panel_rect.x + 20, 500, 160, 50) # New position
        back_button_color = BUTTON_HOVER_COLOR if self.back_to_menu_button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(self.screen, back_button_color, self.back_to_menu_button_rect)
        back_text_surf = self.small_font.render("Do menu", True, WHITE)
        self.screen.blit(back_text_surf, back_text_surf.get_rect(center=self.back_to_menu_button_rect.center))

        # Tries left
        tries_text = self.font.render(f"Pokusy: {self.tries_left}", True, WHITE)
        self.screen.blit(tries_text, (panel_rect.x + 20, 300)) # Shifted down

        # Start and Reset buttons
        self.start_button_rect = pygame.Rect(panel_rect.x + 20, 350, 160, 50) # Shifted down
        start_color = BUTTON_HOVER_COLOR if self.start_button_rect.collidepoint(mouse_pos) and self.tries_left > 0 and not self.laser_is_on else BUTTON_COLOR if self.tries_left > 0 and not self.laser_is_on else LOCKED_BUTTON_COLOR
        pygame.draw.rect(self.screen, start_color, self.start_button_rect)
        start_text_surf = self.small_font.render("SPUSTIT LASER", True, WHITE)
        self.screen.blit(start_text_surf, start_text_surf.get_rect(center=self.start_button_rect.center))
        
        self.reset_button_rect = pygame.Rect(panel_rect.x + 20, 410, 160, 50) # Shifted down
        reset_color = BUTTON_HOVER_COLOR if self.reset_button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(self.screen, reset_color, self.reset_button_rect)
        reset_text_surf = self.small_font.render("RESTART", True, WHITE)
        self.screen.blit(reset_text_surf, reset_text_surf.get_rect(center=self.reset_button_rect.center))
        
        # Game state messages (out of tries, level complete)
        if self.tries_left == 0 and not self.level_complete and not self.laser_is_on:
            lose_text = self.font.render("Došly pokusy!", True, RED)
            self.screen.blit(lose_text, (panel_rect.x + 20, 470)) # Shifted down
        
        if self.level_complete:
            msg_text = "Level splněn!" if self.current_level_index + 1 < len(LEVELS) else "Vše splněno!"
            button_text = "Další level" if self.current_level_index + 1 < len(LEVELS) else "Do menu"
            
            msg_surf = self.font.render(msg_text, True, GREEN)
            self.screen.blit(msg_surf, (panel_rect.x + 20, 500)) # Shifted down
            
            self.next_level_button_rect = pygame.Rect(panel_rect.x + 20, 520, 160, 50) # Shifted down
            pygame.draw.rect(self.screen, GREEN, self.next_level_button_rect)
            btn_surf = self.small_font.render(button_text, True, BLACK)
            btn_rect = btn_surf.get_rect(center=self.next_level_button_rect.center)
            self.screen.blit(btn_surf, btn_rect)

if __name__ == '__main__':
    game = Game()
    game.run()