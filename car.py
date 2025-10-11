import pygame
import math

class Car:
    def __init__(self, x, y):
        self.original_image = pygame.image.load('assets/car.png').convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (75, 38)) 
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))

        self.x = float(x)
        self.y = float(y)
        self.angle = 0  
        
        # --- PENGATURAN FISIKA DAN KECEPATAN MOBIL ---
        
        # Kecepatan aktual mobil saat ini (dimulai dari 0)
        self.current_speed = 0.2  
        
        # Seberapa cepat mobil menambah kecepatan saat digas.
        # Angka lebih besar = akselerasi lebih cepat.
        self.acceleration = 0.5   # <--- UBAH INI UNTUK AKSELERASI
        
        # Seberapa cepat mobil melambat saat tidak digas.
        # Angka lebih besar = mobil berhenti lebih cepat.
        self.friction = 0.04      # <--- UBAH INI UNTUK GAYA GESEK
        
        # Kecepatan Puncak yang bisa dicapai mobil.
        # Ini adalah "TOP SPEED" mobil Anda.
        self.max_speed = 10.0      # <--- UBAH INI UNTUK KECEPATAN MAKSIMUM
        
        # Kecepatan belok dasar mobil.
        # Angka lebih besar = mobil lebih lincah saat berbelok.
        self.rotation_speed = 10 # <--- UBAH INI UNTUK KECEPATAN BELOK

    def rotate(self, steering_input):
        """
        Mengubah sudut mobil berdasarkan input setir.
        Perputaran mobil akan sedikit dipengaruhi oleh current_speed, 
        sehingga lebih sulit berbelok tajam saat sangat cepat.
        """
        if steering_input != 0:
            # Logika ini secara otomatis mengurangi kemampuan belok saat kecepatan tinggi
            effective_rotation_speed = self.rotation_speed * (1 - (self.current_speed / self.max_speed) * 0.5)
            self.angle += effective_rotation_speed * steering_input
            self.angle %= 360  

        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def accelerate_decelerate(self, driving_input):
        """
        Mengatur akselerasi atau deselerasi mobil.
        driving_input: 1 (maju), 0 (idle), -1 (rem/mundur jika ada)
        """
        if driving_input > 0: # Input maju
            self.current_speed += self.acceleration
            if self.current_speed > self.max_speed:
                self.current_speed = self.max_speed
        else: # Tidak ada input maju (mobil melambat karena friksi)
            self.current_speed -= self.friction
            if self.current_speed < 0:
                self.current_speed = 0.0 # Mobil tidak bergerak mundur

    def move(self):
        """
        Menggerakkan mobil maju sesuai dengan arah sudutnya dan current_speed.
        """
        self.x += self.current_speed * math.cos(math.radians(self.angle))
        self.y -= self.current_speed * math.sin(math.radians(self.angle)) 
        
        self.rect.center = (round(self.x), round(self.y))

    def update(self, steering_input, driving_input=1): # driving_input default 1 (maju)
        """
        Satu fungsi untuk memanggil semua logika update per frame.
        """
        self.accelerate_decelerate(driving_input)
        self.rotate(steering_input)
        self.move()

    def stop(self):
        """Menghentikan mobil sepenuhnya."""
        self.current_speed = 0.0

    def draw(self, screen):
        """Menampilkan mobil di layar."""
        screen.blit(self.image, self.rect)