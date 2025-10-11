import pygame
import sys
import cv2
from car import Car
from hand_tracker import HandTracker
import time

# --- Pengaturan Dasar ---
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
FPS = 60

# --- Inisialisasi Pygame ---
pygame.init()
pygame.font.init() 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Balap Tangan")
clock = pygame.time.Clock()
GAME_FONT = pygame.font.SysFont('Arial', 100, bold=True)
COUNTDOWN_FONT = pygame.font.SysFont('Arial', 150, bold=True)
HUD_FONT = pygame.font.SysFont('Arial', 30, bold=True) # Font baru untuk HUD

# --- Muat Aset ---
try:
    track_image = pygame.image.load('assets/sirkuit.png').convert_alpha() 
    track_image = pygame.transform.scale(track_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
except pygame.error as e:
    print(f"Error memuat gambar sirkuit: {e}")
    sys.exit()

# --- PERBAIKAN BUG #1: FUNGSI MASK (Hanya mendeteksi warna hijau sebagai tembok) ---
# PASTIKAN WARNA INI SAMA PERSIS DENGAN WARNA HIJAU DI SIRKUIT.PNG ANDA
GREEN_BORDER_COLOR = (3, 112, 62) 

def create_green_border_mask(image, green_color):
    """
    Membuat mask yang hanya mencakup area berwarna hijau tua (border/rumput).
    Ini adalah implementasi yang paling stabil untuk kasus warna solid.
    """
    green_only_surface = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    pixel_array = pygame.PixelArray(image)

    for x in range(image.get_width()):
        for y in range(image.get_height()):
            pixel_rgb = image.get_at((x, y))[:3] 
            if pixel_rgb == green_color:
                green_only_surface.set_at((x, y), (255, 255, 255, 255))

    del pixel_array 
    return pygame.mask.from_surface(green_only_surface)

TRACK_BORDER_MASK = create_green_border_mask(track_image, GREEN_BORDER_COLOR)

# --- Variabel Game Global ---
player_car = None
tracker = None
game_state = "countdown" # "countdown", "playing", "game_over", "win"
show_mask_debug = False 

# --- Variabel Lap & Waktu ---
lap_count = 0
current_lap_time = 0.0
best_lap_time = float('inf') # Infinity
lap_start_time = 0.0
# Rect untuk garis start/finish, sesuaikan ukurannya agar sesuai dengan sirkuit Anda
# Posisi (x, y, width, height) untuk garis finish Anda
FINISH_LINE_RECT = pygame.Rect(270, 480, 100, 10) 
has_crossed_finish_line = False # Untuk mencegah deteksi lap ganda di garis finish

def reset_game():
    global player_car, game_state, countdown_start_time, lap_count, current_lap_time, lap_start_time, has_crossed_finish_line
    # SESUAIKAN KEMBALI POSISI INI HINGGA MOBIL BERADA TEPAT DI TENGAH LINTASAN START
    player_car = Car(360, 515) 
    player_car.angle = 90 # Ubah sudut awal jika perlu, 90 derajat = menghadap ke atas
    game_state = "countdown"
    countdown_start_time = time.time()
    lap_count = 0
    current_lap_time = 0.0
    lap_start_time = 0.0 # Akan diset saat GO!
    has_crossed_finish_line = False # Reset status garis finish

# --- Fungsi Teks ---
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

def draw_hud():
    """Menggambar Head-Up Display (HUD) di layar."""
    # Lap Count
    draw_text(f"Lap: {lap_count}", HUD_FONT, (255, 255, 255), screen, 100, 30)
    
    # Current Lap Time
    if game_state == "playing":
        current_time_display = f"{current_lap_time:.2f}"
    else:
        current_time_display = "0.00"
    draw_text(f"Time: {current_time_display}", HUD_FONT, (255, 255, 255), screen, 100, 70)

    # Best Lap Time
    best_time_display = f"{best_lap_time:.2f}" if best_lap_time != float('inf') else "N/A"
    draw_text(f"Best: {best_time_display}", HUD_FONT, (255, 255, 255), screen, 100, 110)

# --- Inisialisasi awal ---
try:
    tracker = HandTracker()
    reset_game() 
except IOError as e:
    print(e)
    pygame.quit()
    sys.exit()

# --- Game Loop Utama ---
running = True
webcam_frame = None 
while running:
    clock.tick(FPS)

    # --- Perbarui webcam_frame di setiap frame, terlepas dari game_state ---
    _, webcam_frame = tracker.get_steering_input() 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_state == "game_over":
                reset_game()
            if event.key == pygame.K_m: 
                show_mask_debug = not show_mask_debug

    # --- Logika Game Berdasarkan State ---
    if game_state == "countdown":
        elapsed_time = time.time() - countdown_start_time
        remaining_time = 4 - elapsed_time 
        
        if remaining_time <= 0:
            game_state = "playing"
            lap_start_time = time.time() # Mulai waktu lap saat "GO!"
            lap_count = 1 # Mulai lap pertama
        else:
            if remaining_time > 3: countdown_text = "3"
            elif remaining_time > 2: countdown_text = "2"
            elif remaining_time > 1: countdown_text = "1"
            else: countdown_text = "GO!"
            
            # Mobil TIDAK DIUPDATE posisinya atau digerakkan selama countdown
            player_car.stop() # Pastikan mobil diam
            player_car.rotate(0) # Update rotasi agar rect selalu benar

    elif game_state == "playing":
        # Ambil input setir dan gerakan maju (driving_input=1)
        steering_input, _ = tracker.get_steering_input() 
        player_car.update(steering_input, driving_input=1) # Menggunakan driving_input=1 untuk maju
        
        current_lap_time = time.time() - lap_start_time # Perbarui waktu lap

        # --- LOGIKA TABRAKAN DENGAN AREA HIJAU ---
        car_mask = pygame.mask.from_surface(player_car.image)
        offset = (player_car.rect.x, player_car.rect.y)

        if TRACK_BORDER_MASK.overlap(car_mask, offset):
            game_state = "game_over"
            print("GAME OVER! Mobil menabrak area hijau.")
        
        # --- PERBAIKAN BUG #2: LOGIKA TABRAKAN KELUAR BATAS LAYAR ---
        if (player_car.rect.left < 0 or
            player_car.rect.right > SCREEN_WIDTH or
            player_car.rect.top < 0 or
            player_car.rect.bottom > SCREEN_HEIGHT):
            game_state = "game_over"
            print("GAME OVER! Mobil keluar batas layar.")

        # --- LOGIKA DETEKSI LAP ---
        if player_car.rect.colliderect(FINISH_LINE_RECT):
            if not has_crossed_finish_line: # Deteksi hanya sekali per lintasan
                has_crossed_finish_line = True
                lap_count += 1
                if current_lap_time < best_lap_time:
                    best_lap_time = current_lap_time
                lap_start_time = time.time() # Reset timer untuk lap berikutnya
                print(f"Lap {lap_count-1} selesai! Waktu: {current_lap_time:.2f}s")
        elif has_crossed_finish_line and not player_car.rect.colliderect(FINISH_LINE_RECT):
            # Reset flag setelah mobil melewati garis finish sepenuhnya
            has_crossed_finish_line = False
            
    # --- Render / Gambar ---
    screen.blit(track_image, (0, 0))
    player_car.draw(screen) 

    # --- Tampilan UI ---
    if game_state == "countdown":
        draw_text(countdown_text, COUNTDOWN_FONT, (255, 255, 0), screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    elif game_state == "game_over":
        draw_text('GAME OVER!', GAME_FONT, (255, 0, 0), screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50)
        draw_text('Tekan R untuk Restart', pygame.font.SysFont('Arial', 40), (255, 255, 255), screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50)

    draw_hud()

    if show_mask_debug:
        mask_surface = TRACK_BORDER_MASK.to_surface(setcolor=(255,0,0,255), unsetcolor=(0,0,0,0))
        mask_surface.set_alpha(100)
        screen.blit(mask_surface, (0,0))
        pygame.draw.rect(screen, (0, 0, 255), FINISH_LINE_RECT, 2) # Biru

    if webcam_frame is not None:
        webcam_frame_rgb = cv2.cvtColor(webcam_frame, cv2.COLOR_BGR2RGB)
        webcam_surface = pygame.surfarray.make_surface(webcam_frame_rgb.swapaxes(0, 1))
        webcam_display_size = (320, 240) 
        webcam_surface = pygame.transform.scale(webcam_surface, webcam_display_size)
        screen.blit(webcam_surface, (SCREEN_WIDTH - webcam_display_size[0] - 10, SCREEN_HEIGHT - webcam_display_size[1] - 10)) 

    pygame.display.flip()

if tracker:
    tracker.release()
pygame.quit()
sys.exit()